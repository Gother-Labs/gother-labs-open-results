# Göther Labs Results

## Public evidence for governed technical improvement

This repository is Göther Labs’ public evidence layer for evaluation-driven technical improvement.

Each published result is a bounded, reproducible bundle: it exposes the problem, evaluation contract, accepted candidate, and public artifacts needed to inspect the claim and its limitations.

Public bundles are intentionally sanitized. They exclude private generation context, operational run records, sensitive configuration, and uncurated intermediate material.

Browse the published results at [gotherlabs.com/results](https://www.gotherlabs.com/results/).

This repository is the public editorial and technical source for Göther Labs
results.

Each result lives in `results/<slug>/` and contains:

- `result.json`: structured metadata validated against the public result schema
- `article.md`: editable technical note
- `README.md`: GitHub-rendered article copy with public artifact and figure links
- `artifacts/`: sanitized public artifacts
- `assets/`: public figures used by the website

Internal Evolther runs must be exported through the publication exporter before
they are committed here. Public bundles must not include non-public generation
context, operational run records, sensitive configuration, or uncurated
intermediate material.

The website consumes this repository through `catalog.json`.

Schema identifiers, documentation, tooling, and website routes use “results”
consistently.

```bash
python3 tools/validate_result.py results/quadrature-rule-optimization
python3 tools/build_catalog.py
```
