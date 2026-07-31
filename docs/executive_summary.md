# Executive Summary — Territory Reassignment Recommendation

**Prepared for:** Regional Sales Operations Director
**Analysis scope:** 240 zip-level units, 24 medical reps (scaled model of 300-rep field force)

---

## Situation

Current territory boundaries were drawn by geography alone during the last field-force expansion. No prescriber-potential weighting was applied. This has created significant workload imbalance: the highest-loaded rep carries roughly 2× the prescriber potential of the lowest-loaded rep.

## Finding

Re-optimizing territory assignment against prescriber potential — using a mathematical optimization model that minimizes travel cost while enforcing workload balance — reduces workload imbalance by approximately 58%, measured by coefficient of variation across reps (0.229 → 0.095).

This improvement comes at a modest cost: total travel distance is approximately 5% higher than a pure travel-minimizing (but heavily unbalanced) alternative. We view this as an acceptable trade-off — the imbalance reduction is large, and the travel premium is small.

## Robustness

Prescriber-potential estimates are inherently uncertain. We stress-tested the optimized plan by perturbing every zip's potential by ±15% across 200 simulated scenarios. The plan holds up on average, but roughly 23% of scenarios show at least one rep breaching the tolerance band by more than 10%.

**Implication:** the optimized plan should be treated as the starting point for an annual planning cycle with a semi-annual rebalance check — not as a permanent, one-time fix.

## Illustrative impact

Using a placeholder coverage-to-prescribing elasticity (2% incremental scripts per potential-point of improved coverage, at a margin of ₹45 per script), the rebalanced plan is projected to unlock incremental value on the order of several lakhs per planning period. **This figure is illustrative and should be replaced with a client-derived elasticity before use in a business case.**

## Recommendation

1. **Adopt** the potential-balanced territory plan for the upcoming annual planning cycle.
2. **Schedule** a semi-annual rebalance review, informed by updated potential estimates.
3. **Phase 2:** Add territory-contiguity constraints and real drive-time data (routing API) to further improve operational usability.

## Limitations disclosed

- Synthetic data used (real prescriber panels not available for this analysis)
- No territory-contiguity constraint (zips assigned to a rep may not be geographically contiguous)
- ROI elasticity is illustrative, not client-validated

---

*Analysis performed on synthetic data. Results demonstrate methodology, not actual client outcomes.*
