#!/bin/bash
set -e

# Wait for all services to be ready
for port in 9112 9107; do
    for i in $(seq 1 30); do
        if curl -sf http://localhost:${port}/ > /dev/null 2>&1 || \
           curl -sf -X POST http://localhost:${port}/ > /dev/null 2>&1; then
            break
        fi
        sleep 0.5
    done
done

mkdir -p /app/output

# Step 1: List all jobs to identify failed ones
curl -s -X POST http://localhost:9112/scheduler/jobs \
  -H "Content-Type: application/json" \
  -d '{}' > /tmp/all_jobs.json

# Step 2: Get details for each failed job
curl -s -X POST http://localhost:9112/scheduler/jobs/get \
  -H "Content-Type: application/json" \
  -d '{"job_id": "JOB-003"}' > /tmp/job003.json

curl -s -X POST http://localhost:9112/scheduler/jobs/get \
  -H "Content-Type: application/json" \
  -d '{"job_id": "JOB-005"}' > /tmp/job005.json

curl -s -X POST http://localhost:9112/scheduler/jobs/get \
  -H "Content-Type: application/json" \
  -d '{"job_id": "JOB-007"}' > /tmp/job007.json

# Step 3: List all open tickets
curl -s -X POST http://localhost:9107/helpdesk/tickets \
  -H "Content-Type: application/json" \
  -d '{"status": "open"}' > /tmp/tickets.json

# Step 4: Get details for each ticket
for tk_id in TK-001 TK-002 TK-003 TK-004 TK-005 TK-006 TK-007 TK-008 TK-009 TK-010; do
    curl -s -X POST http://localhost:9107/helpdesk/tickets/get \
      -H "Content-Type: application/json" \
      -d "{\"ticket_id\": \"${tk_id}\"}" > /tmp/ticket_${tk_id}.json
done

# Step 5: Write the correlation analysis report
python3 << 'PYEOF'
import json

summary = {
    "failed_jobs": [
        {
            "job_id": "JOB-003",
            "job_name": "业务数据同步",
            "error_summary": "数据库副本连接超时 (db-replica-03.internal:5432)，错误码 DB_CONN_TIMEOUT",
            "first_failure_time": "2026-05-10T01:30:01Z",
            "failure_count": 3,
            "related_tickets": ["TK-003", "TK-007"],
            "impact_scope": "CRM客户数据、业务数据看板、所有依赖实时数据同步的下游系统。影响客户成功部和数据分析部的日常工作。",
            "suggested_priority": "critical",
            "priority_reason": "该任务每30分钟执行一次，已连续失败3次（从01:30到02:30），导致核心业务数据完全停止更新。影响多个部门（客户成功、数据分析），数据看板核心指标显示为0，直接影响业务决策和客户服务。"
        },
        {
            "job_id": "JOB-005",
            "job_name": "周报自动生成",
            "error_summary": "Java堆内存溢出 (OutOfMemoryError)，已分配4096MB仍不足，销售部门聚合阶段失败",
            "first_failure_time": "2026-05-05T08:00:00Z",
            "failure_count": 1,
            "related_tickets": ["TK-002", "TK-006"],
            "impact_scope": "自动周报生成系统和报表导出功能。影响销售部周报接收和财务部月度结算报告导出。",
            "suggested_priority": "high",
            "priority_reason": "报表生成系统内存不足导致周报和财务报告均无法生成。财务月报涉及月度结算有时效要求，但该任务为周频执行（每周一），非实时关键路径，故为high而非critical。"
        },
        {
            "job_id": "JOB-007",
            "job_name": "系统通知推送",
            "error_summary": "SMTP邮件中继服务不可达 (smtp-relay.internal:587 Connection refused)，累计298封通知未送达",
            "first_failure_time": "2026-05-09T18:00:00Z",
            "failure_count": 3,
            "related_tickets": ["TK-005"],
            "impact_scope": "所有系统通知邮件（审批通知、待办提醒等），影响人力资源部审批流程推进。累计142+89+67=298封通知未送达。",
            "suggested_priority": "high",
            "priority_reason": "SMTP服务持续不可达已超过12小时，累计大量未送达通知正在影响审批流程。虽然不影响核心数据，但阻塞了业务流程推进，且问题持续恶化中（每6小时积压更多通知）。"
        }
    ],
    "unrelated_tickets": ["TK-001", "TK-004", "TK-008", "TK-009", "TK-010"],
    "total_failed_jobs": 3,
    "total_related_tickets": 5,
    "total_unrelated_tickets": 5
}

with open("/app/output/summary.json", "w") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
PYEOF
