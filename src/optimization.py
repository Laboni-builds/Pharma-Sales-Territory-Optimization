"""
Territory optimization via integer programming.

Formulation
-----------
Decision variables:  x[i,j] ∈ {0, 1}  — 1 if zip i assigned to rep j
Objective:           min Σ_i Σ_j  travel[i,j] · x[i,j]
Constraints:
  (1) Σ_j x[i,j] = 1             ∀ i    (every zip assigned exactly once)
  (2) P̄(1−τ) ≤ Σ_i P_i·x[i,j] ≤ P̄(1+τ)  ∀ j    (workload balance ±τ)

Solver: PuLP / CBC (open-source, adequate for ~500 zips)
"""

import numpy as np
import pandas as pd
import pulp
from sklearn.cluster import KMeans


def build_cost_matrix(zip_coords: np.ndarray, rep_coords: np.ndarray) -> np.ndarray:
    """Euclidean distance matrix between zips and rep home bases."""
    n_z, n_r = len(zip_coords), len(rep_coords)
    cost = np.zeros((n_z, n_r))
    for j in range(n_r):
        cost[:, j] = np.sqrt(((zip_coords - rep_coords[j]) ** 2).sum(axis=1))
    return cost


def find_rep_homes(zip_coords: np.ndarray, n_reps: int, seed: int = 42) -> np.ndarray:
    """Place rep home bases via k-means on zip coordinates."""
    km = KMeans(n_clusters=n_reps, n_init=10, random_state=seed).fit(zip_coords)
    return km.cluster_centers_


def solve_territory_ip(
    potential: np.ndarray,
    travel: np.ndarray,
    n_reps: int,
    tolerance: float = 0.15,
    time_limit: int = 60,
) -> np.ndarray:
    """
    Solve the territory assignment integer program.

    Returns
    -------
    assignment : np.ndarray of shape (n_zips,)
        Rep index assigned to each zip. -1 if solver failed.
    """
    n_zips = len(potential)
    avg_potential = potential.sum() / n_reps

    prob = pulp.LpProblem("territory_assignment", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("x", (range(n_zips), range(n_reps)), cat="Binary")

    # Objective: minimize total travel cost
    prob += pulp.lpSum(
        travel[i][j] * x[i][j] for i in range(n_zips) for j in range(n_reps)
    )

    # Constraint 1: each zip assigned exactly once
    for i in range(n_zips):
        prob += pulp.lpSum(x[i][j] for j in range(n_reps)) == 1

    # Constraint 2: workload balance per rep
    for j in range(n_reps):
        workload_j = pulp.lpSum(potential[i] * x[i][j] for i in range(n_zips))
        prob += workload_j >= avg_potential * (1 - tolerance)
        prob += workload_j <= avg_potential * (1 + tolerance)

    solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=time_limit)
    status = prob.solve(solver)

    if pulp.LpStatus[status] != "Optimal":
        print(f"WARNING: Solver status = {pulp.LpStatus[status]}")
        return np.full(n_zips, -1)

    assignment = np.full(n_zips, -1)
    for i in range(n_zips):
        for j in range(n_reps):
            if pulp.value(x[i][j]) == 1:
                assignment[i] = j

    return assignment


if __name__ == "__main__":
    from data_generation import generate_zip_data

    zips = generate_zip_data()
    coords = zips[["lat", "lon"]].values
    rep_homes = find_rep_homes(coords, n_reps=24)
    travel = build_cost_matrix(coords, rep_homes)
    assignment = solve_territory_ip(zips["potential"].values, travel, n_reps=24)

    zips["opt_rep"] = assignment
    workload = zips.groupby("opt_rep")["potential"].sum()
    cv = workload.std() / workload.mean()
    print(f"Optimized workload CV: {cv:.3f}")
    zips.to_csv("../outputs/optimized_assignment.csv", index=False)
    print("Written to outputs/optimized_assignment.csv")
