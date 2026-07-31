"""
Generate synthetic pharma territory dataset.

WHY SYNTHETIC: Real pharma prescriber panels (e.g. IQVIA) are commercially
licensed and not publicly available. This script generates data whose
structure mirrors real pharma potential scoring:
    potential = prescriber_count × prevalence_index × noise

Every downstream result is a demonstration of METHOD, not a claimed
client outcome.

Random seed: 42 (fully reproducible)
"""

import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
N_ZIPS = 240
N_REPS = 24
OUTPUT_PATH = Path(__file__).parent / "synthetic_territory_data.csv"


def generate_zip_data(n_zips: int = N_ZIPS, seed: int = SEED) -> pd.DataFrame:
    """Generate zip-level prescriber potential data."""
    rng = np.random.RandomState(seed)

    zips = pd.DataFrame({
        "zip_id": [f"Z{i:03d}" for i in range(n_zips)],
        "lat": rng.uniform(0, 100, n_zips),
        "lon": rng.uniform(0, 100, n_zips),
        "prescriber_count": rng.poisson(18, n_zips) + 1,
        "prevalence_index": rng.gamma(2, 2, n_zips),
    })

    zips["potential"] = (
        zips["prescriber_count"]
        * zips["prevalence_index"]
        * rng.uniform(0.8, 1.2, n_zips)
    ).round(1)

    return zips


if __name__ == "__main__":
    df = generate_zip_data()
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Written {len(df)} zips to {OUTPUT_PATH}")
    print(f"Total market potential: {df['potential'].sum():,.0f}")
    print(f"Potential range: {df['potential'].min():.1f} – {df['potential'].max():.1f}")
