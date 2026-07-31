# Data Directory

## Why synthetic data?

Real pharma territory/prescriber data is commercially licensed (e.g. IQVIA), covered by client confidentiality agreements, and not publicly available. Using synthetic data is the only ethical option for a student portfolio project. This is not a limitation to hide — it's a data-governance decision to disclose.

## How the synthetic data is structured

The data-generating process mirrors how real pharma potential scores are constructed:

| Field | Generation logic | Real-world analog |
|---|---|---|
| `zip_id` | Sequential ID for 240 zip-code-level units | Actual postal codes / brick-level units |
| `lat`, `lon` | Uniform random on [0, 100] | Real geographic coordinates |
| `prescriber_count` | Poisson(λ=18) + 1 | Number of Rx-writing physicians in the zip, from a prescriber panel |
| `prevalence_index` | Gamma(α=2, β=2) | Disease burden / patient prevalence proxy from claims or epi data |
| `potential` | `prescriber_count × prevalence_index × Uniform(0.8, 1.2)` | Composite potential score used for territory sizing |

**Random seed:** 42 (set in the generation script for full reproducibility)

## To regenerate

```bash
python generate_synthetic_data.py
# Writes: synthetic_territory_data.csv
```
