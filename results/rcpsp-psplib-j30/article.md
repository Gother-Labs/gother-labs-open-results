# PSPLIB J30 scheduling benchmark

## Abstract

This note reports a deterministic dispatch rule for the Resource-Constrained Project Scheduling Problem (RCPSP). On a frozen public subset of PSPLIB J30, the accepted score progressed from 14.312 at baseline to 12.087 with Evölther and 10.108 with Evölther 2.0. The current result is a 29.37% reduction from baseline and preserves feasibility on all 80 evaluated instances.

The result history is expressed as accepted checkpoints rather than placed on a synthetic generation axis. The benchmark is deliberately external and bounded: every portfolio instance has a proven optimal makespan, so the score measures schedule quality against a reference optimum rather than machine speed. This is a benchmark result on the fixed portfolio, not a universal scheduling claim.

## 1. Problem formulation

RCPSP schedules activities subject to precedence constraints and renewable-resource limits. An activity may start only after all predecessors finish, and the total demand of concurrently active activities must remain within available capacity. The objective is to minimize the project makespan, the finish time of the terminal activity.

$$
C_{max}(S) = \max_i F_i
$$

where \(F_i\) is the finish time of activity \(i\) in schedule \(S\).

{{visual:rcpsp-primer}}

{{visual:resource-load}}

Figure 2 uses the real j3025_9 schedules reported later. Evölther 2.0 redistributes demand earlier without crossing any of the four unchanged capacity limits, then releases every resource 20 time units sooner. The evaluator still uses serial schedule generation: Evölther changes the priority policy, not the feasibility validator.

## 2. Benchmark and evaluation contract

The public portfolio contains 80 frozen PSPLIB J30 single-mode instances: parameters 1, 7, 13, 19, 25, 31, 37, and 43 crossed with instances 1 through 10. Each instance contains 32 jobs including dummy source and sink activities, renewable-resource capacities, precedence arcs, and a proven optimal makespan.

{{visual:contract-table}}

For instance \(k\), the evaluator computes the makespan gap against the proven optimum:

$$
g_k = 100 \cdot \frac{C_{max,k}^{candidate} - C_{max,k}^{optimal}}{C_{max,k}^{optimal}}.
$$

The retained objective combines mean portfolio quality with a tail-risk term:

$$
score = mean(g_k) + 0.35 \cdot p95(g_k) + feasibility\_penalty.
$$

A candidate must return finite priorities, choose only eligible activities, schedule every activity exactly once, respect all precedences, remain within every resource capacity, and keep the feasibility penalty at zero.

## 3. Accepted candidate

The current Evölther 2.0 candidate keeps the serial schedule generator unchanged and replaces only the deterministic activity-ranking policy. The rule combines structural, timing, contention, and downstream-work signals exposed by the fixed evaluator. It remains an inspectable dispatch heuristic rather than a replacement solver.

{{visual:implementation-code}}

The complete public comparison is [the baseline-to-Evölther 2.0 diff](artifacts/baseline-to-evolther-2.diff). A leave-one-feature-out replay sets each coefficient to zero independently and evaluates all 80 instances. Every ablation worsens the score; the full measurements are in [ablation.json](artifacts/ablation.json).

## 4. Results

The accepted history contains three directly comparable checkpoints under one unchanged, lower-is-better objective.

{{visual:objective-curve}}

{{visual:benchmark-comparison}}

Evölther first reduced the objective by 15.55%. Evölther 2.0 then reduced the previous incumbent by a further 16.37%, reaching a 29.37% reduction from baseline. Mean gap falls from 7.13% at baseline to 5.01%, p95 gap falls from 20.52% to 14.57%, and all 80 schedules remain feasible. Exact optima are 23/80 at baseline, 19/80 for Evölther, and 27/80 for Evölther 2.0.

Against baseline, Evölther 2.0 improves 35 instances, leaves 27 unchanged, and worsens 18. The accepted claim is therefore portfolio-level improvement rather than universal instance dominance.

{{visual:schedule-compression}}

The clearest compression example is j3025_9: baseline makespan 112, Evölther 2.0 makespan 92, and proven optimum 84. The 20-unit reduction removes 71.4% of the baseline gap to optimum. The task-level comparison and resource profiles use the same two deterministic schedules and the same evaluator.

{{visual:portfolio-deltas}}

The complete instance ledger is available in [portfolio-comparison.json](artifacts/portfolio-comparison.json). Most regressions are one or two time units, while the improvement side contains several reductions of eight to ten units and the 20-unit reduction on j3025_9.

{{visual:gap-summary}}

{{visual:tail-ladder}}

The current mean makespan is 5.01% above proven optimum, the p95 gap is 14.57%, and the worst residual gap is 17.11%. These residuals remain part of the public result definition.

## 5. Limitations

This result is limited to the frozen 80-instance PSPLIB J30 subset. It does not claim evaluation over all 480 J30 instances, measure production integration behavior, or establish robustness under different project distributions. The accepted rule remains a dispatch heuristic; other project classes, resource models, or operational priority policies require a new evaluation contract.

## 6. Reproducibility

The public bundle includes the accepted candidate, full baseline diff, evaluation contract, accepted-checkpoint ledger, retained metrics, deterministic replay confirmation, all 80 baseline comparisons, feature ablations, and the j3025_9 before-and-after schedule.

Replaying the result requires the same portfolio, proven optima, score formula, and lower-is-better direction. Changing the instance set or objective creates a new evaluation. The older animated campaign surface remains in the repository as historical material; it is not the generation axis for Evölther 2.0.

The source bundle is available in the [Göther Labs results repository](https://github.com/Gother-Labs/gother-labs-results/tree/main/results/rcpsp-psplib-j30).
