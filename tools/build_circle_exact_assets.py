#!/usr/bin/env python3
"""Build replay and SVG evidence for the exact 26-circle result."""

from __future__ import annotations

import importlib.util
import json
import sys
from dataclasses import asdict
from decimal import Decimal, getcontext
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results" / "circle-packing-26-unit-square"
ARTIFACTS = RESULT / "artifacts"
ASSETS = RESULT / "assets"
getcontext().prec = 220


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def write(path: Path, value: str) -> None:
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def build_replay(candidate, verifier) -> dict[str, object]:
    payload = candidate.run_packing_exact()
    verified = verifier.verify_exact_packing(payload)
    centers, radii, projected_sum = candidate.run_packing()
    return {
        "schema_version": "result-replay/v2",
        "valid": True,
        "authority": "exact-rational",
        "exact_payload": payload,
        "certificate": asdict(verified.certificate),
        "trace": {
            "centers": centers,
            "radii": radii,
            "reported_sum": projected_sum,
            "status": "non-authoritative display projection",
        },
    }


def packing_svg(replay: dict[str, object]) -> str:
    trace = replay["trace"]
    left, top, size = 210, 112, 760
    circles = []
    for index, ((x, y), radius) in enumerate(zip(trace["centers"], trace["radii"], strict=True), 1):
        cx = left + float(x) * size
        cy = top + (1 - float(y)) * size
        r = float(radius) * size
        circles.append(
            f'<circle class="disk" cx="{cx:.5f}" cy="{cy:.5f}" r="{r:.5f}"/>'
            f'<text x="{cx:.5f}" y="{cy + 4:.5f}" text-anchor="middle">{index}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 980" role="img" aria-labelledby="title desc">
<title id="title">Evölther 2.0 exact 26-circle packing</title>
<desc id="desc">Display projection of the exact rational packing payload.</desc>
<style>svg{{background:#05070b;color:#f5f7fb;font-family:Inter,Arial,sans-serif}}.frame{{fill:none;stroke:#738096;stroke-width:2}}.grid{{stroke:#18202c;stroke-width:1}}.disk{{fill:#168df0;fill-opacity:.28;stroke:#279dff;stroke-width:2}}text{{fill:#dce5f1;font-size:12px}}.title{{font-size:26px;font-weight:700}}.note{{fill:#96a3b6;font-size:15px}}.value{{fill:#279dff;font-size:22px;font-weight:700}}</style>
<text class="title" x="86" y="52">Certified 26-circle geometry</text>
<text class="note" x="86" y="80">Binary64 display projection · canonical decimal payload is authoritative</text>
<path class="grid" d="M{left} {top + size/2}H{left + size}M{left + size/2} {top}V{top + size}"/>
<rect class="frame" x="{left}" y="{top}" width="{size}" height="{size}"/>
{''.join(circles)}
<text class="value" x="600" y="930" text-anchor="middle">sum radii 2.635983084917607783…</text>
</svg>'''


def objective_svg() -> str:
    seed = Decimal("2.635983084917470548216")
    refined = Decimal("2.63598308491760778318656948544348173039667679827447485774577046285576659")
    final = Decimal("2.63598308491760778318656948544348173039667679827447485774577112986070384936047233967679977696814140651626255328163347303631976410259785760429310341594103")
    gains = [(value - seed) / Decimal("1e-15") for value in (seed, refined, final)]
    points = [(180, 650), (600, 650 - float(gains[1]) * 3.4), (1020, 650 - float(gains[2]) * 3.4)]
    path = " ".join(("M" if i == 0 else "L") + f"{x:.1f},{y:.1f}" for i, (x, y) in enumerate(points))
    labels = ["Exact seed", "Precision refinement", "Published certificate"]
    dots = "".join(
        f'<circle cx="{x}" cy="{y:.1f}" r="8"/><text class="label" x="{x}" y="720" text-anchor="middle">{label}</text><text class="gain" x="{x}" y="{y-22:.1f}" text-anchor="middle">+{gain:.6f}</text>'
        for (x, y), label, gain in zip(points, labels, gains, strict=True)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" role="img" aria-labelledby="title desc">
<title id="title">Accepted exact Circle Packing checkpoints</title>
<desc id="desc">Improvement from exact seed measured in quadrillionths of total radius.</desc>
<style>svg{{background:#05070b;font-family:Inter,Arial,sans-serif}}.axis,.grid{{stroke:#2a3444;stroke-width:1}}.line{{fill:none;stroke:#279dff;stroke-width:4}}circle{{fill:#279dff;stroke:#d8efff;stroke-width:2}}text{{fill:#dce5f1}}.title{{font-size:27px;font-weight:700}}.note,.tick,.label{{fill:#9ba8ba;font-size:15px}}.gain{{fill:#279dff;font-size:17px;font-weight:700}}</style>
<text class="title" x="86" y="58">Accepted exact checkpoints</text>
<text class="note" x="86" y="88">gain from exact-v2 seed · ×10⁻¹⁵ total radius</text>
<path class="axis" d="M120 650H1080M120 140V650"/>
<path class="grid" d="M120 480H1080M120 310H1080M120 140H1080"/>
<text class="tick" x="100" y="656" text-anchor="end">0</text><text class="tick" x="100" y="486" text-anchor="end">50</text><text class="tick" x="100" y="316" text-anchor="end">100</text><text class="tick" x="100" y="146" text-anchor="end">150</text>
<path class="line" d="{path}"/>{dots}
</svg>'''


def certificate_svg(certificate: dict[str, object]) -> str:
    boundary = Decimal(certificate["min_boundary_margin"])
    pair = Decimal(certificate["min_pair_squared_margin"])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 540" role="img" aria-labelledby="title desc">
<title id="title">Exact rational certificate readout</title>
<desc id="desc">Eight checks pass with positive boundary and pairwise margins.</desc>
<style>svg{{background:#05070b;font-family:Inter,Arial,sans-serif}}text{{fill:#dce5f1}}.title{{font-size:27px;font-weight:700}}.label{{fill:#9ba8ba;font-size:15px;letter-spacing:1px;text-transform:uppercase}}.value{{font-size:25px;font-weight:700}}.blue{{fill:#279dff}}.rule{{stroke:#273140}}.hash{{font-family:ui-monospace,SFMono-Regular,monospace;font-size:16px}}</style>
<text class="title" x="86" y="58">Exact rational certificate</text>
<text class="label" x="86" y="122">Contract checks</text><text class="value blue" x="86" y="158">8 / 8 pass</text>
<text class="label" x="420" y="122">Arithmetic</text><text class="value" x="420" y="158">Fractions · no tolerance</text>
<text class="label" x="880" y="122">Precision</text><text class="value" x="880" y="158">256-bit</text>
<path class="rule" d="M86 202H1114"/>
<text class="label" x="86" y="254">Minimum boundary margin</text><text class="value blue" x="86" y="292">{boundary:.4E}</text>
<text class="label" x="650" y="254">Minimum pair² margin</text><text class="value blue" x="650" y="292">{pair:.4E}</text>
<path class="rule" d="M86 338H1114"/>
<text class="label" x="86" y="390">Payload</text><text class="hash" x="86" y="422">b4cb8e3778d5ee51…a064213812388d81</text>
<text class="label" x="650" y="390">Certificate</text><text class="hash" x="650" y="422">a447773e2269cdd4…edb3aee71bd8e9</text>
</svg>'''


def main() -> None:
    candidate = load_module("circle_candidate", ARTIFACTS / "accepted_candidate.py")
    verifier = load_module("circle_verifier", ARTIFACTS / "exact_verifier.py")
    replay = build_replay(candidate, verifier)
    write(ARTIFACTS / "replay.json", json.dumps(replay, indent=2, ensure_ascii=False))
    write(ASSETS / "packing-layout.svg", packing_svg(replay))
    write(ASSETS / "objective-curve.svg", objective_svg())
    write(ASSETS / "contact-readout.svg", certificate_svg(replay["certificate"]))


if __name__ == "__main__":
    main()
