# Tolerance-aware 26-circle unit-square packing

[Published article](https://www.gotherlabs.com/results/circle-packing-26-unit-square/) · [Structured metadata](result.json) · [Technical repository](https://github.com/juan-fernandez-gotherlabs/circle-packing-tolerance-audit) · [Zenodo](https://doi.org/10.5281/zenodo.22060172)

This Results bundle is the public ledger for the Evölther 2.0 circle-packing result. It keeps three different numerical objects explicitly separate:

1. **Strict finite-decimal witness.** `artifacts/exact.csv` is feasible at zero tolerance and has exact rational total radius:

   ```text
   2.6359830849176077831865694854434817303966767982744748577457711298607038493344723396767997365079
   ```

2. **Real 78-contact root.** `artifacts/local_optimum_interval.json` encloses a nearby real contact configuration whose total radius lies strictly between:

   ```text
   2.6359830849176077831865694854434817303966767982744
   2.6359830849176077831865694854434817303966767982745
   ```

   The interval certificate proves that this root is a strict local maximizer. It is not the deliberately shrunken CSV witness.

3. **Historical floating run.** `run/` preserves the May 2026 Evölther search campaign whose endpoint printed `2.6359830849768984` with negative numerical slack. It is research history, not an accepted feasibility certificate.

## Three contracts

The bundle publishes one finite-decimal certificate for each non-interchangeable contract:

| Contract | Exact-rational score | Status at zero tolerance |
| --- | ---: | --- |
| `1e-6` | `2.63599872089287514` | fails |
| `1e-10` | `2.63598308647338795` | fails |
| `0` | `2.635983084917607783…` | passes |

Each primary certificate checks 104 wall inequalities, 325 pair inequalities, and 26 positive radii: 455 exact decisions. Each matching Evölther 2.0 certificate ranks first among the complete public witnesses admitted by the same rational contract in the corpus frozen on 8 August 2026. This is not an exhaustive world ranking.

## Replay

Both verification paths use only Python's standard library:

```bash
cd results/circle-packing-26-unit-square/artifacts
python3 verifier.py
python3 -S prove_local_optimum.py
```

The first command regenerates `verification.json` from the three CSV files. The second recomputes the rational interval proof from `exact.csv` and `local_optimum_certificate.json` and regenerates `local_optimum_interval.json`.

## Bundle authority

- `publication-manifest.json`: names the strict witness, enclosed root, and historical run without conflating them.
- `tolerance_1e-6.csv`, `tolerance_1e-10.csv`, `exact.csv`: primary certificates.
- `verifier.py`, `verification.json`: exact-rational feasibility replay.
- `local_optimum_certificate.json`, `prove_local_optimum.py`, `local_optimum_interval.json`: strict local-optimum proof.
- `public_corpus_audit.json`: frozen same-contract public comparison.
- `evaluation_contract.md`: mathematical and computational contract.
- `metrics.json`, `provenance.json`: structured publication facts.
- `article.md`: source narrative for the website.

Release v1.2.0 published the mathematical artifact on 9 August 2026. Release v1.2.1, dated 22 August 2026, is the current editorial and citation surface and does not change the certified mathematics. No global optimum or new Packomania record is claimed.
