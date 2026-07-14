#!/usr/bin/env python3
"""Quick test of fixes."""
import sys
sys.path.insert(0, '.')

from ml.feature_engineering import calculators

print("Testing BP category calculation...")
tests = [
    (120, 80, 1, "Elevated"),
    (130, 85, 2, "Stage 1"),
    (150, 100, 3, "Stage 2"),
    (110, 70, 0, "Normal"),
]

all_pass = True
for sys_bp, dias_bp, expected, label in tests:
    result = calculators.compute_bp_category(sys_bp, dias_bp)
    status = "✓" if result == expected else "✗"
    print(f"{status} BP {sys_bp}/{dias_bp}: {result} (expected {expected} - {label})")
    if result != expected:
        all_pass = False

print("\n" + ("All tests passed!" if all_pass else "Some tests failed!"))
sys.exit(0 if all_pass else 1)
