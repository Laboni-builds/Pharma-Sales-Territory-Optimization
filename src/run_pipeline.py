"""
run_pipeline.py — end-to-end command-line driver for the territory
optimization project.

Imports and orchestrates all four src/ modules to reproduce, as a single
runnable script, the same flow documented narratively in
notebooks/territory_optimization.ipynb:

    1. Generate synthetic data
    2. Establish current-state (naive) baseline
    3. Establish greedy nearest-rep baseline
    4. Solve the integer-programming optimization
    5. Benchmark all three scenarios
    6. Run the Monte Carlo robustness stress test
    7. Translate results into business KPIs
    8. Write outputs to outputs/

Usage
-----
    cd pharma-territory-optimization
    python src/run_pipeline.py

Note: this script duplicates the notebook's logic in code form for
command-line reproducibility (e.g. CI, automation). The notebook remains
the primary narrative deliverable — this is a secondary, code-only path.
"""

import sys
from pathlib import Path

import pandas as pd

# Make sibling src/ imports work regardless of the working directory
sys.path.insert(0, str(Path(__file__).resolve().parent))

from data_generation import generate_zip_data
from baselines import baseline_geographic_sort, baseline_greedy_nearest, workload_cv, total_travel_cost
from optimization import find_rep_homes, build_cost_matrix, solve_territory_ip
from monte_carlo import run_stress_test
from roi_translation import build_kpi_summary

N_REPS = 24
TOLERANCE = 0.15
REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = REPO_ROOT / "outputs"


def main():
    OUTPUTS_DIR.mkdir(exist_ok=True)

    # 1. Synthetic data
    print("=" * 60)
    print("STEP 1: Generating synthetic data (seed=42)")
    print("=" * 60)
    zips = generate_zip_data()
    coords = zips[["lat", "lon"]].values
    potential = zips["potential"].values
    total_potential = potential.sum()
    print(f"Generated {len(zips)} zips | total potential = {total_potential:,.0f}\n")

    # 2. Current-state (naive geographic) baseline
    print("=" * 60)
    print("STEP 2: Current-state baseline (naive geographic sort)")
    print("=" * 60)
    current_assignment = baseline_geographic_sort(zips, N_REPS)
    current_cv = workload_cv(potential, current_assignment)
    print(f"Current-state workload CV: {current_cv:.3f}\n")

    # 3. Rep home bases + travel matrix (needed for both greedy and IP)
    rep_homes = find_rep_homes(coords, n_reps=N_REPS)
    travel = build_cost_matrix(coords, rep_homes)

    # 4. Greedy nearest-rep baseline
    print("=" * 60)
    print("STEP 3: Greedy nearest-rep baseline (travel-only)")
    print("=" * 60)
    greedy_assignment = baseline_greedy_nearest(travel)
    greedy_cv = workload_cv(potential, greedy_assignment)
    greedy_travel = total_travel_cost(travel, greedy_assignment)
    print(f"Greedy workload CV: {greedy_cv:.3f}")
    print(f"Greedy total travel cost: {greedy_travel:,.1f}\n")

    # 5. Integer programming optimization
    print("=" * 60)
    print("STEP 4: Solving integer program (PuLP/CBC)")
    print("=" * 60)
    opt_assignment = solve_territory_ip(potential, travel, n_reps=N_REPS, tolerance=TOLERANCE)
    if (opt_assignment == -1).any():
        print("ERROR: Solver failed to find an optimal solution. Aborting.")
        sys.exit(1)
    opt_cv = workload_cv(potential, opt_assignment)
    opt_travel = total_travel_cost(travel, opt_assignment)
    print(f"Optimized workload CV: {opt_cv:.3f}")
    print(f"Optimized total travel cost: {opt_travel:,.1f}\n")

    # 6. Benchmark summary
    print("=" * 60)
    print("STEP 5: Benchmark comparison")
    print("=" * 60)
    print(f"{'Scenario':<25}{'Workload CV':<15}{'Travel Cost':<15}")
    print(f"{'Current-state':<25}{current_cv:<15.3f}{'n/a':<15}")
    print(f"{'Greedy (travel-only)':<25}{greedy_cv:<15.3f}{greedy_travel:<15,.1f}")
    print(f"{'Optimized (IP)':<25}{opt_cv:<15.3f}{opt_travel:<15,.1f}")
    travel_premium = (opt_travel - greedy_travel) / greedy_travel
    print(f"\nTravel cost premium of optimized vs. greedy: {travel_premium:.1%}\n")

    # 7. Monte Carlo stress test
    print("=" * 60)
    print("STEP 6: Monte Carlo stress test (200 scenarios, ±15% noise)")
    print("=" * 60)
    mc_results = run_stress_test(
        potential, opt_assignment, n_reps=N_REPS,
        n_sims=200, noise_std=0.15, tolerance=TOLERANCE,
    )
    print(f"Mean CV under noise: {mc_results['cv_mean']:.3f}")
    print(f"Breach rate: {mc_results['breach_rate']:.1%} "
          f"({mc_results['breach_count']}/{mc_results['n_sims']} scenarios)\n")

    # 8. ROI translation
    print("=" * 60)
    print("STEP 7: ROI / business KPI translation")
    print("=" * 60)
    kpi_df = build_kpi_summary(
        baseline_cv=current_cv,
        greedy_cv=greedy_cv,
        opt_cv=opt_cv,
        travel_greedy=greedy_travel,
        travel_opt=opt_travel,
        breach_rate=mc_results["breach_rate"],
        total_potential=total_potential,
    )
    print(kpi_df.to_string(index=False))
    print()

    # 9. Write outputs
    zips_out = zips.copy()
    zips_out["current_rep"] = current_assignment
    zips_out["greedy_rep"] = greedy_assignment
    zips_out["optimized_rep"] = opt_assignment
    zips_out.to_csv(OUTPUTS_DIR / "optimized_assignment.csv", index=False)
    kpi_df.to_csv(OUTPUTS_DIR / "kpi_summary.csv", index=False)

    print("=" * 60)
    print("DONE")
    print("=" * 60)
    print(f"Written: {OUTPUTS_DIR / 'optimized_assignment.csv'}")
    print(f"Written: {OUTPUTS_DIR / 'kpi_summary.csv'}")


if __name__ == "__main__":
    main()
