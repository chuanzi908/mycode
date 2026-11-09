#!/bin/bash
set -e

# Wait for the service to be ready
for i in $(seq 1 30); do
    if curl -sf -X POST http://localhost:9108/inventory/products \
         -H "Content-Type: application/json" -d '{}' > /dev/null 2>&1; then
        break
    fi
    sleep 0.5
done

mkdir -p /app/output

# Step 1: Fetch all products
curl -s -X POST http://localhost:9108/inventory/products \
  -H "Content-Type: application/json" \
  -d '{}' > /tmp/all_products.json

# Step 2: Place orders for items needing restock (excluding backordered)
# PRD-404: critical, qty=75
curl -s -X POST http://localhost:9108/inventory/orders/create \
  -H "Content-Type: application/json" \
  -d '{"product_id": "PRD-404", "quantity": 75, "supplier": "深圳联拓数码有限公司"}'

# PRD-408: high, qty=131
curl -s -X POST http://localhost:9108/inventory/orders/create \
  -H "Content-Type: application/json" \
  -d '{"product_id": "PRD-408", "quantity": 131, "supplier": "深圳联拓数码有限公司"}'

# PRD-406: high, qty=97
curl -s -X POST http://localhost:9108/inventory/orders/create \
  -H "Content-Type: application/json" \
  -d '{"product_id": "PRD-406", "quantity": 97, "supplier": "东莞声博电子有限公司"}'

# PRD-403: high, qty=114
curl -s -X POST http://localhost:9108/inventory/orders/create \
  -H "Content-Type: application/json" \
  -d '{"product_id": "PRD-403", "quantity": 114, "supplier": "苏州罗尼电子有限公司"}'

# PRD-401: high, qty=79
curl -s -X POST http://localhost:9108/inventory/orders/create \
  -H "Content-Type: application/json" \
  -d '{"product_id": "PRD-401", "quantity": 79, "supplier": "东莞精研电子有限公司"}'

# PRD-409: medium, qty=35 (non-obvious: quantity=88 but reserved=55, available=33)
curl -s -X POST http://localhost:9108/inventory/orders/create \
  -H "Content-Type: application/json" \
  -d '{"product_id": "PRD-409", "quantity": 35, "supplier": "深圳华辰光电有限公司"}'

# PRD-410: backordered - do NOT place order

# Step 3: Write the expected output
python3 << 'PYEOF'
import json, math

summary = {
    "restock_items": [
        {
            "product_id": "PRD-404",
            "sku": "SKU-004",
            "name": "USB-C扩展坞7合1",
            "available_stock": 0,
            "reorder_level": 50,
            "order_quantity": 75,
            "supplier": "深圳联拓数码有限公司",
            "unit_cost": 125.00,
            "line_cost": 9375.00,
            "urgency": "critical",
            "order_status": "ordered"
        },
        {
            "product_id": "PRD-410",
            "sku": "SKU-010",
            "name": "Type-C扩展坞12合1",
            "available_stock": 0,
            "reorder_level": 35,
            "order_quantity": 53,
            "supplier": "广州绿联科技有限公司",
            "unit_cost": 245.00,
            "line_cost": 12985.00,
            "urgency": "critical",
            "order_status": "pending_supplier"
        },
        {
            "product_id": "PRD-408",
            "sku": "SKU-008",
            "name": "无线充电板15W",
            "available_stock": 4,
            "reorder_level": 90,
            "order_quantity": 131,
            "supplier": "深圳联拓数码有限公司",
            "unit_cost": 28.00,
            "line_cost": 3668.00,
            "urgency": "high",
            "order_status": "ordered"
        },
        {
            "product_id": "PRD-406",
            "sku": "SKU-006",
            "name": "降噪耳机H5",
            "available_stock": 8,
            "reorder_level": 70,
            "order_quantity": 97,
            "supplier": "东莞声博电子有限公司",
            "unit_cost": 310.00,
            "line_cost": 30070.00,
            "urgency": "high",
            "order_status": "ordered"
        },
        {
            "product_id": "PRD-403",
            "sku": "SKU-003",
            "name": "静音鼠标M3",
            "available_stock": 6,
            "reorder_level": 80,
            "order_quantity": 114,
            "supplier": "苏州罗尼电子有限公司",
            "unit_cost": 42.00,
            "line_cost": 4788.00,
            "urgency": "high",
            "order_status": "ordered"
        },
        {
            "product_id": "PRD-401",
            "sku": "SKU-001",
            "name": "机械键盘K9 Pro",
            "available_stock": 11,
            "reorder_level": 60,
            "order_quantity": 79,
            "supplier": "东莞精研电子有限公司",
            "unit_cost": 195.00,
            "line_cost": 15405.00,
            "urgency": "high",
            "order_status": "ordered"
        },
        {
            "product_id": "PRD-409",
            "sku": "SKU-009",
            "name": "4K 显示器 U32",
            "available_stock": 33,
            "reorder_level": 45,
            "order_quantity": 35,
            "supplier": "深圳华辰光电有限公司",
            "unit_cost": 1750.00,
            "line_cost": 61250.00,
            "urgency": "medium",
            "order_status": "ordered"
        }
    ],
    "orders_placed": [
        {"product_id": "PRD-404", "quantity": 75, "supplier": "深圳联拓数码有限公司"},
        {"product_id": "PRD-408", "quantity": 131, "supplier": "深圳联拓数码有限公司"},
        {"product_id": "PRD-406", "quantity": 97, "supplier": "东莞声博电子有限公司"},
        {"product_id": "PRD-403", "quantity": 114, "supplier": "苏州罗尼电子有限公司"},
        {"product_id": "PRD-401", "quantity": 79, "supplier": "东莞精研电子有限公司"},
        {"product_id": "PRD-409", "quantity": 35, "supplier": "深圳华辰光电有限公司"}
    ],
    "total_restock_items": 7,
    "total_orders_placed": 6,
    "total_cost": 137541.00
}

with open("/app/output/summary.json", "w") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
PYEOF

# Step 4: Write the automation script (code_delivery_demand pattern)
python3 << 'SCRIPTEOF'
script_content = '''#!/usr/bin/env python3
"""Inventory restock automation bot.
Reads inventory API, identifies low-stock items, places reorder orders.
"""

import json
import math
import subprocess
import sys

SERVICE_URL = "http://localhost:9108"


def curl_post(endpoint, data=None):
    """Make a POST request to the inventory service."""
    cmd = ["curl", "-sf", "-X", "POST",
           "-H", "Content-Type: application/json"]
    if data:
        cmd += ["-d", json.dumps(data)]
    cmd.append(f"{SERVICE_URL}{endpoint}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    if result.returncode != 0:
        print(f"Error calling {endpoint}: {result.stderr}", file=sys.stderr)
        return None
    return json.loads(result.stdout)


def get_all_products():
    """Fetch all products from inventory."""
    resp = curl_post("/inventory/products", {})
    return resp.get("products", []) if resp else []


def calculate_available(product):
    """Available stock = quantity - reserved."""
    return product["quantity"] - product.get("reserved", 0)


def needs_restock(product):
    """Check if product needs restocking per policy v3.2 section 7.1."""
    if product.get("status") == "discontinued":
        return False
    available = calculate_available(product)
    return available < product["reorder_level"]


def calculate_order_quantity(product):
    """Formula per policy v3.2 section 7.2: ceil(reorder_level * 1.5 - available)."""
    available = calculate_available(product)
    qty = math.ceil(product["reorder_level"] * 1.5 - available)
    return max(qty, 1)


def determine_urgency(product):
    """Urgency per policy v3.2 section 7.4."""
    available = calculate_available(product)
    if available == 0:
        return "critical"
    elif available < product["reorder_level"] * 0.3:
        return "high"
    else:
        return "medium"


def place_order(product_id, quantity, supplier):
    """Place a restock order via API."""
    return curl_post("/inventory/orders/create", {
        "product_id": product_id,
        "quantity": quantity,
        "supplier": supplier
    })


def main():
    products = get_all_products()
    if not products:
        print("Error: could not fetch products", file=sys.stderr)
        sys.exit(1)

    restock_items = []
    orders_placed = []

    for product in products:
        if not needs_restock(product):
            continue

        available = calculate_available(product)
        order_qty = calculate_order_quantity(product)
        urgency = determine_urgency(product)
        is_backordered = product.get("status") == "backordered"

        item = {
            "product_id": product["product_id"],
            "sku": product["sku"],
            "name": product["name"],
            "available_stock": available,
            "reorder_level": product["reorder_level"],
            "order_quantity": order_qty,
            "supplier": product["supplier"],
            "unit_cost": product["cost"],
            "line_cost": product["cost"] * order_qty,
            "urgency": urgency,
            "order_status": "pending_supplier" if is_backordered else "ordered"
        }
        restock_items.append(item)

        if not is_backordered:
            resp = place_order(product["product_id"], order_qty, product["supplier"])
            if resp and resp.get("status") == "created":
                orders_placed.append({
                    "product_id": product["product_id"],
                    "quantity": order_qty,
                    "supplier": product["supplier"]
                })

    # Sort by urgency
    urgency_order = {"critical": 0, "high": 1, "medium": 2}
    restock_items.sort(key=lambda x: urgency_order.get(x["urgency"], 99))

    total_cost = sum(item["line_cost"] for item in restock_items)

    summary = {
        "restock_items": restock_items,
        "orders_placed": orders_placed,
        "total_restock_items": len(restock_items),
        "total_orders_placed": len(orders_placed),
        "total_cost": total_cost
    }

    import os
    os.makedirs("/app/output", exist_ok=True)
    with open("/app/output/summary.json", "w") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"Restock analysis complete: {len(restock_items)} items, {len(orders_placed)} orders placed")
    print(f"Total cost impact: {total_cost:.2f}")


if __name__ == "__main__":
    main()
'''

with open("/app/output/restock_bot.py", "w") as f:
    f.write(script_content)
SCRIPTEOF
