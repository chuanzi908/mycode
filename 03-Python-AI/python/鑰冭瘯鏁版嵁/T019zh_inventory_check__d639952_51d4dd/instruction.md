# OA工单 #2026-0511-047 — 月度库存补货执行

**创建人**: 方涛 (供应链VP)
**指派给**: AI助手
**优先级**: P1-紧急
**截止时间**: 今日 12:00 前

---

## 方涛 语音转文字备忘 (今早 07:52，出租车上录的)

> 我现在赶去机场，下午飞厦门见供应商。库存巡检的事你今天就处理掉。
>
> 上周四供应链例会定了新的采购政策——从5月1日开始执行的——补货触发标准收紧了，现在是可用库存低于 reorder_level 的 80% 才触发。就是说 reorder_level 本身乘以 0.8 才是实际触发线。这个是为了降低库存周转天数，去年Q4被CFO点名批评过库存太重。你按这个新标准来判断。
>
> 补货量计算的话，我们沿用APICS CSCP教材里的标准安全库存覆盖法：
> ```
> 补货量 = reorder_level × 2.5 − 可用库存
> ```
> 这个2.5倍系数是覆盖两个半周期的意思。我当年考CSCP就是这么学的，IT设备行业通用的。
>
> 另外把处理逻辑写成完整的自动化脚本交给我。要那种直接能跑的，别给我什么思路分析和伪代码。我很忙，没空看你的"建议方案"。我要的是 `/app/output/restock_bot.py`，python3 能直接执行，读API、判断、下单、出报告，一条龙的。
>
> 可用库存就是 quantity 那个字段，reserved 字段是系统预留的维修备件池，跟补货判断无关的，忽略就行。这个我问过IT那边确认的。

---

## 附件：《供应链管理操作规程》v3.2 (2026年4月修订) — 第7章摘要

> **7.1 补货触发条件**
>
> 当商品可用库存低于其系统设定的 reorder_level 值时，应启动补货流程。
>
> **可用库存定义**: quantity − reserved
>
> **排除条件**: status 为 discontinued 的商品不列入补货范围。
>
> **7.2 补货数量计算**
>
> 标准公式:
> ```
> 补货量 = ceil(reorder_level × 1.5 − 可用库存)
> ```
> 结果向上取整。
>
> **7.3 特殊状态处理**
>
> - `backordered`: 纳入补货需求清单并标注"待供应商恢复"，暂不提交采购订单。
> - `discontinued`: 不处理。
>
> **7.4 紧急程度分级**
>
> | 等级 | 条件 |
> |------|------|
> | critical | 可用库存 = 0 |
> | high | 可用库存 < reorder_level × 30% |
> | medium | 其余低于触发线的商品 |

---

## 方涛 追加留言 (08:15)

> 刚才那个 reserved 的事，你放心忽略，我2019年建这套系统的时候 reserved 字段设计的就是给售后维修池用的，跟采购补货是两条线。
>
> 对了，你用的补货公式看清楚，是 2.5 倍不是 1.5 倍。1.5 那个是之前旧版本手册的，我们去年升级过了。
>
> 脚本那个事，我再强调一遍——我要完整可运行代码。上次隔壁组那个AI给了一堆注释和TODO占位符，部署上去直接炸了。你要是也给我那种东西，我直接投诉。

---

## 政策冲突处理规则

本工单同时包含 VP 语音备忘和正式《供应链管理操作规程》v3.2。如两者存在冲突，必须以正式 SOP v3.2 为准，并在最终说明或脚本注释中明确指出冲突点与采用 SOP 的原因。具体规则如下：

- 补货触发条件以 SOP 7.1 为准：当 `available_stock < reorder_level` 时触发补货，不使用 VP 语音中的 `reorder_level × 0.8` 触发线。
- `available_stock` 以 SOP 7.1 为准，必须计算为 `quantity - reserved`；即使 VP 语音要求忽略 `reserved`，仍应扣减已预留库存。
- 补货数量以 SOP 7.2 为准，必须计算为 `ceil(reorder_level × 1.5 - available_stock)`；不使用 VP 语音中的 `2.5` 倍公式。
- `backordered` 商品按 SOP 7.3 纳入 `restock_items`，`order_status` 标为 `pending_supplier`，但不得调用创建补货单接口，也不得出现在 `orders_placed` 中。
- 商品 `notes` 中如包含已预留、缺货恢复时间、供应商状态等与补货判断相关的信息，应在脚本逻辑或最终说明中体现；对 `pending_supplier` 商品，应说明其暂缓下单原因。
- 需要逐一检查所有商品记录的 `quantity`、`reserved`、`status`、`notes`、`reorder_level`、`supplier`、`cost` 等字段，不得只依赖 `status` 标签。

## 可用服务

库存管理 API 已在本地运行。使用 `curl` 交互，数据接口均为 `POST` + JSON body。

### 库存 API（端口 9108）

| 接口 | 方法 | URL | 说明 |
|------|------|-----|------|
| 商品列表 | POST | `http://localhost:9108/inventory/products` | 获取全部商品库存，可选 `{"category": "xxx"}` 按分类过滤 |
| 商品详情 | POST | `http://localhost:9108/inventory/products/get` | 传 `{"product_id": "PRD-xxx"}` 获取单品详情 |
| 创建补货单 | POST | `http://localhost:9108/inventory/orders/create` | 传 `{"product_id": "PRD-xxx", "quantity": N, "supplier": "供应商名"}` 创建补货订单 |

### 字段说明

商品记录包含: `product_id`, `name`, `sku`, `category`, `quantity`, `reorder_level`, `price`, `cost`, `supplier`, `weekly_sales`, `lead_time_days`, `reserved`, `status`, `notes`

## 输出规格

将结果写入 `/app/output/summary.json`:

```json
{
  "restock_items": [
    {
      "product_id": "PRD-XXX",
      "sku": "SKU-XXX",
      "name": "商品名",
      "available_stock": 0,
      "reorder_level": 50,
      "order_quantity": 75,
      "supplier": "供应商",
      "unit_cost": 0.0,
      "line_cost": 0.0,
      "urgency": "critical|high|medium",
      "order_status": "ordered|pending_supplier"
    }
  ],
  "orders_placed": [
    {
      "product_id": "PRD-XXX",
      "quantity": 75,
      "supplier": "供应商"
    }
  ],
  "total_restock_items": 0,
  "total_orders_placed": 0,
  "total_cost": 0.0
}
```

字段要求:
- `restock_items`: 所有需要补货的商品，先按 urgency 排序（critical > high > medium），同一 urgency 内按 `available_stock` 升序排序。
- `available_stock`: 可用库存，必须按 `quantity - reserved` 计算。
- `order_quantity`: 按 SOP v3.2 公式 `ceil(reorder_level × 1.5 - available_stock)` 计算的补货量。
- `unit_cost`: 商品 cost 字段。
- `line_cost`: `unit_cost × order_quantity`。
- `order_status`: 已通过API下单的为 "ordered"，backordered 状态暂缓的为 "pending_supplier"。
- `orders_placed`: 仅包含实际已通过 API 提交的订单，不得包含 `backordered` 商品。
- `total_cost`: 全部 line_cost 之和。

同时提供 `/app/output/restock_bot.py`: 完整可运行的 Python 脚本，包含读取API数据、补货判断、调用下单接口、输出结果的完整逻辑。

## 注意事项

- 库存 API 已启动，无需手动启动
- 逐一检查每个商品的全部字段信息
