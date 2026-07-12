# Iberian BESS Policy Challenge

## Abstract

This result presents a replayable offline challenger for Iberian BESS dispatch. A deterministic policy portfolio is evaluated against frozen OMIE day-ahead scenarios, a commercial quantile baseline, and a perfect-foresight upper bound under one explicit battery contract.

The accepted policy reduces the published weighted euro-like score from a 72.544043 quantile-dispatch baseline to 48.086813 while preserving zero constraint breaches. That is an absolute delta of 24.457230 score units and a 33.71363% relative reduction. The claim is intentionally bounded: this is evidence that Göther Labs can produce auditable improvement candidates and stress-case readouts for optimizer teams, not evidence of live trading readiness.

## 1. Problem formulation

This result evaluates a single 1 MW / 4 MWh battery trading frozen OMIE day-ahead price scenarios. The policy decides hourly charge and discharge while respecting power, state-of-charge, efficiency, and terminal SOC constraints.

The pre-sell question is deliberately narrow: can a replayable challenger discover an auditable improvement candidate against a commercial dispatch baseline, while keeping every constraint and weak case visible? The result should be read as a professional offline benchmark, not as a claim about live bidding or a replacement for a client optimizer.

{{visual:benchmark-readout}}

## 2. Optimizer team readout

This result is designed to answer the questions a battery optimizer team will ask before trusting a challenger: whether the baseline is explicit, whether the improvement survives replay, whether weak cases remain visible, and whether the evidence is tied to public artifacts.

{{visual:customer-readout}}

## 3. Evaluation contract

The public benchmark is the Iberian BESS Policy Challenge v0.1. It compares the accepted policy against commercial baselines and a perfect-foresight LP upper bound. The oracle is not a sales baseline; it is the remaining headroom under the same simplified physical model.

{{visual:contract-table}}

## 4. Commercial baseline result

The seed quantile baseline scored 72.544043. The accepted policy portfolio scored 48.086813, a reduction of 24.45723 score units (33.71363%).

Across the eight frozen scenarios for the single 1 MW / 4 MWh battery, the accepted policy produced 20.197299 EUR/day mean gross simulated dispatch-profit uplift against the quantile comparison baseline, with 0.0 constraint breaches and a downside rate of 0.0. This uplift is before the degradation-cost proxy; the cycle-adjusted margin reports that proxy separately. The benchmark excludes intraday and reserve revenues, imbalance settlement, taxes, grid and portfolio effects, and production bidding constraints.

{{visual:commercial-readout}}

{{visual:scenario-table}}

## 5. Accepted policy

The accepted policy is a small deterministic portfolio. It evaluates several valid dispatch heuristics on the same daily price horizon and selects the highest-margin valid plan. This is intentionally simple: the pre-sell point is not to replace a client optimizer, but to show that an offline policy challenger can find auditable improvement candidates under a fixed contract.

{{visual:implementation-code}}

{{visual:objective-curve}}

## 6. Tail behavior

The comparison bundle keeps every scenario visible, including stress-tail days and weaker cases. The public claim uses aggregate uplift together with p5/p95 uplift, regret, cycle-adjusted margin, and constraint health.

{{visual:dispatch-readout}}

{{visual:robustness-table}}

## 7. Limitations

This is an offline day-ahead benchmark over frozen scenarios. It is not production trading, not a live bidding system, not an official market benchmark, and does not model intraday, reserves, imbalance settlement, taxes, grid constraints, or portfolio effects.

## 8. Reproducibility

The bundle includes the accepted candidate, evaluation contract, comparison rows, dispatch trace, replay data, forecast-error smoke output, metrics, score trace, and provenance. A curated run surface is available at [the run page](./run/). It is a presentation layer over the same public artifacts, not a separate result, and excludes non-public operational material.

The source bundle is available in the [Göther Labs results repository](https://github.com/Gother-Labs/gother-labs-results/tree/main/results/iberian-bess-policy-challenge).

## 9. Private challenge

The natural next step is not a generic demo. It is a small private policy challenge using the client's current baseline, approved scenarios, battery contract, and operational guardrails.

{{visual:private-challenge-cta}}
