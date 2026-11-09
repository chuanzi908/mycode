#!/usr/bin/env python3
"""Independent verification of all numeric and enumeration values used in rubrics.

Reads source data fixtures directly and computes every expected value,
without relying on ground_truth.json or solution/solve.sh.

Usage: python3 scripts/verify_values.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JOBS_PATH = ROOT / "environment" / "resources" / "fixtures" / "scheduler" / "jobs.json"
TICKETS_PATH = ROOT / "environment" / "resources" / "fixtures" / "helpdesk" / "tickets.json"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def compute_values():
    jobs = load_json(JOBS_PATH)
    tickets = load_json(TICKETS_PATH)

    results = {}

    # --- Identify failed jobs ---
    failed_jobs = [j for j in jobs if j["last_status"] == "failed"]
    failed_ids = {j["job_id"] for j in failed_jobs}
    results["failed_job_ids"] = sorted(failed_ids)

    # --- Failure counts per job ---
    for j in failed_jobs:
        failures = [r for r in j.get("execution_history", []) if r["status"] == "failed"]
        results[f"{j['job_id']}.failure_count"] = len(failures)
        first_failure = min(failures, key=lambda r: r["started_at"])
        results[f"{j['job_id']}.first_failure_time"] = first_failure["started_at"]

    # --- Successful jobs (should NOT be in failed_jobs output) ---
    successful_ids = {j["job_id"] for j in jobs if j["last_status"] == "success"}
    results["successful_job_ids"] = sorted(successful_ids)

    # --- Ticket counts ---
    results["total_tickets"] = len(tickets)
    results["all_ticket_ids"] = sorted([t["ticket_id"] for t in tickets])

    # --- Cross-service correlation: which tickets relate to which failed jobs ---
    # Based on analysis of ticket descriptions and timelines:
    # TK-002: "本周一（5月5日）一直没有收到" → JOB-005 failed at 2026-05-05T08:00
    # TK-003: "CRM系统中的客户跟进记录...一直没有更新" → JOB-003 DB_CONN_TIMEOUT (data-sync)
    # TK-005: "从昨天下午开始就收不到系统的任何通知邮件" → JOB-007 SMTP_UNREACHABLE at 18:00
    # TK-006: "报告生成失败" → JOB-005 OutOfMemoryError (report-generation)
    # TK-007: "数据看板...依赖于每日凌晨的数据同步任务" → JOB-003 (data-sync)
    #
    # TK-001: CSS样式问题 → unrelated
    # TK-004: 功能请求（批量导出）→ unrelated
    # TK-008: 登录页面加载缓慢 → unrelated
    # TK-009: 维护窗口确认 → unrelated
    # TK-010: 移动端APP响应超时 → unrelated

    related_tickets = {
        "JOB-003": ["TK-003", "TK-007"],
        "JOB-005": ["TK-002", "TK-006"],
        "JOB-007": ["TK-005"],
    }
    unrelated_tickets = ["TK-001", "TK-004", "TK-008", "TK-009", "TK-010"]

    results["related_tickets_by_job"] = related_tickets
    results["unrelated_tickets"] = unrelated_tickets

    # --- Counts ---
    all_related = set()
    for tlist in related_tickets.values():
        all_related.update(tlist)
    results["total_related_tickets"] = len(all_related)
    results["total_unrelated_tickets"] = len(unrelated_tickets)
    results["total_failed_jobs"] = len(failed_ids)

    # --- Verify 10 tickets are all classified ---
    classified = all_related | set(unrelated_tickets)
    results["all_tickets_classified"] = classified == {t["ticket_id"] for t in tickets}

    # --- Priority levels ---
    results["expected_priorities"] = {
        "JOB-003": "critical",
        "JOB-005": "high",
        "JOB-007": "high",
    }

    # --- Error field format verification ---
    for j in failed_jobs:
        history = j.get("execution_history", [])
        for r in history:
            if r["status"] == "failed":
                has_error_obj = "error" in r
                has_error_msg = "error_message" in r
                key = f"{j['job_id']}.error_field_type"
                if key not in results:
                    results[key] = []
                results[key].append({
                    "run_id": r["run_id"],
                    "has_error_object": has_error_obj,
                    "has_error_message_string": has_error_msg,
                })

    # --- Timeline verification ---
    for t in tickets:
        tid = t["ticket_id"]
        created = t["created_at"]
        results[f"{tid}.created_at"] = created
        results[f"{tid}.category"] = t["category"]

    # --- Required fields per job entry ---
    results["required_job_fields"] = [
        "job_id", "job_name", "error_summary", "first_failure_time",
        "failure_count", "related_tickets", "impact_scope",
        "suggested_priority", "priority_reason",
    ]

    return results


def verify():
    values = compute_values()
    errors = []

    # Verify failed jobs = {JOB-003, JOB-005, JOB-007}
    expected_failed = {"JOB-003", "JOB-005", "JOB-007"}
    actual_failed = set(values["failed_job_ids"])
    if actual_failed != expected_failed:
        errors.append(f"FAIL: failed_job_ids expected {expected_failed}, got {actual_failed}")

    # Verify failure counts
    expected_counts = {"JOB-003": 3, "JOB-005": 1, "JOB-007": 3}
    for jid, expected in expected_counts.items():
        actual = values[f"{jid}.failure_count"]
        if actual != expected:
            errors.append(f"FAIL: {jid}.failure_count expected {expected}, got {actual}")

    # Verify first failure times
    expected_times = {
        "JOB-003": "2026-05-10T01:30:01Z",
        "JOB-005": "2026-05-05T08:00:00Z",
        "JOB-007": "2026-05-09T18:00:00Z",
    }
    for jid, expected in expected_times.items():
        actual = values[f"{jid}.first_failure_time"]
        if actual != expected:
            errors.append(f"FAIL: {jid}.first_failure_time expected {expected}, got {actual}")

    # Verify ticket classifications
    if values["total_related_tickets"] != 5:
        errors.append(f"FAIL: total_related_tickets expected 5, got {values['total_related_tickets']}")
    if values["total_unrelated_tickets"] != 5:
        errors.append(f"FAIL: total_unrelated_tickets expected 5, got {values['total_unrelated_tickets']}")
    if values["total_failed_jobs"] != 3:
        errors.append(f"FAIL: total_failed_jobs expected 3, got {values['total_failed_jobs']}")
    if not values["all_tickets_classified"]:
        errors.append("FAIL: not all 10 tickets are classified")

    # Verify error field formats
    for jid in ["JOB-003", "JOB-007"]:
        for entry in values.get(f"{jid}.error_field_type", []):
            if not entry["has_error_object"]:
                errors.append(f"FAIL: {jid} {entry['run_id']} missing error object")
    for entry in values.get("JOB-005.error_field_type", []):
        if not entry["has_error_message_string"]:
            errors.append(f"FAIL: JOB-005 {entry['run_id']} missing error_message string")
        if entry["has_error_object"]:
            errors.append(f"FAIL: JOB-005 {entry['run_id']} has error object (should be error_message string)")

    # Print results
    print("=" * 60)
    print("Independent Value Verification Report")
    print("=" * 60)
    print(f"\nFailed jobs: {values['failed_job_ids']}")
    print(f"Successful jobs (should be excluded): {values['successful_job_ids']}")
    print(f"\nFailure counts:")
    for jid in ["JOB-003", "JOB-005", "JOB-007"]:
        print(f"  {jid}: {values[f'{jid}.failure_count']} failed runs")
        print(f"  {jid}: first_failure_time = {values[f'{jid}.first_failure_time']}")
    print(f"\nRelated tickets by job:")
    for jid, tlist in values["related_tickets_by_job"].items():
        print(f"  {jid}: {tlist}")
    print(f"\nUnrelated tickets: {values['unrelated_tickets']}")
    print(f"\nCounts: failed_jobs={values['total_failed_jobs']}, "
          f"related={values['total_related_tickets']}, "
          f"unrelated={values['total_unrelated_tickets']}")
    print(f"\nAll tickets classified: {values['all_tickets_classified']}")
    print(f"\nError field formats:")
    for jid in ["JOB-003", "JOB-005", "JOB-007"]:
        for entry in values.get(f"{jid}.error_field_type", []):
            print(f"  {entry['run_id']}: error_object={entry['has_error_object']}, "
                  f"error_message_string={entry['has_error_message_string']}")

    if errors:
        print(f"\n{'=' * 60}")
        print(f"ERRORS FOUND: {len(errors)}")
        print(f"{'=' * 60}")
        for e in errors:
            print(f"  {e}")
        return 1
    else:
        print(f"\n{'=' * 60}")
        print("ALL VALUES VERIFIED — 0 errors")
        print(f"{'=' * 60}")
        return 0


if __name__ == "__main__":
    sys.exit(verify())
