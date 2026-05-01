# Quadrature rule optimization

## Problem

Numerical integration is useful only when the rule is stable enough to trust and
small enough to inspect. This result asks whether an evaluation-driven loop can
improve a compact one-dimensional quadrature rule against a frozen suite of
analytic integrands.

## Evaluation

Every candidate is scored by the same evaluation contract. The objective is
lower-is-better and combines integration error across the public integrand
suite. A candidate is accepted only when it improves the measured objective
under that unchanged contract.

## Result

The seed objective was 688.676231. The accepted result reached
114.514813, a reduction of 574.161418
objective units (83.371749%).

## What changed

The accepted rule changes the placement and weighting of the quadrature nodes.
The public trace keeps the curated sequence of accepted states so the improvement
can be inspected without exposing non-public proposal context or uncurated
intermediate material.

## Limitations

This is a bounded numerical benchmark, not a universal integration method. The
result should be interpreted against the frozen integrand suite and evaluation
contract included with this bundle.

## Reproducibility

The bundle includes the accepted candidate, the evaluation contract, metrics, a
sanitized evolution trace, and provenance. Replaying the result should use the
same contract and objective direction: lower is better.
