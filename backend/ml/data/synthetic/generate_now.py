#!/usr/bin/env python3
"""Quick script to generate synthetic dataset."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.generate_synthetic_data import build_dataset, validate_dataset

output_path = Path(__file__).parent / "pregnancy_risk_v1.csv"

print("Generating synthetic maternal risk dataset...")
df = build_dataset(samples=5000, seed=42)

print("Validating dataset...")
validate_dataset(df)

print("Saving to CSV...")
df.to_csv(output_path, index=False)

print(f"\n✓ Saved to {output_path}")
print(f"✓ Rows: {len(df)}")
print("\nRisk level distribution:")
print(df['risk_level'].value_counts().sort_index().to_string())
print(f"\nColumns: {len(df.columns)}")
print(f"First row:\n{df.iloc[0]}")
