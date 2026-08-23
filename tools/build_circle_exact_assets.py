#!/usr/bin/env python3
"""Regenerate and validate the canonical Circle Packing evidence reports."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "results" / "circle-packing-26-unit-square" / "artifacts"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    verifier = load_module("circle_tolerance_verifier", ARTIFACTS / "verifier.py")
    local_proof = load_module("circle_local_proof", ARTIFACTS / "prove_local_optimum.py")

    verification = verifier.verify_repository(write=True)
    interval_report = local_proof.proof()
    (ARTIFACTS / "local_optimum_interval.json").write_text(
        json.dumps(interval_report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    if verification["status"] != "PASS" or interval_report["status"] != "PASS":
        raise SystemExit("Circle Packing evidence regeneration failed")
    print("Regenerated exact feasibility and strict local-optimum reports")


if __name__ == "__main__":
    main()
