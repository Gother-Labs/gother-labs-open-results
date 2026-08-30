#!/usr/bin/env python3
"""Local-only JSON Schema loading and actionable validation errors."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


class SchemaValidationError(ValueError):
    """Raised when a schema or instance fails local validation."""


def _reject_nonfinite_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON numeric constant {value}")


def _json_path(parts: Iterable[str | int]) -> str:
    rendered = "$"
    for part in parts:
        if isinstance(part, int):
            rendered += f"[{part}]"
        elif part.isidentifier():
            rendered += f".{part}"
        else:
            rendered += f"[{json.dumps(part, ensure_ascii=False)}]"
    return rendered


@lru_cache(maxsize=None)
def _schema_set(schema_dir_text: str) -> tuple[dict[str, dict[str, Any]], Registry]:
    schema_dir = Path(schema_dir_text)
    schemas: dict[str, dict[str, Any]] = {}
    registry = Registry()

    for schema_path in sorted(schema_dir.glob("*.schema.json")):
        try:
            schema = json.loads(
                schema_path.read_text(encoding="utf-8"),
                parse_constant=_reject_nonfinite_constant,
            )
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            raise SchemaValidationError(f"Cannot load schema {schema_path}: {exc}") from exc

        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            raise SchemaValidationError(f"Invalid JSON Schema {schema_path}: {exc}") from exc

        schema_id = schema.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            raise SchemaValidationError(f"Schema {schema_path} must declare a non-empty $id")
        if schema_id in schemas:
            raise SchemaValidationError(f"Duplicate schema $id {schema_id}")

        schemas[schema_id] = schema
        registry = registry.with_resource(schema_id, Resource.from_contents(schema))

    if not schemas:
        raise SchemaValidationError(f"No *.schema.json files found in {schema_dir}")
    return schemas, registry


def validate_instance(
    instance: Any,
    *,
    schema_id: str,
    schema_dir: Path,
    instance_label: str,
) -> None:
    """Validate an instance using only schemas registered from ``schema_dir``."""

    schemas, registry = _schema_set(str(schema_dir.resolve()))
    try:
        schema = schemas[schema_id]
    except KeyError as exc:
        raise SchemaValidationError(f"Schema $id not registered locally: {schema_id}") from exc

    validator = Draft202012Validator(
        schema,
        registry=registry,
        format_checker=FormatChecker(),
    )
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: (tuple(str(part) for part in error.absolute_path), error.message),
    )
    if not errors:
        return

    details = [
        f"{instance_label} {_json_path(error.absolute_path)}: {error.message}"
        for error in errors
    ]
    raise SchemaValidationError("JSON Schema validation failed:\n" + "\n".join(details))
