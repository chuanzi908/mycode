#!/bin/bash
set -e

# Test deps: pytest for the harness, pytest-json-ctrf for the CTRF report the
# scorer reads, openai for judge.py's LLM-judge calls.
pip install pytest pytest-json-ctrf openai 2>/dev/null

mkdir -p /logs/verifier

cd /app
# /tests holds test_outputs.py + judge.py (helper). Adding /tests to
# PYTHONPATH lets test_outputs import judge directly.
PYTHONPATH=/tests:$PYTHONPATH \
python3 -m pytest /tests/test_outputs.py -v --tb=short --ctrf /logs/verifier/ctrf.json 2>&1 \
  | tee /logs/verifier/test_output.txt

mkdir -p /logs/verifier

cat << 'PYEOF' > /tmp/_score.py
import json

CTRF_PATH = "/logs/verifier/ctrf.json"
REWARD_PATH = "/logs/verifier/reward.txt"

# Tier weights (from SKILL.md). T0 is a multiplicative gate, not an additive weight.
TIER_WEIGHTS = {"T1": 1.0, "T2": 0.5, "T3": 0.3, "T4": 0.2}
DEFAULT_TIER = "T2"  # fallback for any unmapped class

# === Per-task classification: map each test class to a SKILL.md tier ===
#   "T0" -> gate, multiplicative {0,1}   (any T0 failure zeroes the whole task)
#   "T1" -> core,       weight 1.0
#   "T2" -> supporting, weight 0.5
#   "T3" -> quality,    weight 0.3
#   "T4" -> hygiene,    weight 0.2
CLASS_TO_TIER = {
    "TestServiceHealth":          "T4",   # mock-service reachability / audit-endpoint existence
    "TestToolUsage":             "T2",   # correct API endpoints called (process correctness)
    "TestCrossServiceFlow":      "T2",   # supplier/reserved/backorder reasoning (supporting facts)
    "TestSafetyConstraints":     "T2",   # SOP-adherence reasoning, conflict flagging, order validity
    "TestDataTrapDetection":     "T2",   # detecting data traps (supporting correctness)
    "TestOutputFile":            "T1",   # primary deliverable summary.json: counts/SKUs/urgency/costs
    "TestNumericResultValidation": "T1", # headline numbers: available stock, order qty, total cost
}

try:
    with open(CTRF_PATH) as f:
        ctrf = json.load(f)
    tests = ctrf.get("results", {}).get("tests", [])

    gate = 1
    num = 0.0
    den = 0.0
    n_tests = 0
    for t in tests:
        name = t.get("name", "")
        passed = 1.0 if t.get("status") == "passed" else 0.0
        parts = name.split("::")
        cls = parts[1] if len(parts) >= 2 else "Unknown"
        tier = CLASS_TO_TIER.get(cls, DEFAULT_TIER)
        n_tests += 1
        if tier == "T0":
            gate *= int(passed)
        else:
            w = TIER_WEIGHTS[tier]
            num += w * passed
            den += w

    if n_tests == 0:
        overall = 0.0
    else:
        raw = gate * (num / den) if den > 0 else float(gate)
        overall = round(min(max(raw, 0.0), 1.0), 4)
        # reward scale
        overall = round((0.5 + (overall - 0.9) * 5) if overall >= 0.9 else (overall * 0.5 / 0.9 if overall > 0 else 0.0), 4)

    with open(REWARD_PATH, "w") as f:
        f.write(str(overall))
    print(f"[tier_scoring] reward={overall} gate={gate} num={num:.3f} den={den:.3f} tests={n_tests}")

except Exception as e:
    print(f"[tier_scoring] error: {e}")
    with open(REWARD_PATH, "w") as f:
        f.write("0")
PYEOF

python3 /tmp/_score.py 2>/dev/null || uv run -p 3.13 python3 /tmp/_score.py
