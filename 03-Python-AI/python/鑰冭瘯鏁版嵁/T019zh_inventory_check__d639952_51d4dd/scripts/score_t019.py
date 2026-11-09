#!/usr/bin/env python3
"""T019 库存补货任务 — 独立评分与测试脚本

直接从 fixtures/products.json 计算所有期望值，
验证 summary.json 和 restock_bot.py 的正确性。
无需依赖 mock API 服务，可离线运行。

用法:
  python3 scripts/score_t019.py [--output-dir /app/output]
"""

import ast
import json
import math
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 路径配置
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
FIXTURES_PATH = ROOT / "environment" / "resources" / "fixtures" / "inventory" / "products.json"

DEFAULT_OUTPUT_DIR = ROOT / "environment" / "output"


def load_products():
    with open(FIXTURES_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_output(output_dir):
    path = Path(output_dir) / "summary.json"
    if not path.is_file():
        return None, str(path)
    with open(path, encoding="utf-8") as f:
        return json.load(f), str(path)


def load_bot(output_dir):
    path = Path(output_dir) / "restock_bot.py"
    if not path.is_file():
        return None, str(path)
    with open(path, encoding="utf-8") as f:
        return f.read(), str(path)


# ---------------------------------------------------------------------------
# 从 fixtures 独立计算所有期望值
# ---------------------------------------------------------------------------

def compute_expected(products):
    """根据 SOP v3.2 规则计算所有期望值。"""
    restock_items = []
    excluded_items = []

    for p in products:
        pid = p["product_id"]
        sku = p["sku"]
        qty = p["quantity"]
        reserved = p.get("reserved", 0)
        reorder = p["reorder_level"]
        status = p.get("status", "")

        # SOP 7.1: 可用库存 = quantity - reserved
        available = qty - reserved

        # SOP 7.1: discontinued 不补货
        if status == "discontinued":
            excluded_items.append({"sku": sku, "reason": "discontinued"})
            continue

        # SOP 7.1: 补货触发条件 available < reorder_level
        # 注意: 政策冲突处理规则使用 reorder_level (非 VP 的 0.8x)
        if available >= reorder:
            excluded_items.append({"sku": sku, "reason": f"available({available}) >= reorder({reorder})"})
            continue

        # SOP 7.2: 补货量 = ceil(reorder_level * 1.5 - available)
        order_qty = math.ceil(reorder * 1.5 - available)

        # SOP 7.4: 紧急程度分级
        if available == 0:
            urgency = "critical"
        elif available < reorder * 0.3:
            urgency = "high"
        else:
            urgency = "medium"

        # backordered 处理 (SOP 7.3)
        is_backordered = status == "backordered"
        order_status = "pending_supplier" if is_backordered else "ordered"

        restock_items.append({
            "product_id": pid,
            "sku": sku,
            "name": p["name"],
            "available_stock": available,
            "reorder_level": reorder,
            "order_quantity": order_qty,
            "supplier": p["supplier"],
            "unit_cost": p["cost"],
            "line_cost": p["cost"] * order_qty,
            "urgency": urgency,
            "order_status": order_status,
            "is_backordered": is_backordered,
        })

    # 排序: urgency (critical > high > medium), 同级别按 available_stock 升序
    urgency_order = {"critical": 0, "high": 1, "medium": 2}
    restock_items.sort(key=lambda x: (urgency_order.get(x["urgency"], 99), x["available_stock"]))

    return restock_items, excluded_items


# ---------------------------------------------------------------------------
# 评分函数
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
        print("T019 库存补货任务 — 评分报告")
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
    products = load_products()
    expected_items, excluded = compute_expected(products)
    result = ScoreResult()

    # ===== 1. 文件存在性检查 =====
    output, output_path = load_output(output_dir)
    result.add("文件存在: summary.json", output is not None, output_path)

    bot_code, bot_path = load_bot(output_dir)
    result.add("文件存在: restock_bot.py", bot_code is not None, bot_path)

    if output is None:
        result.add("summary.json 是合法 JSON", False, "文件不存在")
        return result

    result.add("summary.json 是合法 JSON", isinstance(output, dict))

    # ===== 2. JSON 结构检查 =====
    required_keys = {"restock_items", "orders_placed", "total_restock_items",
                     "total_orders_placed", "total_cost"}
    missing = required_keys - set(output.keys())
    result.add("JSON 顶层字段完整", len(missing) == 0, f"缺失: {missing}" if missing else "")

    restock = output.get("restock_items", [])
    orders = output.get("orders_placed", [])

    # ===== 3. 补货商品集合检查 =====
    expected_skus = {i["sku"] for i in expected_items}
    actual_skus = {i.get("sku") for i in restock}
    result.add("补货 SKU 集合正确", actual_skus == expected_skus,
               f"期望 {sorted(expected_skus)}, 实际 {sorted(actual_skus)}")

    excluded_skus = {i["sku"] for i in excluded}
    wrongly_included = actual_skus & excluded_skus
    result.add("不应补货的商品未被包含", len(wrongly_included) == 0,
               f"错误包含: {wrongly_included}" if wrongly_included else "")

    # ===== 4. 数量统计 =====
    result.add("total_restock_items 正确",
               output.get("total_restock_items") == len(restock),
               f"值={output.get('total_restock_items')}, 数组长度={len(restock)}")

    result.add("total_orders_placed 正确",
               output.get("total_orders_placed") == len(orders),
               f"值={output.get('total_orders_placed')}, 数组长度={len(orders)}")

    # ===== 5. 可用库存计算 =====
    for exp in expected_items:
        sku = exp["sku"]
        actual_item = next((i for i in restock if i.get("sku") == sku), None)
        if actual_item is None:
            result.add(f"{sku} 可用库存", False, "商品不在 restock_items 中")
            continue
        result.add(f"{sku} 可用库存={exp['available_stock']}",
                   actual_item.get("available_stock") == exp["available_stock"],
                   f"实际={actual_item.get('available_stock')}")

    # ===== 6. 补货数量计算 (SOP v3.2: ceil(reorder*1.5 - available)) =====
    for exp in expected_items:
        sku = exp["sku"]
        actual_item = next((i for i in restock if i.get("sku") == sku), None)
        if actual_item is None:
            continue
        result.add(f"{sku} 补货量={exp['order_quantity']}",
                   actual_item.get("order_quantity") == exp["order_quantity"],
                   f"公式: ceil({exp['reorder_level']}*1.5-{exp['available_stock']})"
                   f"={exp['order_quantity']}, 实际={actual_item.get('order_quantity')}")

    # ===== 7. 紧急程度分级 =====
    for exp in expected_items:
        sku = exp["sku"]
        actual_item = next((i for i in restock if i.get("sku") == sku), None)
        if actual_item is None:
            continue
        result.add(f"{sku} 紧急程度={exp['urgency']}",
                   actual_item.get("urgency") == exp["urgency"],
                   f"实际={actual_item.get('urgency')}")

    # ===== 8. 排序检查 =====
    urgency_order = {"critical": 0, "high": 1, "medium": 2}
    urgencies = [urgency_order.get(i.get("urgency"), 99) for i in restock]
    result.add("按 urgency 级别排序", urgencies == sorted(urgencies),
               f"urgency 序列: {urgencies}")

    for level in ("critical", "high", "medium"):
        items_in_level = [i for i in restock if i.get("urgency") == level]
        stocks = [i.get("available_stock", 0) for i in items_in_level]
        result.add(f"{level} 级别内按 available_stock 升序",
                   stocks == sorted(stocks),
                   f"stocks={stocks}")

    # ===== 9. 订单状态检查 =====
    ordered_skus = {i.get("sku") for i in orders if "product_id" in i}
    for exp in expected_items:
        sku = exp["sku"]
        actual_item = next((i for i in restock if i.get("sku") == sku), None)
        if actual_item is None:
            continue
        if exp["is_backordered"]:
            result.add(f"{sku} backordered → pending_supplier",
                       actual_item.get("order_status") == "pending_supplier",
                       f"实际={actual_item.get('order_status')}")
        else:
            result.add(f"{sku} 正常 → ordered",
                       actual_item.get("order_status") == "ordered",
                       f"实际={actual_item.get('order_status')}")

    # ===== 10. backordered 商品不出现在 orders_placed =====
    backorder_pids = {exp["product_id"] for exp in expected_items if exp["is_backordered"]}
    order_pids = {o.get("product_id") for o in orders}
    leaked = backorder_pids & order_pids
    result.add("backordered 商品未下单", len(leaked) == 0,
               f"泄露的 PID: {leaked}" if leaked else "")

    # ===== 11. 成本计算 =====
    for exp in expected_items:
        sku = exp["sku"]
        actual_item = next((i for i in restock if i.get("sku") == sku), None)
        if actual_item is None:
            continue
        result.add(f"{sku} unit_cost={exp['unit_cost']}",
                   actual_item.get("unit_cost") == exp["unit_cost"],
                   f"实际={actual_item.get('unit_cost')}")
        result.add(f"{sku} line_cost={exp['line_cost']}",
                   actual_item.get("line_cost") == exp["line_cost"],
                   f"实际={actual_item.get('line_cost')}")

    expected_total = sum(exp["line_cost"] for exp in expected_items)
    actual_total = output.get("total_cost", 0)
    result.add(f"total_cost={expected_total}",
               abs(actual_total - expected_total) < 1,
               f"实际={actual_total}, 差异={abs(actual_total - expected_total)}")

    # ===== 12. 字段完整性 =====
    required_restock_fields = {
        "product_id", "sku", "name", "available_stock", "reorder_level",
        "order_quantity", "supplier", "unit_cost", "line_cost", "urgency",
        "order_status"
    }
    for i, item in enumerate(restock):
        missing_f = required_restock_fields - set(item.keys())
        result.add(f"restock_items[{i}] 字段完整",
                   len(missing_f) == 0,
                   f"SKU={item.get('sku')}, 缺失: {missing_f}" if missing_f else "")

    required_order_fields = {"product_id", "quantity", "supplier"}
    for i, order in enumerate(orders):
        missing_f = required_order_fields - set(order.keys())
        result.add(f"orders_placed[{i}] 字段完整",
                   len(missing_f) == 0,
                   f"缺失: {missing_f}" if missing_f else "")

    # ===== 13. restock_bot.py 质量检查 =====
    if bot_code is not None:
        # 语法检查
        try:
            ast.parse(bot_code)
            result.add("restock_bot.py 语法合法", True)
        except SyntaxError as e:
            result.add("restock_bot.py 语法合法", False, str(e))

        # 无 TODO/FIXME 占位符
        lower = bot_code.lower()
        has_placeholder = any(m in lower for m in ("todo", "fixme", "pass  #", "raise notimplementederror"))
        result.add("restock_bot.py 无占位符", not has_placeholder)

        # 包含关键逻辑
        has_api_call = "localhost:9108" in bot_code or "9108" in bot_code
        result.add("restock_bot.py 包含 API 调用", has_api_call)

        has_formula = "1.5" in bot_code
        result.add("restock_bot.py 使用 SOP 1.5x 公式", has_formula)

        has_reserved = "reserved" in bot_code
        result.add("restock_bot.py 扣减 reserved", has_reserved)
    else:
        result.add("restock_bot.py 语法合法", False, "文件不存在")
        result.add("restock_bot.py 无占位符", False, "文件不存在")

    return result


# ---------------------------------------------------------------------------
# 单元测试: 核心计算逻辑
# ---------------------------------------------------------------------------

def test_available_stock_calculation():
    """测试可用库存计算: quantity - reserved"""
    products = load_products()
    cases = {
        "SKU-001": (11, 0, 11),
        "SKU-003": (6, 0, 6),
        "SKU-004": (0, 0, 0),
        "SKU-005": (230, 10, 220),
        "SKU-006": (14, 6, 8),
        "SKU-008": (4, 0, 4),
        "SKU-009": (88, 55, 33),
        "SKU-010": (0, 0, 0),
    }
    for p in products:
        sku = p["sku"]
        if sku in cases:
            qty, res, exp = cases[sku]
            actual = p["quantity"] - p.get("reserved", 0)
            assert actual == exp, f"{sku}: {p['quantity']}-{p.get('reserved', 0)}={actual}, 期望 {exp}"
    print("  [PASS] 可用库存计算")


def test_restock_formula():
    """测试 SOP v3.2 补货公式: ceil(reorder_level * 1.5 - available)"""
    cases = [
        (60, 11, 79),   # SKU-001
        (80, 6, 114),   # SKU-003
        (50, 0, 75),    # SKU-004
        (70, 8, 97),    # SKU-006
        (90, 4, 131),   # SKU-008
        (45, 33, 35),   # SKU-009
        (35, 0, 53),    # SKU-010
    ]
    for reorder, available, expected in cases:
        actual = math.ceil(reorder * 1.5 - available)
        assert actual == expected, \
            f"ceil({reorder}*1.5-{available})={actual}, 期望 {expected}"
    print("  [PASS] 补货量公式")


def test_urgency_classification():
    """测试紧急程度分级规则"""
    # (available, reorder_level, expected_urgency)
    cases = [
        (0, 50, "critical"),    # SKU-004
        (0, 35, "critical"),    # SKU-010
        (4, 90, "high"),        # SKU-008: 4 < 27 (90*0.3)
        (6, 80, "high"),        # SKU-003: 6 < 24 (80*0.3)
        (8, 70, "high"),        # SKU-006: 8 < 21 (70*0.3)
        (11, 60, "high"),       # SKU-001: 11 < 18 (60*0.3)
        (33, 45, "medium"),     # SKU-009: 33 >= 13.5 (45*0.3)
    ]
    for available, reorder, expected in cases:
        if available == 0:
            actual = "critical"
        elif available < reorder * 0.3:
            actual = "high"
        else:
            actual = "medium"
        assert actual == expected, \
            f"available={available}, reorder={reorder}: {actual}, 期望 {expected}"
    print("  [PASS] 紧急程度分级")


def test_restock_trigger():
    """测试补货触发条件: available < reorder_level"""
    products = load_products()
    should_restock = {"SKU-001", "SKU-003", "SKU-004", "SKU-006", "SKU-008", "SKU-009", "SKU-010"}
    should_not = {"SKU-002", "SKU-005", "SKU-007", "SKU-011", "SKU-012"}

    for p in products:
        sku = p["sku"]
        available = p["quantity"] - p.get("reserved", 0)
        reorder = p["reorder_level"]
        status = p.get("status", "")
        triggered = available < reorder and status != "discontinued"

        if sku in should_restock:
            assert triggered, f"{sku} 应触发补货 (available={available}, reorder={reorder})"
        elif sku in should_not:
            assert not triggered, f"{sku} 不应触发补货 (available={available}, reorder={reorder})"
    print("  [PASS] 补货触发条件")


def test_sku009_trap():
    """测试 SKU-009 数据陷阱: quantity=88 但 reserved=55, available=33 < reorder=45"""
    products = load_products()
    sku009 = next(p for p in products if p["sku"] == "SKU-009")
    available = sku009["quantity"] - sku009["reserved"]
    assert sku009["status"] == "in_stock", "SKU-009 应标记为 in_stock"
    assert available == 33, f"可用库存应为 33, 实际 {available}"
    assert available < sku009["reorder_level"], \
        f"SKU-009 可用库存 {available} < reorder {sku009['reorder_level']}, 应触发补货"
    print("  [PASS] SKU-009 数据陷阱识别")


def test_backordered_handling():
    """测试 backordered 商品处理: 列入清单但不下单"""
    products = load_products()
    sku010 = next(p for p in products if p["sku"] == "SKU-010")
    assert sku010["status"] == "backordered", "SKU-010 应为 backordered"
    assert sku010["quantity"] == 0, "SKU-010 quantity 应为 0"
    available = sku010["quantity"] - sku010.get("reserved", 0)
    assert available < sku010["reorder_level"], "SKU-010 应触发补货"
    print("  [PASS] backordered 商品处理")


def test_total_cost_range():
    """测试总成本在合理范围内"""
    expected_items, _ = compute_expected(load_products())
    total = sum(i["line_cost"] for i in expected_items)
    low, high = 116910, 158172
    assert low <= total <= high, \
        f"total_cost={total} 不在 [{low}, {high}] 范围内"
    print(f"  [PASS] 总成本={total} 在合理范围 [{low}, {high}]")


# ---------------------------------------------------------------------------
# 主程序
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="T019 库存补货评分")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR),
                        help="输出文件目录")
    parser.add_argument("--unit-tests", action="store_true",
                        help="仅运行单元测试")
    args = parser.parse_args()

    print("=" * 70)
    print("T019 库存补货任务 — 评测系统")
    print("=" * 70)

    # 运行单元测试
    print("\n--- 单元测试: 核心计算逻辑 ---")
    test_funcs = [
        test_available_stock_calculation,
        test_restock_formula,
        test_urgency_classification,
        test_restock_trigger,
        test_sku009_trap,
        test_backordered_handling,
        test_total_cost_range,
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
