"""judge.py — LLM-judge primitive for rubric-based evaluation.

General-purpose drop-in replacement for keyword-list checks. A test that
used to look like:

    keywords = ["location", "where", "city", "metro", ...]
    found = any(kw in assistant_text for kw in keywords)
    assert found, "Agent should have asked about location"

becomes:

    from judge import judge
    assert judge(
        rubric="Did the assistant ask the user about the property's "
               "geographic location (city / metro / submarket / region)?",
        evidence=assistant_text,
    ), "Agent should have asked about location"

The judge:
  - calls a remote LLM to evaluate evidence against rubric
  - auto-detects Gemini (URL contains "generateContent") vs OpenAI-compat
  - returns a clean bool based solely on the LLM's pass/fail verdict
  - returns a {pass, reason} dict via judge_score()
  - caches verdicts on disk by (rubric, evidence) hash so re-running tests
    doesn't re-hit the LLM

Env vars:
  JUDGE_API_KEY                — auth token
  JUDGE_BASE_URL               — endpoint (auto-detects Gemini vs OpenAI)
  JUDGE_MODEL_ID               — model id, default "gemini-2.5-flash"
  JUDGE_TIMEOUT_SEC            — per-call timeout (default 100)
  JUDGE_MAX_TOKENS             — completion budget (default 4096)
  JUDGE_CACHE_DIR              — verdict cache dir (default /tmp/judge_cache)
  JUDGE_DISABLE_CACHE=1        — bypass cache, always call LLM
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Any


# ---------------------------------------------------------------------------
# Defaults — DeepSeek (OpenAI-compatible API)
# API key must be supplied at runtime via the JUDGE_API_KEY env var.
# ---------------------------------------------------------------------------
_DEFAULT_BASE_URL = "https://api.deepseek.com/v1"
_DEFAULT_MODEL = "deepseek-v4-flash"
_DEFAULT_API_KEY = ""


_SYSTEM_PROMPT = """\
You are a strict, terse grading judge. Determine whether the EVIDENCE
satisfies the RUBRIC with a clear pass or fail verdict.

Output rules:
- Output ONE valid JSON object on a single line. No prose, no markdown
  code-fences, no explanation outside the JSON.
- Schema: {"pass": <true|false>, "reason": "<1-2 sentence justification>"}
- Be conservative on edge cases. If evidence is empty / off-topic / does
  not clearly meet the rubric, return pass=false.
- Synonyms, paraphrases, and structural markers (bullets, headers,
  tables) all count as evidence — judge the *substance*, not the exact
  wording. Do NOT require specific keywords unless the rubric demands them.
- If the rubric asks "did the assistant do X" and the evidence is the
  conversation transcript, look for X anywhere in the assistant's turns.
"""


def _get_config() -> dict:
    return {
        "base_url": os.environ.get("JUDGE_BASE_URL", _DEFAULT_BASE_URL),
        "api_key": os.environ.get("JUDGE_API_KEY", _DEFAULT_API_KEY),
        "model": os.environ.get("JUDGE_MODEL_ID", _DEFAULT_MODEL),
        "timeout": float(os.environ.get("JUDGE_TIMEOUT_SEC", "100")),
        "max_tokens": int(os.environ.get("JUDGE_MAX_TOKENS", "4096")),
    }


def _cache_path(rubric: str, evidence: str) -> str:
    cache_dir = os.environ.get("JUDGE_CACHE_DIR", "/tmp/judge_cache")
    os.makedirs(cache_dir, exist_ok=True)
    h = hashlib.sha256()
    h.update(rubric.encode("utf-8"))
    h.update(b"\x00")
    h.update(evidence.encode("utf-8"))
    h.update(b"\x00")
    h.update(os.environ.get("JUDGE_MODEL_ID", _DEFAULT_MODEL).encode("utf-8"))
    return os.path.join(cache_dir, h.hexdigest()[:32] + ".json")


def _try_cache(path: str) -> dict | None:
    if os.environ.get("JUDGE_DISABLE_CACHE") in ("1", "true", "yes"):
        return None
    if not os.path.isfile(path):
        return None
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return None


def _save_cache(path: str, verdict: dict) -> None:
    if os.environ.get("JUDGE_DISABLE_CACHE") in ("1", "true", "yes"):
        return
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(verdict, f, ensure_ascii=False)
    except Exception:
        pass


def _parse_verdict(raw: str) -> dict:
    """Extract {pass, reason} from the LLM output. Best-effort —
    the model might wrap in markdown despite the system prompt."""
    s = (raw or "").strip()
    if s.startswith("```"):
        # strip code fence
        s = s.strip("`")
        if s.lower().startswith("json"):
            s = s[4:]
        s = s.strip()
    try:
        d = json.loads(s)
    except Exception:
        # try to find the first {...} block
        i = s.find("{")
        j = s.rfind("}")
        if 0 <= i < j:
            try:
                d = json.loads(s[i : j + 1])
            except Exception:
                d = {}
        else:
            d = {}
    out = {
        "pass": bool(d.get("pass", False)),
        "reason": str(d.get("reason", "(unparseable judge output)")),
    }
    return out


def _is_gemini(base_url: str) -> bool:
    return "generateContent" in base_url


def _call_gemini(cfg: dict, system: str, user_msg: str) -> str:
    import httpx
    resp = httpx.post(
        cfg["base_url"],
        headers={"api-key": cfg["api_key"], "Content-Type": "application/json"},
        json={
            "model": cfg["model"],
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user_msg}]}],
            "generationConfig": {
                "maxOutputTokens": cfg["max_tokens"],
                "temperature": 0,
            },
        },
        timeout=cfg["timeout"],
    )
    resp.raise_for_status()
    data = resp.json()
    if "Error" in data or "error" in data:
        raise RuntimeError(data.get("Error") or data.get("error"))
    candidates = data.get("candidates", [])
    if not candidates:
        return ""
    parts = candidates[0].get("content", {}).get("parts", [])
    return "".join(p.get("text", "") for p in parts)


def _call_openai(cfg: dict, system: str, user_msg: str) -> str:
    from openai import OpenAI
    client = OpenAI(
        api_key=cfg["api_key"] or "dummy",
        base_url=cfg["base_url"],
        timeout=cfg["timeout"],
    )
    resp = client.chat.completions.create(
        model=cfg["model"],
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=cfg["max_tokens"],
        temperature=0.0,
    )
    return resp.choices[0].message.content or ""


def judge_score(rubric: str, evidence: str | Any) -> dict:
    """Return {pass: bool, reason: str}.

    `evidence` may be a string OR any JSON-serializable structure (a list
    of conversation turns, a dict, etc.) — it'll be stringified for the
    LLM.
    """
    if not isinstance(evidence, str):
        try:
            evidence_str = json.dumps(evidence, ensure_ascii=False, indent=2)
        except Exception:
            evidence_str = str(evidence)
    else:
        evidence_str = evidence

    cache_p = _cache_path(rubric, evidence_str)
    cached = _try_cache(cache_p)
    if cached is not None:
        return cached

    cfg = _get_config()
    call_fn = _call_gemini if _is_gemini(cfg["base_url"]) else _call_openai

    user_msg = (
        f"RUBRIC:\n{rubric.strip()}\n\n"
        f"EVIDENCE:\n{evidence_str.strip()[:32000]}"
    )

    import random as _rnd
    import time as _t

    last_exc = None
    max_attempts = int(os.environ.get("JUDGE_MAX_ATTEMPTS", "5"))
    base_delay = float(os.environ.get("JUDGE_RETRY_BASE_DELAY", "2.0"))
    for attempt in range(max_attempts):
        try:
            raw = call_fn(cfg, _SYSTEM_PROMPT, user_msg)
            verdict = _parse_verdict(raw)
            _save_cache(cache_p, verdict)
            return verdict
        except Exception as exc:
            last_exc = exc
            if attempt + 1 < max_attempts:
                # Exponential backoff with jitter; longer for rate-limit
                # signals so we don't pile on the quota window.
                msg_lower = str(exc).lower()
                rate_limited = (
                    "rate" in msg_lower
                    or "quota" in msg_lower
                    or "exceed" in msg_lower
                    or "429" in msg_lower
                )
                delay = base_delay * (2 ** attempt)
                if rate_limited:
                    delay = max(delay, 8.0)  # be polite when throttled
                delay += _rnd.uniform(0, 1)
                _t.sleep(delay)

    # All retries exhausted — fail closed (judge couldn't run, so we can't
    # say the agent passed). Do NOT cache, so the next pytest run retries.
    return {
        "pass": False,
        "reason": f"judge LLM call failed after {max_attempts} retries: {type(last_exc).__name__}: {last_exc}",
    }


def judge(rubric: str, evidence: str | Any) -> bool:
    """Convenience wrapper — return True iff the LLM verdict is pass=true."""
    v = judge_score(rubric, evidence)
    return bool(v.get("pass"))


def assert_judge(rubric: str, evidence: str | Any, msg: str | None = None) -> None:
    """pytest-friendly assertion. Failure message includes the judge's reason."""
    v = judge_score(rubric, evidence)
    if v.get("pass"):
        return
    detail = f"reason={v.get('reason')!r}"
    base = msg or f"judge failed for rubric: {rubric!r}"
    raise AssertionError(f"{base}\n  {detail}")


if __name__ == "__main__":
    # Smoke-test from CLI: python judge.py "<rubric>" "<evidence>"
    import sys

    if len(sys.argv) < 3:
        print("usage: judge.py <rubric> <evidence>", file=sys.stderr)
        sys.exit(2)
    v = judge_score(sys.argv[1], sys.argv[2])
    print(json.dumps(v, ensure_ascii=False, indent=2))
