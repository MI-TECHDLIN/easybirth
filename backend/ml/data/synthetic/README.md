# Synthetic Dataset

This folder contains generated synthetic training data for the EasyBirth pregnancy risk model.

## Current dataset

- `pregnancy_risk_v1.csv` — synthetic dataset generated from clinically plausible ranges and rules

## Generation command

```bash
python scripts/generate_synthetic_data.py --samples 5000 --seed 42
```
