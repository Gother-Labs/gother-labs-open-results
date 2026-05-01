# Storage arbitrage policy

## Problem

Storage arbitrage looks simple until the policy has to respect physical limits,
terminal state-of-charge requirements, and price scenarios that change faster
than a static playbook. This result asks whether an evaluation-driven loop can
improve a deterministic dispatch policy without making the operating behavior
opaque.

## Evaluation

Every candidate is scored under the same frozen contract. The objective is
lower-is-better and combines scenario regret against an oracle with validity
checks for power, state of charge, and terminal constraints. A candidate is
retained only when that objective improves under the unchanged evaluator.

## Result

The seed objective was 73.4941. The accepted policy reached
24.856175, a reduction of 48.637926
objective units (66.179361%).

## What changed

The accepted policy uses a short lookahead average and reintroduces round-trip
efficiency into the spread gate. The result is still deterministic and bounded,
but it reacts to near-term price structure instead of relying only on static
daily quantiles.

## Limitations

This is a bounded public dispatch benchmark, not a market trading system. It is
scored against the frozen scenarios and battery assumptions included in the
evaluation contract.

## Reproducibility

The bundle includes the accepted policy, the evaluation contract, metrics, a
sanitized evolution trace, dispatch traces, and provenance. Replaying the result
should use the same scenario set and objective direction: lower is better.
