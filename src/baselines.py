"""
Two baseline territory assignments for benchmarking.

Baseline 1 — Current-state (naive geographic sort)
    Zips sorted by longitude, then split into N equal-sized groups.
    Simulates how territories drift when drawn by geography alone.

Baseline 2 — Greedy nearest-rep
    Each zip assigned to its closest rep home base.
    Minimizes travel but ignores workload balance entirely.
    Purpose: quantify the "cost of fairness" — how much extra travel
    the optimized plan accepts in exchange for balanced workloads.
"""

import numpy as np
import pandas as pd


def baseline_geographic_sort(zips: pd.DataFrame, n_reps: int) -> np.ndarray:
    """Assign zips by sorting on longitude and splitting into equal groups."""
    sorted_idx = zips["lon"].argsort()
    assignment = np.zeros(len(zips), dtype=int)
    assignment[sorted_idx] = np.repeat(range(n_reps), len(zips) // n_reps)
    return assignment


def baseline_greedy_nearest(travel_matrix: np.ndarray) -> np.ndarray:
    """Assign each zip to the nearest rep (travel-only, no balance)."""
    return travel_matrix.argmin(axis=1)


def workload_cv(potential: np.ndarray, assignment: np.ndarray) -> float:
    """Coefficient of variation of workload across reps."""
    workload = pd.Series(potential).groupby(assignment).sum()
    return workload.std() / workload.mean()


def total_travel_cost(travel_matrix: np.ndarray, assignment: np.ndarray) -> float:
    """Total travel cost under a given assignment."""
    return sum(travel_matrix[i, assignment[i]] for i in range(len(assignment)))
