# Assumptions, Limitations, and Risks

## Assumptions

| # | Assumption | Impact if wrong | Mitigation |
|---|---|---|---|
| A1 | Travel cost is well-proxied by Euclidean distance | Optimized territories may not be drivable in practice | Replace with real drive-time from Google Maps / OSRM in Phase 2 |
| A2 | ±15% workload tolerance is acceptable to sales ops | Tighter tolerance may be infeasible; looser tolerance may not fix the problem | Workshop with stakeholder before finalizing |
| A3 | Prescriber potential is the right metric for territory sizing | Other factors (call frequency norms, specialty mix) may matter | Validate with sales-ops team that potential is the primary sizing driver |
| A4 | Rep home bases can be approximated by k-means cluster centers | Real reps live at specific addresses | Replace with actual rep home addresses in a real engagement |
| A5 | ROI elasticity of 2% scripts per potential-point is reasonable | Over/under-estimates the business case | Replace with client- or literature-derived elasticity before presenting ROI to finance |

## Limitations

| # | Limitation | Severity | Planned resolution |
|---|---|---|---|
| L1 | No territory-contiguity constraint | High — territories may be geographically fragmented | Phase 2: graph-based contiguity constraint or post-processing merge |
| L2 | CBC solver limits practical scale to ~500 zips | Medium — national rollouts need thousands | Move to Gurobi/CPLEX or cluster-then-optimize decomposition |
| L3 | Monte Carlo only varies potential, not travel or rep attrition | Low-Medium — incomplete uncertainty picture | Extend simulation to jointly perturb all three |
| L4 | Synthetic data, not real prescriber panels | Context-dependent — method is valid, numbers are illustrative | Clearly disclosed everywhere; re-run on real data in a client engagement |
| L5 | Single-objective optimization (travel cost only, balance as constraint) | Low — could instead maximize coverage or multi-objective | Test alternative formulations if stakeholder priorities shift |

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Reps resist territory changes (relationship disruption) | High | High — adoption failure | Phase changes gradually; protect longest-standing rep-physician relationships |
| Potential estimates are stale by the time plan is implemented | Medium | Medium — plan quality degrades | Semi-annual rebalance cadence, not one-time fix |
| Contiguity gaps make some territories undrivable | High (given L1) | High — operational failure | Manual review of optimized output before deployment; Phase 2 constraint |
