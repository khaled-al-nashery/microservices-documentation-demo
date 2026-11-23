#!/usr/bin/env python3
"""Validate the order-service OpenAPI contract and its example payload.

Runs a structural check (no network, no jsonschema dep): confirms the spec
version/info/paths/schemas are present and that the example response matches
the Order schema (required fields, enum, minimum quantity).
"""
import json
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SERVICE = ROOT / "order-service"
ERRORS = 0


def ok(msg: str) -> None:
    print(f"  OK  {msg}")


def fail(msg: str) -> None:
    global ERRORS
    ERRORS += 1
    print(f"  FAIL {msg}")


def main() -> None:
    spec = yaml.safe_load((SERVICE / "contracts" / "openapi.yaml").read_text(encoding="utf-8"))

    print("== OpenAPI structural validation ==")
    if str(spec.get("openapi", "")).startswith("3."):
        ok(f"openapi version {spec['openapi']}")
    else:
        fail(f"openapi version missing/invalid: {spec.get('openapi')!r}")

    info = spec.get("info", {})
    ok(f"info.title = {info['title']!r}") if info.get("title") else fail("info.title missing")
    ok(f"info.version = {info['version']!r}") if info.get("version") else fail("info.version missing")

    paths = spec.get("paths", {})
    ok(f"paths: {len(paths)} endpoints -> {', '.join(paths)}") if paths else fail("paths missing")

    schemas = spec.get("components", {}).get("schemas", {})
    ok(f"components.schemas: {', '.join(schemas)}") if schemas else fail("components.schemas missing")

    print("\n== Example vs schema ==")
    example = json.loads((SERVICE / "examples" / "get-order-response.json").read_text(encoding="utf-8"))
    order = schemas.get("Order", {})
    required = order.get("required", [])
    props = order.get("properties", {})

    missing = [r for r in required if r not in example]
    if missing:
        for m in missing:
            fail(f"example missing required field: {m}")
    else:
        ok(f"example has all required fields: {', '.join(required)}")

    status_enum = props.get("status", {}).get("enum", [])
    if example.get("status") in status_enum:
        ok(f"status {example['status']!r} is a valid enum value")
    else:
        fail(f"status {example.get('status')!r} not in enum {status_enum}")

    items = example.get("items", [])
    item_schema = schemas.get("OrderItem", {})
    item_required = item_schema.get("required", [])
    qty_min = item_schema.get("properties", {}).get("quantity", {}).get("minimum", 0)
    item_errors = 0
    for i, it in enumerate(items):
        imissing = [r for r in item_required if r not in it]
        if imissing:
            item_errors += 1
            fail(f"item[{i}] missing: {imissing}")
        elif it.get("quantity", 0) < qty_min:
            item_errors += 1
            fail(f"item[{i}] quantity {it.get('quantity')} < minimum {qty_min}")
    if item_errors == 0:
        ok(f"items: {len(items)} valid (required={item_required}, quantity>={qty_min})")

    print()
    if ERRORS:
        print(f"RESULT: FAIL ({ERRORS} error(s))")
        sys.exit(1)
    print("RESULT: PASS — contract and example are consistent")


if __name__ == "__main__":
    main()
