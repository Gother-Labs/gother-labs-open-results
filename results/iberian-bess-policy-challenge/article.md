# Iberian BESS Policy Challenge

## Problem

This result evaluates a single 1 MW / 4 MWh battery trading frozen OMIE day-ahead price scenarios. The policy decides hourly charge and discharge while respecting power, state-of-charge, efficiency, and terminal SOC constraints.

## Evaluation Contract

The public benchmark is the Iberian BESS Policy Challenge v0.1. It compares the accepted policy against commercial baselines and a perfect-foresight LP upper bound. The oracle is not a sales baseline; it is the remaining headroom under the same simplified physical model.

## Result

The seed quantile baseline scored 72.544043. The accepted policy portfolio scored 48.086813, a reduction of 24.45723 score units (33.71363%).

The accepted policy produced 20.197299 EUR/day average uplift against the quantile comparison baseline, with 0.0 constraint breaches and a downside rate of 0.0.

## What Changed

The accepted policy is a small deterministic portfolio. It evaluates several valid dispatch heuristics on the same daily price horizon and selects the highest-margin valid plan. This is intentionally simple: the pre-sell point is not to replace a client optimizer, but to show that an offline policy challenger can find auditable improvement candidates under a fixed contract.

## Tail Behavior

The comparison bundle keeps every scenario visible, including stress-tail days and weaker cases. The public claim uses aggregate uplift together with p5/p95 uplift, regret, cycle-adjusted margin, and constraint health.

## Limitations

This is an offline day-ahead benchmark over frozen scenarios. It is not production trading, not a live bidding system, not an official market benchmark, and does not model intraday, reserves, imbalance settlement, taxes, grid constraints, or portfolio effects.

## Reproducibility

The bundle includes the accepted candidate, evaluation contract, comparison rows, dispatch trace, replay data, forecast-error smoke output, metrics, score trace, and provenance. Public-claim guardrails validate that required artifacts exist, constraints are clean, limitations are stated, and replay evidence is present.
