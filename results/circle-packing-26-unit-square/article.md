# 26-circle unit-square packing

{{visual:history-ledger}}

## Abstract

We study the placement of 26 independently sized circles in the unit square while maximizing their total radius. The headline is not one naked score: **Evölther 2.0 publishes three independently replayable certificates for three non-interchangeable feasibility contracts**—\(\tau=10^{-6}\), \(10^{-10}\), and \(0\). Each ranks first among the complete public witnesses in the manifested corpus that are valid under the same exact-rational contract.

For the strict problem, the finite-decimal witness has total radius

$$
2.6359830849176077831865694854434817303966767982744748577457711298607038493344723396767997365079.
$$

An exact rational interval certificate additionally proves that the nearby real 78-contact configuration is a **strict local maximizer**. This is a tolerance-aware reproducibility result and a local theorem—not a proof of global optimality or a new universal packing record.

## 1. One geometry, three numerical problems

For centers \((x_i,y_i)\) and radii \(r_i>0\), maximize

$$
f(x)=\sum_{i=0}^{25}r_i
$$

subject to four wall constraints per circle and one non-overlap constraint per pair. The model therefore contains 78 continuous variables and 429 geometric inequalities: 104 wall decisions and 325 pair decisions. Including radius positivity, every certificate makes 455 exact decisions.

{{visual:packing-primer}}

A tolerance \(\tau\) changes the feasible set. Wall gaps may be as low as \(-\tau\), while a pair must satisfy

$$
(x_i-x_j)^2+(y_i-y_j)^2\geq(r_i+r_j-\tau)^2
$$

whenever \(r_i+r_j-\tau>0\). Consequently, a larger score at \(10^{-6}\) cannot be presented as an improvement over a strict \(\tau=0\) witness. It solves a different numerical contract.

{{visual:tolerance-contracts}}

The relaxed certificates consume their declared tolerance and fail when rechecked at zero. The strict CSV was formed by rounding a high-precision contact root to 90 decimal places and reducing every radius by approximately \(10^{-75}\). That tiny inward movement turns the serialized decimal geometry into an exact feasible rational lower bound.

{{visual:tolerance-layouts}}

The three drawings appear almost identical because their differences are smaller than the plotted line width. The contract and verifier—not the image—determine which result is valid.

## 2. Where each result stands

We authenticated nine upstream artifacts and evaluated ten complete public witnesses. Every numeric token was retained as a decimal string and reevaluated as a rational number under all three contracts. Downloaded programs and notebooks were parsed as data rather than executed; mutable sources were hash-pinned and fail closed if their contents drift.

{{visual:tolerance-rankings}}

Evölther 2.0 is the highest-scoring valid witness in the explicit manifested corpus for each matching contract. **At \(\tau=10^{-6}\)**, 2.63599872089287514 ranks above the other complete witnesses admitted by that relaxed contract. **At \(\tau=10^{-10}\)**, 2.63598308647338795 ranks first in the stricter relaxed panel. **At \(\tau=0\)**, 2.635983084917607783… ranks first among the strict exact-rational witnesses acquired in the audit.

This is the reproducible meaning of “best” on this page: **best exact-rationally reevaluated witness in the manifested public corpus under the same tolerance**. It is not an exhaustive world ranking. Reported values without a complete downloadable witness—such as Numaro and HELIX at the snapshot date—remain outside the computed ranking.

## 3. How the exact score is computed

Each CSV row contains \(x_i\), \(y_i\), and \(r_i\) as finite decimal strings. Python's `Decimal` parser and `Fraction` convert them into exact rationals. The score is then the rational sum of the 26 radii; no binary floating-point value participates in acceptance.

For each circle the verifier computes \(x_i-r_i\), \(1-x_i-r_i\), \(y_i-r_i\), and \(1-y_i-r_i\). For every pair it computes the squared distance and compares it with the squared tolerance-adjusted radius sum. This is the core of the published verifier:

{{visual:implementation-code}}

The strict certificate passes 455/455 decisions. Its smallest zero-tolerance wall gap is approximately \(1.0\times10^{-75}\), and its smallest squared pair gap is approximately \(6.46\times10^{-76}\). Square roots are used only for readable diagnostics, never for pass/fail.

{{visual:exact-readout}}

## 4. From a feasible CSV to a local theorem

Exact feasibility proves that one serialized witness is valid. The stronger mathematical result concerns the nearby real contact root. The strict witness identifies 78 active constraints—58 circle-circle contacts and 20 wall contacts—which match the 78 variables.

{{visual:contact-graph}}

Let \(g:\mathbb{R}^{78}\to\mathbb{R}^{78}\) collect those active polynomial gaps. The certificate proceeds in four auditable steps:

**Step 1 — isolate the root.** A rational Krawczyk operator proves that a box of radius \(10^{-90}\) contains exactly one root \(x^*\) of \(g(x)=0\). Its maximum inclusion ratio and contraction bound are both below \(8.552\times10^{-15}\).

**Step 2 — preserve feasibility.** Every one of the 351 inactive geometric constraints remains strictly feasible throughout that box; the smallest certified inactive polynomial gap is greater than 0.0071877548.

**Step 3 — certify stationarity.** A second rational Krawczyk calculation encloses the KKT multipliers. All 78 multipliers are positive, with the smallest greater than 0.0208256021.

**Step 4 — conclude locally.** Because the active gradients form a basis, the active gaps are local coordinates. With positive multipliers, every nonzero feasible nearby gap direction strictly decreases the total radius. Therefore \(x^*\) is a strict local maximum.

{{visual:local-proof}}

The real root is enclosed between 2.6359830849176077831865694854434817303966767982744 and 2.6359830849176077831865694854434817303966767982745 in total radius. It lies slightly above the deliberately shrunken CSV witness; the two objects should not be conflated.

## 5. What changed from the earlier result

The historical Evölther reconstruction printed 2.6359830849768984 under binary64 arithmetic, but its minimum numerical slack was negative. It remains valuable as a search checkpoint, not as a strict certificate. Evölther 2.0 separates search from publication: first propose a high-quality contact geometry, then publish independent witnesses for named contracts and prove what can actually be established.

{{visual:precision-comparison}}

The advance is therefore not merely a few more decimals. It is the transition from an attractive numerical output to a claim with explicit scope: three contract-specific corpus leaders, an exact strict witness, and a computer-assisted proof of strict local optimality for the nearby contact root.

## 6. Reproducibility and limits

The public artifact includes the three CSV certificates, exact-rational verifier, hash-authenticated source manifest, generated audit tables, contact system, interval certificate, and deterministic publication build. Version 1.2.1 passes 39/39 tests and the four-document publication gate. The verification path uses only the Python standard library.

```text
python3 scripts/verifier.py
python3 scripts/prove_local_optimum.py --verify-only
```

The audit is frozen to its manifested corpus and snapshot. It does not certify that no stronger unpublished or unacquired witness exists. The interval argument proves a strict local maximum for one 78-contact root, not global optimality over every 26-circle topology.

Read the [technical repository](https://github.com/juan-fernandez-gotherlabs/circle-packing-tolerance-audit), the [v1.2.1 release](https://github.com/juan-fernandez-gotherlabs/circle-packing-tolerance-audit/releases/tag/v1.2.1), or the archived artifact at [Zenodo](https://doi.org/10.5281/zenodo.22060172).
