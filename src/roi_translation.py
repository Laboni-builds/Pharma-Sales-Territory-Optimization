"""
Translate technical optimization results into business KPIs and
illustrative ROI.

IMPORTANT: The elasticity and margin assumptions below are PLACEHOLDERS.
In a real engagement, these would come from:
  - A prior HCP-response study (coverage → prescribing elasticity)
  - The client's finance team (margin per script)

Every output of this module should be clearly flagged as
"illustrative / assumption-driven" in any presentation or document.
"""

import pandas as pd


def build_kpi_summary(
    baseline_cv: float,
    greedy_cv: float,
    opt_cv: float,
    travel_greedy: float,
    travel_opt: float,
    breach_rate: float,
    total_potential: float,
    assumed_elasticity: float = 0.02,
    margin_per_script: float = 45.0,
) -> pd.DataFrame:
    """
    Build a single KPI summary table suitable for an executive slide.
    """
    workload_gap_recovered = (baseline_cv - opt_cv) * total_potential
    incremental_scripts = workload_gap_recovered * assumed_elasticity
    incremental_value = incremental_scripts * margin_per_script

    return pd.DataFrame({
        "KPI": [
            "Workload CV (current → optimized)",
            "CV reduction vs. current state",
            "Travel cost premium vs. greedy baseline",
            "Monte Carlo breach rate",
            "Illustrative incremental value per period",
        ],
        "Value": [
            f"{baseline_cv:.3f} → {opt_cv:.3f}",
            f"{(baseline_cv - opt_cv) / baseline_cv:.0%}",
            f"{(travel_opt - travel_greedy) / travel_greedy:.1%}",
            f"{breach_rate:.0%}",
            f"~{incremental_value:,.0f} currency units (ILLUSTRATIVE — replace with client elasticity)",
        ],
    })
