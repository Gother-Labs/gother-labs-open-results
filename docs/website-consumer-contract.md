# Website Consumer Contract

Status: `results-catalog/v2`

`catalog.json` is the **only structured result feed** consumed by the Göther Labs website.

## Contract

1. The website reads the committed root [`catalog.json`](../catalog.json).
2. The supported `schema_version` is `results-catalog/v2`; a consumer must reject an unknown version before reading entries.
3. Each item in `results` is one complete `result/v1` object validated against [`result.schema.json`](../schemas/result.schema.json) and the bundle's semantic checks.
4. The website filters entries by `status`, uses the committed array order, and derives article/assets/run locations from the validated `slug` and website paths.
5. The website does **not** scan `results/*`, merge a second metadata document, or treat an individual `result.json` as an alternative feed.

Individual `results/<slug>/result.json` files remain the authoring units. `tools/build_catalog.py` validates them and embeds their complete content into the catalog. The catalog and every referenced public artifact therefore belong to the same Git commit.

## Determinism and provenance

The catalog contains no wall-clock generation timestamp. Its bytes are a pure function of committed schemas and bundles:

- input discovery is lexically sorted;
- output ordering is `website.order`, then `slug`;
- JSON formatting and the final newline are fixed;
- `generated_at` and other environment-dependent values are prohibited by the catalog schema.

Use the repository commit as the publication/version identifier. HTTP or deployment timestamps are transport metadata, not catalog content.

## Publication sequence

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
python3 tools/validate_result.py results/*
python3 tools/build_catalog.py
python3 tools/build_catalog.py --check
```

Commit the bundle and regenerated catalog together. Pull requests and pushes to `main` run the same validation and fail if the committed catalog differs from a clean rebuild.

## Artifact and security boundary

- Declared public files use normalized POSIX paths under the bundle's `artifacts/` or `assets/` directories.
- Absolute paths, parent traversal, backslashes, malformed segments, missing files and symlinks that escape the bundle fail validation.
- JSON Schema references resolve only from the committed `schemas/` directory; validation does not retrieve remote schemas.
- Publication validation does not execute candidate or artifact code.
- Adding a new structural metadata property requires a schema change. Domain-specific metrics remain intentionally extensible under `metrics`.

## Compatibility note

The current website synchronizer already accepts embedded catalog entries: when an entry has no legacy `path`, it uses the catalog object directly. `results-catalog/v2` removes the legacy per-entry `path` and `generated_at` fields so the website has one validated structured surface. The website should add an explicit version guard before claiming strict enforcement of this consumer contract.
