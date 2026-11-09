#!/usr/bin/env python3
"""Inventory Restock Bot — reads product data from the inventory API, applies
restock logic per SOP v3.2, places purchase orders, and writes summary.json.

Service: http://localhost:9108
Output: /app/output/summary.json
"""

import json
import math
import os
import sys

import requests

API_BASE = "http://localhost:9108"
OUTPUT_DIR = "/app/output"
SUMMARY_PATH = os.path.join(OUTPUT_DIR, "summary.json")

URGENCY_ORDER = {"critical": 0, "high": 1, "medium": 2}


def fetch_products():
    """Retrieve the full product list from the inventory API."""
    resp = requests.post(
        f"{API_BASE}/inventory/products",
        json={},
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    body = resp.json()
    return body.get("products", [])


def place_order(product_id, quantity, supplier):
    """Submit a purchase order via the inventory API. Returns True on success."""
    resp = requests.post(
        f"{API_BASE}/inventory/orders/create",
        json={
            "product_id": product_id,
            "quantity": quantity,
            "supplier": supplier,
        },
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    body = resp.json()
    return body.get("status") == "created"


def compute_restock(products):
    """Apply restock logic to the product list.

    Returns (restock_items, orders_placed).
    """
    restock_items = []
    orders_placed = []

    for p in products:
        status = p.get("status", "")
        if status == "discontinued":
            continue

        quantity = p.get("quantity", 0)
        reserved = p.get("reserved", 0)
        reorder_level = p.get("reorder_level", 0)
        available_stock = quantity - reserved
        trigger = reorder_level * 0.8

        if available_stock >= trigger:
            continue

        cost = p.get("cost", 0)
        order_quantity = math.ceil(reorder_level * 1.5 - available_stock)

        if available_stock == 0:
            urgency = "critical"
        elif available_stock < reorder_level * 0.3:
            urgency = "high"
        else:
            urgency = "medium"

        line_cost = cost * order_quantity

        item = {
            "product_id": p["product_id"],
            "sku": p["sku"],
            "name": p["name"],
            "available_stock": available_stock,
            "reorder_level": reorder_level,
            "order_quantity": order_quantity,
            "supplier": p["supplier"],
            "unit_cost": cost,
            "line_cost": line_cost,
            "urgency": urgency,
            "order_status": None,
        }

        if status == "backordered":
            item["order_status"] = "pending_supplier"
        else:
            success = place_order(p["product_id"], order_quantity, p["supplier"])
            if success:
                item["order_status"] = "ordered"
                orders_placed.append({
                    "product_id": p["product_id"],
                    "quantity": order_quantity,
                    "supplier": p["supplier"],
                })
            else:
                item["order_status"] = "pending_supplier"

        restock_items.append(item)

    restock_items.sort(key=lambda i: (
        URGENCY_ORDER.get(i["urgency"], 99),
        i["available_stock"],
    ))

    return restock_items, orders_placed


def write_summary(restock_items, orders_placed):
    """Write summary.json to the output directory."""
    total_cost = sum(item["line_cost"] for item in restock_items)

    summary = {
        "restock_items": restock_items,
        "orders_placed": orders_placed,
        "total_restock_items": len(restock_items),
        "total_orders_placed": len(orders_placed),
        "total_cost": total_cost,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    return summary


def main():
    print("=== Inventory Restock Bot ===", flush=True)
    print(f"API: {API_BASE}", flush=True)

    print("Fetching product list...", flush=True)
    products = fetch_products()
    print(f"  Retrieved {len(products)} products", flush=True)

    print("Computing restock requirements...", flush=True)
    restock_items, orders_placed = compute_restock(products)
    print(f"  Items needing restock: {len(restock_items)}", flush=True)
    print(f"  Orders placed via API: {len(orders_placed)}", flush=True)

    print("Writing summary...", flush=True)
    summary = write_summary(restock_items, orders_placed)
    print(f"  Output: {SUMMARY_PATH}", flush=True)
    print(f"  Total cost: {summary['total_cost']}", flush=True)

    for item in restock_items:
        print(
            f"  [{item['urgency']:>8}] {item['sku']} {item['name']} "
            f"| available={item['available_stock']} "
            f"| order={item['order_quantity']} "
            f"| {item['order_status']}",
            flush=True,
        )

    print("Done.", flush=True)


if __name__ == "__main__":
    main()
