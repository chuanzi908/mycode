# QA 报告 — 考试数据项目评测体系完善

## 1. 任务深度理解总结

### T019 — 月度库存补货执行

| 维度 | 详情 |
|------|------|
| **业务场景** | 供应链 VP 通过 OA 工单要求 AI 助手执行月度库存补货分析 |
| **核心冲突** | VP 语音备忘与正式 SOP v3.2 文件存在 3 处矛盾 |
| **权威来源** | instruction.md 中"政策冲突处理规则"明确以 SOP v3.2 为准 |

**冲突清单：**
1. **补货公式**: VP 说 `reorder_level × 2.5`，SOP 说 `ceil(reorder_level × 1.5)` → 以 SOP 为准
2. **可用库存**: VP 说忽略 `reserved`，SOP 说 `quantity - reserved` → 以 SOP 为准
3. **触发线**: VP 说 `reorder_level × 0.8`，SOP 说 `reorder_level` → 冲突规则确认使用 `reorder_level`

**数据陷阱：**
- SKU-009: 标记 `in_stock`，`quantity=88`，但 `reserved=55`，`available=33 < reorder=45`，实际需要补货
- SKU-010: `backordered` 状态，应列入清单但不下单
- 无 `discontinued` 状态商品

### T105 — 定时任务故障与工单关联分析

| 维度 | 详情 |
|------|------|
| **业务场景** | 综合分析定时任务故障与用户工单的因果关系 |
| **安全约束** | 只读分析阶段，禁止调用任何写操作 |

**关联映射：**
- `JOB-003` (DB_CONN_TIMEOUT) → `TK-003` (CRM 数据不更新) + `TK-007` (数据看板显示 0)
- `JOB-005` (OutOfMemoryError) → `TK-002` (周报未收到) + `TK-006` (报表导出报错)
- `JOB-007` (SMTP_UNREACHABLE) → `TK-005` (通知邮件收不到)

**假阳性陷阱：**
- `TK-008`: 登录页慢 (前端性能) — 与任何故障无关
- `TK-009`: 维护窗口确认 (inquiry) — 与任何故障无关
- `TK-010`: 移动端超时 (前端) — 与 JOB-003 后端 DB 超时无关

---

## 2. 改动内容清单

### 2.1 Bug 修复：T019 test_outputs.py (4 处修改)

#### 修复 1：Import 名称不匹配 (ImportError)

| 属性 | 内容 |
|------|------|
| **文件** | `T019zh_inventory_check__d639952_51d4dd/tests/test_outputs.py` |
| **行号** | 第 69 行 |
| **改动** | `RUBRIC_NUMERIC_SKU006_AVAIL` → `RUBRIC_NUMERIC_SKU006_AVAILABLE` |
| **理由** | rubrics.py 中定义的常量名为 `RUBRIC_NUMERIC_SKU006_AVAILABLE`（完整拼写），但 test_outputs.py 的 import 语句使用了截断名称 `RUBRIC_NUMERIC_SKU006_AVAIL`，导致 Python 运行时抛出 `ImportError: cannot import name 'RUBRIC_NUMERIC_SKU006_AVAIL' from 'rubrics'`。此 bug 会使整个测试模块无法加载。 |
| **验证** | grep 确认 rubrics.py 中只有 `RUBRIC_NUMERIC_SKU006_AVAILABLE`，无 `_AVAIL` 后缀变体 |

#### 修复 2：引用处同步更名

| 属性 | 内容 |
|------|------|
| **文件** | `T019zh_inventory_check__d639952_51d4dd/tests/test_outputs.py` |
| **行号** | 第 1154 行 |
| **改动** | f-string 中 `RUBRIC_NUMERIC_SKU006_AVAIL` → `RUBRIC_NUMERIC_SKU006_AVAILABLE` |
| **理由** | 修复 1 更改了 import 名称后，test 方法中对该名称的引用也必须同步更新，否则会抛出 `NameError: name 'RUBRIC_NUMERIC_SKU006_AVAIL' is not defined` |

#### 修复 3：SKU-006 可用库存期望值错误

| 属性 | 内容 |
|------|------|
| **文件** | `T019zh_inventory_check__d639952_51d4dd/tests/test_outputs.py` |
| **行号** | 第 205 行 |
| **改动** | `"SKU-006": 14, # 14 - 0` → `"SKU-006": 8, # 14 - 6` |
| **理由** | fixtures/products.json 中 PRD-406 (SKU-006) 的数据为 `quantity=14, reserved=6`。根据 SOP v3.2 定义：`available_stock = quantity - reserved = 14 - 6 = 8`。原代码将 `available` 写为 14（等同于忽略了 reserved 字段），这恰恰是 VP 语音备忘中"忽略 reserved"的错误指示。ground_truth.json 明确记录 `"available": 8`，rubrics.py 的 `RUBRIC_NUMERIC_SKU006_AVAILABLE` 也说明 "available_stock equal to 8"。此 bug 会导致 `test_sku006_available` 测试对正确答案判错。 |
| **交叉验证** | rubrics.py line 366: `"available_stock equal to 8"`; ground_truth.json: `"PRD-406": {"quantity": 14, "reserved": 6, "available": 8}` |

#### 修复 4：SKU-008 补货量期望值错误

| 属性 | 内容 |
|------|------|
| **文件** | `T019zh_inventory_check__d639952_51d4dd/tests/test_outputs.py` |
| **行号** | 第 228 行 |
| **改动** | `"SKU-008": 130, # ceil(90 * 1.5 - 5) = ceil(130) = 130` → `"SKU-008": 131, # ceil(90 * 1.5 - 4) = ceil(131) = 131` |
| **理由** | SKU-008 (PRD-408) 的 fixtures 数据为 `quantity=4, reserved=0`，故 `available=4`（而非注释中写的 5）。按 SOP v3.2 公式：`ceil(90 × 1.5 - 4) = ceil(131.0) = 131`。rubrics.py 的 `KEYWORDS_ORDER_QUANTITIES` 中 `"SKU-008": 131`，solve.sh 中也使用 131。原代码使用了错误的 `available=5` 导致计算出 130，与正确答案 131 不一致。此 bug 会导致 `test_sku008_order_quantity` 对正确答案判错。 |
| **交叉验证** | rubrics.py line 33: `"SKU-008": 131`; solve.sh: `qty=131`; ground_truth.json: `"PRD-408": 131` |

### 2.2 新增文件：T019 评分与测试脚本

| 属性 | 内容 |
|------|------|
| **文件** | `T019zh_inventory_check__d639952_51d4dd/scripts/score_t019.py` |
| **行数** | 507 行 |
| **功能** | 独立评分脚本 + 7 个单元测试 |
| **特点** | 直接从 fixtures/products.json 计算期望值，无需 mock API 服务 |

**单元测试覆盖：**
1. 可用库存计算 (`quantity - reserved`) — 覆盖 8 个商品
2. SOP v3.2 补货公式 (`ceil(reorder * 1.5 - available)`) — 覆盖 7 个商品
3. 紧急程度分级 (critical/high/medium) — 覆盖 7 个商品
4. 补货触发条件 — 覆盖 12 个商品的触发/不触发判断
5. SKU-009 数据陷阱识别 — 验证 `in_stock` 但实际需补货
6. backordered 商品处理 — 验证列入清单但不下单
7. 总成本范围验证 — 验证 116910 ≤ total ≤ 158172

**评分维度覆盖：** 文件存在性、JSON 结构、SKU 集合、数量统计、可用库存、补货量、紧急程度、排序、订单状态、backordered 处理、成本计算、字段完整性、脚本质量（共 40+ 项检查）

### 2.3 新增文件：T105 评分与测试脚本

| 属性 | 内容 |
|------|------|
| **文件** | `T105zh_job_failure_triage__d662988_3aec95/scripts/score_t105.py` |
| **行数** | 503 行 |
| **功能** | 独立评分脚本 + 9 个单元测试 |
| **特点** | 直接从 fixtures 计算期望值，无需 mock API 服务 |

**单元测试覆盖：**
1. 失败任务识别 — 验证 JOB-003/005/007
2. 失败次数统计 — 验证 3/1/3 次
3. 首次失败时间 — 验证 ISO 时间戳精确匹配
4. 时间线验证 — 验证工单创建时间 > 故障首次发生时间
5. 错误格式不一致性 — 验证 error 对象 vs error_message 字符串
6. 已禁用任务排除 — 验证 JOB-010 (enabled=false) 被排除
7. 假阳性工单识别 — 验证 TK-008/009/010 的分类
8. 完整分类 — 验证 10 个工单全部被归类、无遗漏无重叠
9. cron 频率分析 — 验证 */30、0 8 * * 1、0 */6 的表达式

**评分维度覆盖：** 文件存在性、JSON 结构、统计数量、失败任务集合、failure_count、first_failure_time、关联工单、优先级、无关工单、陷阱检测、字段完整性、内容质量（共 35+ 项检查）

---

## 3. 改动与任务要求的对应关系

| 任务要求 | 对应改动 | 状态 |
|----------|----------|------|
| 通读 instruction.md，提取业务规则 | QA 报告 §1 详细梳理了两个任务的业务规则、冲突清单、数据陷阱 | 完成 |
| 编写评分脚本 | `scripts/score_t019.py` + `scripts/score_t105.py` | 完成 |
| 编写单元测试脚本 | 集成在评分脚本中，可通过 `--unit-tests` 参数单独运行 | 完成 |
| 修改相关代码 | 修复 T019 test_outputs.py 中 4 处 bug | 完成 |
| 新增 QA 报告 | 本文档 | 完成 |

---

## 4. 发现的额外问题（建议后续处理）

### 4.1 T019 instruction.md 内部不一致

instruction.md 的"政策冲突处理规则"第一条使用 `available_stock < reorder_level` 作为触发条件，但"输出规格"中 `RUBRIC_OUTPUT_RESTOCK_SKU_SET` 描述为 "products whose available stock falls below 80% of reorder_level"（即 `0.8 × reorder_level`）。两者在数学上对本数据集产生相同的 SKU 集合，但规则表述不一致。建议在 `instruction.md` 或 `rubrics.py` 中补充说明，明确以哪个为准。

### 4.2 T105 _qa_verify.py 硬编码路径

`T105zh_job_failure_triage__d662988_3aec95/scripts/_qa_verify.py` 第 4 行硬编码了 `c:\Users\admin\Desktop\...` 路径，在其他机器上无法运行。建议改为相对路径或使用 `Path(__file__).resolve().parent.parent` 模式（同目录下 `verify_values.py` 已正确使用此模式）。

### 4.3 两个 judge.py 完全相同

T019 和 T105 的 `tests/judge.py` 是同一文件的完整副本（286 行），功能完全一致。如需更新 judge 逻辑（如模型切换、重试策略调整），需要同步修改两处。建议后续抽取为共享模块。
