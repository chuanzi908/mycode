# 定时任务故障与工单关联分析

## 任务背景

最近有多个用户通过工单系统报告了各种系统问题，同时运维监控发现定时任务调度系统中也有一些任务执行失败的记录。你需要综合分析这两个系统的数据，找出哪些用户工单实际上是由定时任务故障引起的，并输出一份结构化的关联分析报告。

请完成以下工作：
1. 查看所有定时任务的状态，识别出失败的任务及其详细错误信息
2. 查看当前所有未解决的工单
3. 基于错误类型、时间线和影响范围，分析哪些工单与定时任务故障存在关联
4. 输出一份关联分析报告，说明每个故障任务对应了哪些工单、影响范围和建议处理优先级

完成分析后，将结果写入 `/app/output/summary.json`。

## 可用服务

本地有多个 API 服务正在运行，请使用 `curl` 与之交互。所有数据操作接口均使用 `POST` 方法并接受 JSON 请求体。

### 定时任务调度 API (端口 9112)

| 接口 | 方法 | URL | 说明 |
|------|------|-----|------|
| 列出任务 | POST | `http://localhost:9112/scheduler/jobs` | 列出所有定时任务，可按状态过滤 |
| 获取任务详情 | POST | `http://localhost:9112/scheduler/jobs/get` | 获取指定任务的完整信息（含执行历史） |
| 获取执行历史 | POST | `http://localhost:9112/scheduler/jobs/history` | 获取指定任务的执行历史记录 |

### 工单系统 API (端口 9107)

| 接口 | 方法 | URL | 说明 |
|------|------|-----|------|
| 列出工单 | POST | `http://localhost:9107/helpdesk/tickets` | 列出工单，可按状态过滤 |
| 获取工单详情 | POST | `http://localhost:9107/helpdesk/tickets/get` | 获取指定工单的完整描述和历史 |
| 更新工单 | POST | `http://localhost:9107/helpdesk/tickets/update` | 更新工单属性（优先级、标签等） |

### 请求/响应示例

**列出定时任务：**
```bash
curl -s -X POST http://localhost:9112/scheduler/jobs \
  -H "Content-Type: application/json" \
  -d '{}'
```
响应：`{"jobs": [{"job_id": "JOB-001", "name": "...", "last_status": "success", ...}], "total": 10}`

可通过 `status` 字段过滤：
```bash
curl -s -X POST http://localhost:9112/scheduler/jobs \
  -H "Content-Type: application/json" \
  -d '{"status": "failed"}'
```

**获取任务详情（含执行历史和错误信息）：**
```bash
curl -s -X POST http://localhost:9112/scheduler/jobs/get \
  -H "Content-Type: application/json" \
  -d '{"job_id": "JOB-003"}'
```
响应包含 `execution_history` 数组，失败记录中会包含 `error` 或 `error_message` 字段。

**列出工单：**
```bash
curl -s -X POST http://localhost:9107/helpdesk/tickets \
  -H "Content-Type: application/json" \
  -d '{"status": "open"}'
```
响应：`{"tickets": [{"ticket_id": "TK-001", "title": "...", "priority": "...", "status": "open", ...}], "total": 10}`

**获取工单详情：**
```bash
curl -s -X POST http://localhost:9107/helpdesk/tickets/get \
  -H "Content-Type: application/json" \
  -d '{"ticket_id": "TK-001"}'
```

### 字段说明

- 定时任务的 `execution_history` 中，失败记录可能以 `error`（对象，含 `code` 和 `message`）或 `error_message`（字符串）的形式记录错误信息
- 工单的 `created_at` 字段表示用户提交工单的时间
- 工单的 `category` 和 `tags` 字段可辅助判断工单类型

## 输出规范

将分析结果写入 `/app/output/summary.json`，格式如下：

```json
{
  "failed_jobs": [
    {
      "job_id": "JOB-XXX",
      "job_name": "任务名称",
      "error_summary": "错误摘要",
      "first_failure_time": "首次失败时间（ISO格式）",
      "failure_count": 3,
      "related_tickets": ["TK-XXX", "TK-YYY"],
      "impact_scope": "影响范围描述",
      "suggested_priority": "critical/high/medium/low",
      "priority_reason": "优先级判断理由"
    }
  ],
  "unrelated_tickets": ["TK-XXX", "TK-YYY"],
  "total_failed_jobs": 3,
  "total_related_tickets": 5,
  "total_unrelated_tickets": 5
}
```

字段说明：
- `failed_jobs`: 所有失败任务的分析列表
- `related_tickets`: 该故障任务关联的工单ID列表
- `impact_scope`: 简要描述该故障的业务影响范围
- `suggested_priority`: 建议的处理优先级（基于影响范围和紧急程度）
- `priority_reason`: 给出优先级判断的理由
- `unrelated_tickets`: 与任何定时任务故障无关的工单ID列表
- `total_failed_jobs` / `total_related_tickets` / `total_unrelated_tickets`: 统计数量

## 注意事项

- 所有 API 服务已在运行，无需手动启动
- 本次任务是分析阶段，请勿关闭任何工单（不要调用 close 接口）
- 关联分析应基于错误类型与工单描述的语义匹配以及时间线合理性（工单提交时间应在故障首次发生之后）
- 注意区分真正由故障引起的工单和碰巧提及类似关键词的工单（如功能请求、咨询类等）
- 确保所有工单都被归类（要么关联到某个故障任务，要么归为无关工单），不能遗漏
