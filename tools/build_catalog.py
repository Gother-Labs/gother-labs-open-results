#!/usr/bin/env python3
"""Build or check the deterministic website catalog from validated bundles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

if __package__:
    from .schema_validation import SchemaValidationError, validate_instance
    from .validate_result import ResultValidationError, validate_result
else:
    from schema_validation import SchemaValidationError, validate_instance
    from validate_result import ResultValidationError, validate_result


ROOT = Path(__file__).resolve().parents[1]
CATALOG_SCHEMA_ID = "https://gotherlabs.com/schemas/catalog.schema.json"


class CatalogBuildError(ValueError):
    """Raised when committed result inputs cannot produce a valid catalog."""


def build_catalog(root: Path = ROOT) -> dict[str, Any]:
    root = root.resolve()
    entries: list[dict[str, Any]] = []
    slugs: set[str] = set()
    orders: set[int] = set()

    for result_path in sorted(root.glob("results/*/result.json")):
        result = validate_result(result_path.parent, schema_dir=root / "schemas")
        slug = result["slug"]
        order = result["website"]["order"]
        if slug in slugs:
            raise CatalogBuildError(f"Duplicate result slug: {slug}")
        if order in orders:
            raise CatalogBuildError(f"Duplicate website.order: {order}")
        slugs.add(slug)
        orders.add(order)
        entries.append(result)

    entries.sort(key=lambda item: (item["website"]["order"], item["slug"]))
    catalog = {
        "schema_version": "results-catalog/v2",
        "results": entries,
    }
    try:
        validate_instance(
            catalog,
            schema_id=CATALOG_SCHEMA_ID,
            schema_dir=root / "schemas",
            instance_label="catalog.json",
        )
    except SchemaValidationError as exc:
        raise CatalogBuildError(str(exc)) from exc
    return catalog


def render_catalog(catalog: dict[str, Any]) -> str:
    return json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"


def check_catalog(root: Path = ROOT) -> None:
    expected = render_catalog(build_catalog(root))
    catalog_path = root / "catalog.json"
    try:
        committed = catalog_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise CatalogBuildError("catalog.json is missing; run tools/build_catalog.py") from exc
    if committed != expected:
        raise CatalogBuildError(
            "catalog.json is out of date; run `python3 tools/build_catalog.py` "
            "and commit the result"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail instead of writing when catalog.json differs from validated inputs.",
    )
    args = parser.parse_args()
    try:
        if args.check:
            check_catalog(ROOT)
            print("catalog.json is deterministic and up to date")
            return
        catalog_path = ROOT / "catalog.json"
        catalog_path.write_text(render_catalog(build_catalog(ROOT)), encoding="utf-8")
        print(f"Wrote {catalog_path.relative_to(ROOT)}")
    except (CatalogBuildError, ResultValidationError) as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
