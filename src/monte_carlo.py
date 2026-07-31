"""
Monte Carlo stress test for territory robustness.

Tests whether the optimized assignment (which was built on point-estimate
potential scores) still satisfies workload-balance constraints when
potential estimates are perturbed by realistic noise.

This is NOT a validation of the optimizer — it's a validation of the
DECISION to deploy the plan given inherent estimation uncertainty.
"""

import numpy as np
import pandas as pd


def run_stress_test(
    potential: np.ndarray,
    assignment: np.ndarray,
    n_reps: int,
    n_sims: int = 200,
    noise_std: float = 0.15,
    tolerance: float = 0.15,
    breach_margin: float = 0.10,
    seed: int = 123,
) -> dict:
    """
    Perturb potential estimates and check balance under the fixed assignment.

    Parameters
    ----------
    potential : base potential scores per zip
    assignment : optimized rep assignment per zip
    n_sims : number of Monte Carlo scenarios
    noise_std : std of multiplicative noise (0.15 = ±15%)
    tolerance : original IP tolerance band
    breach_margin : how far beyond the band counts as a breach (0.10 = 10% beyond)

    Returns
    -------
    dict with cv_list, breach_count, breach_rate
    """
    rng = np.random.RandomState(seed)
    avg_potential = potential.sum() / n_reps
    upper = avg_potential * (1 + tolerance) * (1 + breach_margin)
    lower = avg_potential * (1 - tolerance) * (1 - breach_margin)

    cv_list = []
    breach_count = 0

    for _ in range(n_sims):
        noise = rng.normal(1.0, noise_std, len(potential))
        sim_potential = potential * noise
        sim_workload = pd.Series(sim_potential).groupby(assignment).sum()
        cv = sim_workload.std() / sim_workload.mean()
        cv_list.append(cv)
        if (sim_workload > upper).any() or (sim_workload < lower).any():
            breach_count += 1

    return {
        "cv_list": cv_list,
        "cv_mean": np.mean(cv_list),
        "breach_count": breach_count,
        "breach_rate": breach_count / n_sims,
        "n_sims": n_sims,
        "noise_std": noise_std,
    }
