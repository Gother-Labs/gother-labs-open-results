# Exact 26-circle unit-square packing

[Published article](https://www.gotherlabs.com/results/circle-packing-26-unit-square/) · [Structured metadata](result.json) · [Exact candidate](artifacts/accepted_candidate.py) · [Exact verifier](artifacts/exact_verifier.py) · [Certificate](artifacts/certificate.json)

Evölther 2.0 produces a certified exact total radius of:

```text
2.63598308491760778318656948544348173039667679827447485774577112986070384936047233967679977696814140651626255328163347303631976410259785760429310341594103
```

The geometry contains 26 positive-radius circles inside the unit square. Every coordinate and radius is a canonical decimal string. The verifier parses those strings as rational numbers and checks the sum, 104 boundary inequalities, 325 pairwise squared-distance inequalities, and deterministic certificate hashes without a geometric tolerance.

## Replay

The replay uses only Python's standard library:

```bash
cd results/circle-packing-26-unit-square/artifacts
python3 verify.py
```

Expected identifiers:

```text
payload_digest     sha256:b4cb8e3778d5ee51ea7ce69252f3b675c75d4814736e66d7a064213812388d81
certificate_digest sha256:a447773e2269cdd46dcc07417b978be415a85b061e8b24b0bdedb3aee71bd8e9
```

## What changed

The former public result displayed a binary64 reconstruction at `2.6359830849768984`. Its smallest reported slack was `-3.786615465628529e-11`, so it is now classified as a non-authoritative search checkpoint. The exact result is numerically a little lower, but it is the stronger publication because its feasibility and sum reproduce exactly.

The checkpoint narrative also replaces the old generation-centric story. The public evidence now follows three retained states: exact seed, higher-precision refinement, and published certificate.

## Public standing

Public papers and repositories report AlphaEvolve V2, ThetaEvolve, and TTT-Discover in the same `2.635983` neighborhood. Most provide only six or eight decimal digits. This bundle therefore claims equality at their displayed precision and exact feasibility for our payload, not a strict world record or proof of global optimality. See [reference-comparison.json](artifacts/reference-comparison.json).

## Bundle

- `accepted_candidate.py`: authoritative canonical decimal geometry
- `exact_verifier.py`: exact rational verifier
- `verify.py`: one-command certificate replay
- `certificate.json`: sanitized public certificate
- `replay.json`: exact payload plus display projection
- `evaluation_contract.md`: accepted input and validation rules
- `evolution.json` and `score-trace.json`: accepted evidence checkpoints
- `metrics.json` and `provenance.json`: structured publication facts
- `article.md`: source narrative for the website

The historical animated run is retained for search context. It is not the authority for the exact result.
