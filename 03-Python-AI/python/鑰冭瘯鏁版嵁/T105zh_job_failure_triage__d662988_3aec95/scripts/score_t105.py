#!/usr/bin/env python3
"""T105 定时任务故障关联分析 — 独立评分与测试脚本

直接从 fixtures 计算所有期望值，验证 summary.json 的正确性。
无需依赖 mock API 服务，可离线运行。

用法:
  python3 scripts/score_t105.py [--output-dir /app/output]
"""

import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 路径配置
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
JOBS_PATH = ROOT / "environment" / "resources" / "fixtures" / "scheduler" / "jobs.json"
TICKETS_PATH = ROOT / "environment" / "resources" / "fixtures" / "helpdesk" / "tickets.json"

DEFAULT_OUTPUT_DIR = ROOT / "environment" / "output"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_output(output_dir):
    path = Path(output_dir) / "summary.json"
    if not path.is_file():
        return None, str(path)
    with open(path, encoding="utf-8") as f:
        return json.load(f), str(path)


# ---------------------------------------------------------------------------
# 从 fixtures 独立计算所有期望值
# ---------------------------------------------------------------------------

def compute_expected(jobs, tickets):
    """从源数据独立计算所有期望值。"""

    # --- 1. 识别失败任务 ---
    failed_jobs = [j for j in jobs if j["last_status"] == "failed"]
    failed_ids = sorted(j["job_id"] for j in failed_jobs)

    # --- 2. 每个失败任务的详细信息 ---
    job_details = {}
    for j in failed_jobs:
        jid = j["job_id"]
        failed_runs = [r for r in j.get("execution_history", [])
                       if r["status"] == "failed"]
        first_failure = min(failed_runs, key=lambda r: r["started_at"])

        # 提取错误信息（处理两种格式：error 对象 和 error_message 字符串）
        first_err = failed_runs[0]
        if "error" in first_err and isinstance(first_err["error"], dict):
            err = first_err["error"]
            error_summary = f"{err.get('code', '')}: {err.get('message', '')}"
        elif "error_message" in first_err:
            error_summary = first_err["error_message"]
        else:
            error_summary = "Unknown error"

        job_details[jid] = {
            "job_id": jid,
            "job_name": j["name"],
            "error_summary": error_summary,
            "first_failure_time": first_failure["started_at"],
            "failure_count": len(failed_runs),
            "cron_expression": j["cron_expression"],
            "enabled": j["enabled"],
        }

    # --- 3. 关联分析（基于语义 + 时间线） ---
    # JOB-003 (业务数据同步, DB_CONN_TIMEOUT) → TK-003 (CRM数据不更新), TK-007 (数据看板显示0)
    # JOB-005 (周报自动生成, OutOfMemoryError) → TK-002 (周报未收到), TK-006 (报表导出报错)
    # JOB-007 (系统通知推送, SMTP_UNREACHABLE) → TK-005 (通知邮件收不到)
    expected_correlations = {
        "JOB-003": {"related": ["TK-003", "TK-007"], "priority": "critical"},
        "JOB-005": {"related": ["TK-002", "TK-006"], "priority": "high"},
        "JOB-007": {"related": ["TK-005"], "priority": "high"},
    }

    # --- 4. 无关工单 ---
    all_related = set()
    for v in expected_correlations.values():
        all_related.update(v["related"])
    all_ticket_ids = {t["ticket_id"] for t in tickets}
    expected_unrelated = sorted(all_ticket_ids - all_related)

    return {
        "failed_ids": failed_ids,
        "job_details": job_details,
        "correlations": expected_correlations,
        "all_related": sorted(all_related),
        "unrelated": expected_unrelated,
        "total_failed": len(failed_ids),
        "total_related": len(all_related),
        "total_unrelated": len(expected_unrelated),
    }


# ---------------------------------------------------------------------------
# 评分系统
# ---------------------------------------------------------------------------

class ScoreResult:
    def __init__(self):
        self.tests = []
        self.passed = 0
        self.failed = 0

    def add(self, name: str, passed: bool, detail: str = ""):
        self.tests.append({"name": name, "passed": passed, "detail": detail})
        if passed:
            self.passed += 1
        else:
            self.failed += 1

    def score(self) -> float:
        total = self.passed + self.failed
        return round(self.passed / total, 4) if total > 0 else 0.0

    def print_report(self):
        print("=" * 70)
        print("T105 定时任务故障关联分析 — 评分报告")
        print("=" * 70)
        for t in self.tests:
            status = "PASS" if t["passed"] else "FAIL"
            detail = f"  ({t['detail']})" if t["detail"] else ""
            print(f"  [{status}] {t['name']}{detail}")
        print("-" * 70)
        total = self.passed + self.failed
        print(f"结果: {self.passed}/{total} 通过, 得分: {self.score():.2%}")
        print("=" * 70)


def run_scoring(output_dir: str) -> ScoreResult:
    jobs = load_json(JOBS_PATH)
    tickets = load_json(TICKETS_PATH)
    expected = compute_expected(jobs, tickets)
    result = ScoreResult()

    # ===== 1. 文件存在性 =====
    output, output_path = load_output(output_dir)
    result.add("文件存在: summary.json", output is not None, output_path)

    if output is None:
        return result

    result.add("summary.json 是合法 JSON", isinstance(output, dict))

    # ===== 2. JSON 结构 =====
    required_keys = {"failed_jobs", "unrelated_tickets", "total_failed_jobs",
                     "total_related_tickets", "total_unrelated_tickets"}
    missing = required_keys - set(output.keys())
    result.add("JSON 顶层字段完整", len(missing) == 0,
               f"缺失: {missing}" if missing else "")

    failed_jobs_out = output.get("failed_jobs", [])
    unrelated_out = output.get("unrelated_tickets", [])

    # ===== 3. 统计数量 =====
    result.add("total_failed_jobs == 3",
               output.get("total_failed_jobs") == expected["total_failed"],
               f"期望={expected['total_failed']}, 实际={output.get('total_failed_jobs')}")

    result.add("total_related_tickets == 5",
               output.get("total_related_tickets") == expected["total_related"],
               f"期望={expected['total_related']}, 实际={output.get('total_related_tickets')}")

    result.add("total_unrelated_tickets == 5",
               output.get("total_unrelated_tickets") == expected["total_unrelated"],
               f"期望={expected['total_unrelated']}, 实际={output.get('total_unrelated_tickets')}")

    # ===== 4. 失败任务识别 =====
    actual_failed_ids = sorted(j.get("job_id") for j in failed_jobs_out)
    result.add("失败任务集合正确",
               set(actual_failed_ids) == set(expected["failed_ids"]),
               f"期望={expected['failed_ids']}, 实际={actual_failed_ids}")

    # 不应包含成功任务
    successful_ids = {j["job_id"] for j in jobs if j["last_status"] == "success"}
    wrongly_included = set(actual_failed_ids) & successful_ids
    result.add("未包含成功任务", len(wrongly_included) == 0,
               f"错误包含: {wrongly_included}" if wrongly_included else "")

    # 不应包含已禁用任务 (JOB-010)
    result.add("未包含已禁用任务 JOB-010",
               "JOB-010" not in actual_failed_ids)

    # ===== 5. 每个失败任务的详细检查 =====
    for jid, exp_detail in expected["job_details"].items():
        actual_job = next((j for j in failed_jobs_out
                           if j.get("job_id") == jid), None)
        if actual_job is None:
            result.add(f"{jid} 存在于 failed_jobs", False, "未找到")
            continue
        result.add(f"{jid} 存在于 failed_jobs", True)

        # failure_count
        result.add(f"{jid} failure_count == {exp_detail['failure_count']}",
                   actual_job.get("failure_count") == exp_detail["failure_count"],
                   f"实际={actual_job.get('failure_count')}")

        # first_failure_time
        result.add(f"{jid} first_failure_time == {exp_detail['first_failure_time']}",
                   actual_job.get("first_failure_time") == exp_detail["first_failure_time"],
                   f"实际={actual_job.get('first_failure_time')}")

    # ===== 6. 关联工单正确性 =====
    for jid, exp_corr in expected["correlations"].items():
        actual_job = next((j for j in failed_jobs_out
                           if j.get("job_id") == jid), None)
        if actual_job is None:
            continue

        actual_related = set(actual_job.get("related_tickets", []))
        expected_related = set(exp_corr["related"])

        result.add(f"{jid} related_tickets 包含 {sorted(exp_corr['related'])}",
                   expected_related <= actual_related,
                   f"实际={sorted(actual_related)}")

        # suggested_priority
        result.add(f"{jid} suggested_priority == {exp_corr['priority']}",
                   actual_job.get("suggested_priority") == exp_corr["priority"],
                   f"实际={actual_job.get('suggested_priority')}")

    # ===== 7. 无关工单集合 =====
    actual_unrelated = set(unrelated_out)
    expected_unrelated = set(expected["unrelated"])
    result.add("unrelated_tickets 集合正确",
               actual_unrelated == expected_unrelated,
               f"期望={sorted(expected_unrelated)}, 实际={sorted(actual_unrelated)}")

    # 确认关键陷阱工单分类正确
    for tid in ["TK-009", "TK-010", "TK-008"]:
        result.add(f"{tid} 在 unrelated_tickets 中",
                   tid in actual_unrelated,
                   f"这是一个容易误判为相关的陷阱工单")

    for tid in ["TK-006", "TK-007"]:
        result.add(f"{tid} 不在 unrelated_tickets 中",
                   tid not in actual_unrelated,
                   f"该工单应关联到失败任务")

    # ===== 8. 所有工单都被分类 =====
    all_classified = actual_unrelated.copy()
    for j in failed_jobs_out:
        all_classified.update(j.get("related_tickets", []))
    all_ticket_ids = {t["ticket_id"] for t in tickets}
    missing_tickets = all_ticket_ids - all_classified
    result.add("所有 10 个工单都被分类",
               len(missing_tickets) == 0,
               f"遗漏: {missing_tickets}" if missing_tickets else "")

    # ===== 9. 字段完整性 =====
    required_job_fields = {
        "job_id", "job_name", "error_summary", "first_failure_time",
        "failure_count", "related_tickets", "impact_scope",
        "suggested_priority", "priority_reason"
    }
    for j in failed_jobs_out:
        jid = j.get("job_id", "?")
        missing_f = required_job_fields - set(j.keys())
        result.add(f"{jid} 字段完整",
                   len(missing_f) == 0,
                   f"缺失: {missing_f}" if missing_f else "")

    # ===== 10. 内容质量基础检查 =====
    for j in failed_jobs_out:
        jid = j.get("job_id", "?")
        # impact_scope 非空
        impact = j.get("impact_scope", "")
        result.add(f"{jid} impact_scope 非空",
                   bool(impact and len(str(impact)) > 5))

        # priority_reason 非空
        reason = j.get("priority_reason", "")
        result.add(f"{jid} priority_reason 非空",
                   bool(reason and len(str(reason)) > 5))

    return result


# ---------------------------------------------------------------------------
# 单元测试: 核心分析逻辑
# ---------------------------------------------------------------------------

def test_failed_job_identification():
    """测试失败任务识别"""
    jobs = load_json(JOBS_PATH)
    failed = [j for j in jobs if j["last_status"] == "failed"]
    failed_ids = sorted(j["job_id"] for j in failed)
    assert failed_ids == ["JOB-003", "JOB-005", "JOB-007"], \
        f"失败任务应为 JOB-003/005/007, 实际 {failed_ids}"
    print("  [PASS] 失败任务识别")


def test_failure_counts():
    """测试失败次数统计"""
    jobs = load_json(JOBS_PATH)
    expected = {"JOB-003": 3, "JOB-005": 1, "JOB-007": 3}
    for j in jobs:
        jid = j["job_id"]
        if jid in expected:
            count = len([r for r in j["execution_history"]
                         if r["status"] == "failed"])
            assert count == expected[jid], \
                f"{jid} 失败次数: 期望 {expected[jid]}, 实际 {count}"
    print("  [PASS] 失败次数统计")


def test_first_failure_times():
    """测试首次失败时间"""
    jobs = load_json(JOBS_PATH)
    expected = {
        "JOB-003": "2026-05-10T01:30:01Z",
        "JOB-005": "2026-05-05T08:00:00Z",
        "JOB-007": "2026-05-09T18:00:00Z",
    }
    for j in jobs:
        jid = j["job_id"]
        if jid in expected:
            failed_runs = [r for r in j["execution_history"]
                           if r["status"] == "failed"]
            first = min(failed_runs, key=lambda r: r["started_at"])
            assert first["started_at"] == expected[jid], \
                f"{jid} 首次失败: 期望 {expected[jid]}, 实际 {first['started_at']}"
    print("  [PASS] 首次失败时间")


def test_ticket_timeline_validation():
    """测试工单时间线验证: 工单创建时间 > 故障首次发生时间"""
    jobs = load_json(JOBS_PATH)
    tickets = load_json(TICKETS_PATH)

    correlations = {
        "JOB-003": ["TK-003", "TK-007"],
        "JOB-005": ["TK-002", "TK-006"],
        "JOB-007": ["TK-005"],
    }

    for jid, ticket_ids in correlations.items():
        j = next(x for x in jobs if x["job_id"] == jid)
        failed_runs = [r for r in j["execution_history"]
                       if r["status"] == "failed"]
        first_fail = min(failed_runs, key=lambda r: r["started_at"])["started_at"]

        for tid in ticket_ids:
            t = next(x for x in tickets if x["ticket_id"] == tid)
            assert t["created_at"] > first_fail, \
                f"{tid} ({t['created_at']}) 应在 {jid} 首次失败 ({first_fail}) 之后"
    print("  [PASS] 时间线验证")


def test_error_format_inconsistency():
    """测试错误格式不一致性: JOB-005 用 error_message, 其他用 error 对象"""
    jobs = load_json(JOBS_PATH)

    for j in jobs:
        jid = j["job_id"]
        for r in j["execution_history"]:
            if r["status"] == "failed":
                if jid == "JOB-005":
                    assert "error_message" in r, \
                        f"JOB-005 {r['run_id']} 应有 error_message 字符串"
                    assert isinstance(r["error_message"], str), \
                        f"JOB-005 error_message 应为字符串"
                elif jid in ("JOB-003", "JOB-007"):
                    assert "error" in r, \
                        f"{jid} {r['run_id']} 应有 error 对象"
                    assert isinstance(r["error"], dict), \
                        f"{jid} error 应为字典"
    print("  [PASS] 错误格式不一致性")


def test_disabled_job_exclusion():
    """测试已禁用任务 JOB-010 不应出现在分析中"""
    jobs = load_json(JOBS_PATH)
    job010 = next(j for j in jobs if j["job_id"] == "JOB-010")
    assert job010["enabled"] is False, "JOB-010 应为 disabled"
    assert job010["next_run"] is None, "JOB-010 next_run 应为 null"
    assert job010["last_status"] == "success", "JOB-010 last_status 为 success"
    print("  [PASS] 已禁用任务排除")


def test_false_positive_tickets():
    """测试假阳性工单识别"""
    tickets = load_json(TICKETS_PATH)

    # TK-009: 维护窗口确认 (category=inquiry) — 与故障无关
    tk009 = next(t for t in tickets if t["ticket_id"] == "TK-009")
    assert tk009["category"] == "inquiry", "TK-009 应为 inquiry 类型"

    # TK-010: 移动端超时 (category=performance) — 前端问题，与后端 DB 超时无关
    tk010 = next(t for t in tickets if t["ticket_id"] == "TK-010")
    assert tk010["category"] == "performance", "TK-010 应为 performance 类型"
    assert "mobile" in tk010["tags"], "TK-010 应有 mobile 标签"

    # TK-008: 登录页慢 (category=performance) — 前端性能问题
    tk008 = next(t for t in tickets if t["ticket_id"] == "TK-008")
    assert tk008["category"] == "performance", "TK-008 应为 performance 类型"
    assert "login" in tk008["tags"], "TK-008 应有 login 标签"

    print("  [PASS] 假阳性工单识别")


def test_complete_classification():
    """测试所有 10 个工单都被完整分类"""
    tickets = load_json(TICKETS_PATH)
    related = {"TK-002", "TK-003", "TK-005", "TK-006", "TK-007"}
    unrelated = {"TK-001", "TK-004", "TK-008", "TK-009", "TK-010"}
    all_ids = {t["ticket_id"] for t in tickets}

    assert related | unrelated == all_ids, \
        f"分类不完整: 遗漏 {all_ids - related - unrelated}"
    assert related & unrelated == set(), \
        f"分类有重叠: {related & unrelated}"
    print("  [PASS] 完整分类")


def test_cron_frequency_analysis():
    """测试 cron 表达式频率分析"""
    jobs = load_json(JOBS_PATH)

    # JOB-003: */30 * * * * = 每30分钟
    j003 = next(j for j in jobs if j["job_id"] == "JOB-003")
    assert j003["cron_expression"] == "*/30 * * * *", \
        "JOB-003 应为每30分钟执行"

    # JOB-005: 0 8 * * 1 = 每周一 08:00
    j005 = next(j for j in jobs if j["job_id"] == "JOB-005")
    assert j005["cron_expression"] == "0 8 * * 1", \
        "JOB-005 应为每周一执行"

    # JOB-007: 0 */6 * * * = 每6小时
    j007 = next(j for j in jobs if j["job_id"] == "JOB-007")
    assert j007["cron_expression"] == "0 */6 * * *", \
        "JOB-007 应为每6小时执行"

    print("  [PASS] cron 频率分析")


# ---------------------------------------------------------------------------
# 主程序
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="T105 故障关联评分")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR),
                        help="输出文件目录")
    parser.add_argument("--unit-tests", action="store_true",
                        help="仅运行单元测试")
    args = parser.parse_args()

    print("=" * 70)
    print("T105 定时任务故障关联分析 — 评测系统")
    print("=" * 70)

    # 运行单元测试
    print("\n--- 单元测试: 核心分析逻辑 ---")
    test_funcs = [
        test_failed_job_identification,
        test_failure_counts,
        test_first_failure_times,
        test_ticket_timeline_validation,
        test_error_format_inconsistency,
        test_disabled_job_exclusion,
        test_false_positive_tickets,
        test_complete_classification,
        test_cron_frequency_analysis,
    ]
    ut_pass = 0
    ut_fail = 0
    for fn in test_funcs:
        try:
            fn()
            ut_pass += 1
        except AssertionError as e:
            print(f"  [FAIL] {fn.__name__}: {e}")
            ut_fail += 1

    print(f"\n单元测试: {ut_pass}/{ut_pass + ut_fail} 通过")

    if args.unit_tests:
        return 0 if ut_fail == 0 else 1

    # 运行评分
    print("\n--- 输出评分 ---")
    result = run_scoring(args.output_dir)
    result.print_report()

    return 0 if result.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
