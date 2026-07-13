"""Generate a reproducible synthetic maternal risk dataset grounded in reference data."""
from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from configs.paths import BACKEND_ROOT  # noqa: E402

REFERENCE_PATHS = [
    ROOT / "ml" / "data" / "reference" / "uci_maternal_health.csv",
    ROOT / "ml" / "data" / "reference" / "Maternal Health Risk Data Set.csv",
]


def load_reference_dataset() -> pd.DataFrame:
    for path in REFERENCE_PATHS:
        if path.exists():
            return pd.read_csv(path)
    raise FileNotFoundError("No maternal reference dataset found in ml/data/reference")


def build_dataset(samples: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    random.seed(seed)
    reference_df = load_reference_dataset()

    age_values = reference_df["Age"].dropna().astype(float).to_numpy()
    systolic_values = reference_df["SystolicBP"].dropna().astype(float).to_numpy()
    diastolic_values = reference_df["DiastolicBP"].dropna().astype(float).to_numpy()
    glucose_values = reference_df["BS"].dropna().astype(float).to_numpy()
    temp_values = reference_df["BodyTemp"].dropna().astype(float).to_numpy()
    heart_rate_values = reference_df["HeartRate"].dropna().astype(float).to_numpy()

    risk_labels = ["Low"] * int(samples * 0.4)
    risk_labels += ["Moderate"] * int(samples * 0.3)
    risk_labels += ["High"] * int(samples * 0.2)
    risk_labels += ["Emergency"] * int(samples * 0.1)
    rng.shuffle(risk_labels)

    data: list[dict[str, object]] = []
    for index in range(samples):
        target_level = risk_labels[index]
        age = int(round(float(rng.choice(age_values)) + rng.normal(0, 2)))
        age = max(15, min(49, age))

        weeks_pregnant = int(rng.normal(loc=28, scale=8))
        weeks_pregnant = max(1, min(42, weeks_pregnant))

        height_cm = round(float(rng.normal(loc=162, scale=8)), 1)
        weight_kg = round(float(rng.normal(loc=68, scale=12)), 1)
        bmi = round(weight_kg / ((height_cm / 100) ** 2), 2)

        previous_pregnancies = int(rng.integers(0, 4))
        previous_c_section = int(rng.random() < 0.15)
        previous_miscarriages = int(rng.random() < 0.12)
        multiple_pregnancy = int(rng.random() < 0.05)
        history_hypertension = int(rng.random() < 0.2)
        history_diabetes = int(rng.random() < 0.12)
        history_pre_eclampsia = int(rng.random() < 0.08)

        base_systolic = float(rng.choice(systolic_values))
        base_diastolic = float(rng.choice(diastolic_values))
        base_glucose = float(rng.choice(glucose_values))
        base_temp = float(rng.choice(temp_values))
        base_heart_rate = float(rng.choice(heart_rate_values))

        severity_offset = {"Low": 0, "Moderate": 8, "High": 18, "Emergency": 35}[target_level]
        systolic_bp = int(round(base_systolic + severity_offset + rng.normal(0, 8)))
        systolic_bp = max(60, min(220, systolic_bp))
        diastolic_bp = int(round(base_diastolic + severity_offset // 2 + rng.normal(0, 4)))
        diastolic_bp = max(40, min(140, diastolic_bp))
        heart_rate = int(round(base_heart_rate + severity_offset // 3 + rng.normal(0, 6)))
        body_temperature = round(base_temp + (target_level in {"High", "Emergency"}) * 0.8 + rng.normal(0, 0.3), 2)
        blood_sugar = round(base_glucose + (target_level in {"High", "Emergency"}) * 10 + rng.normal(0, 5), 2)
        oxygen_saturation = round(float(rng.normal(loc=97.5, scale=2.0)), 2)
        hemoglobin = round(float(rng.normal(loc=12.2, scale=1.2)), 2)

        if target_level == "Emergency":
            headache = int(rng.random() < 0.7)
            blurred_vision = int(rng.random() < 0.45)
            swollen_feet = int(rng.random() < 0.6)
            bleeding = int(rng.random() < 0.25)
            abdominal_pain = int(rng.random() < 0.6)
            fever = int(rng.random() < 0.3)
            reduced_fetal_movement = int(rng.random() < 0.3)
            severe_vomiting = int(rng.random() < 0.4)
            difficulty_breathing = int(rng.random() < 0.25)
        elif target_level == "High":
            headache = int(rng.random() < 0.45)
            blurred_vision = int(rng.random() < 0.25)
            swollen_feet = int(rng.random() < 0.35)
            bleeding = int(rng.random() < 0.1)
            abdominal_pain = int(rng.random() < 0.35)
            fever = int(rng.random() < 0.2)
            reduced_fetal_movement = int(rng.random() < 0.15)
            severe_vomiting = int(rng.random() < 0.2)
            difficulty_breathing = int(rng.random() < 0.08)
        else:
            headache = int(rng.random() < 0.2)
            blurred_vision = int(rng.random() < 0.07)
            swollen_feet = int(rng.random() < 0.12)
            bleeding = int(rng.random() < 0.03)
            abdominal_pain = int(rng.random() < 0.15)
            fever = int(rng.random() < 0.05)
            reduced_fetal_movement = int(rng.random() < 0.05)
            severe_vomiting = int(rng.random() < 0.08)
            difficulty_breathing = int(rng.random() < 0.02)

        smoker = int(rng.random() < 0.12)
        alcohol = int(rng.random() < 0.05)
        nutrition_score = int(rng.integers(1, 11))
        water_intake = int(rng.integers(1, 5))
        sleep_hours = round(float(rng.normal(loc=7.4, scale=1.2)), 2)

        distance_to_hospital = int(rng.integers(5, 120))
        travel_time_minutes = int(rng.integers(10, 90))
        urban_or_rural = int(rng.random() < 0.65)

        data.append(
            {
                "age": age,
                "height_cm": height_cm,
                "weight_kg": weight_kg,
                "bmi": bmi,
                "weeks_pregnant": weeks_pregnant,
                "previous_pregnancies": previous_pregnancies,
                "previous_c_section": previous_c_section,
                "previous_miscarriages": previous_miscarriages,
                "multiple_pregnancy": multiple_pregnancy,
                "history_hypertension": history_hypertension,
                "history_diabetes": history_diabetes,
                "history_pre_eclampsia": history_pre_eclampsia,
                "systolic_bp": systolic_bp,
                "diastolic_bp": diastolic_bp,
                "heart_rate": heart_rate,
                "body_temperature": body_temperature,
                "blood_sugar": blood_sugar,
                "oxygen_saturation": oxygen_saturation,
                "hemoglobin": hemoglobin,
                "headache": headache,
                "blurred_vision": blurred_vision,
                "swollen_feet": swollen_feet,
                "bleeding": bleeding,
                "abdominal_pain": abdominal_pain,
                "fever": fever,
                "reduced_fetal_movement": reduced_fetal_movement,
                "severe_vomiting": severe_vomiting,
                "difficulty_breathing": difficulty_breathing,
                "smoker": smoker,
                "alcohol": alcohol,
                "nutrition_score": nutrition_score,
                "water_intake": water_intake,
                "sleep_hours": sleep_hours,
                "distance_to_hospital": distance_to_hospital,
                "travel_time_minutes": travel_time_minutes,
                "urban_or_rural": urban_or_rural,
                "risk_level": target_level,
            }
        )

    return pd.DataFrame(data)


def validate_dataset(df: pd.DataFrame) -> None:
    if df.isna().any().any():
        raise ValueError("Dataset contains missing values")
    if df.empty:
        raise ValueError("Dataset is empty")
    if not (15 <= df["age"].min() <= 49):
        raise ValueError("Age range is unrealistic")
    if not (1 <= df["weeks_pregnant"].min() <= 42):
        raise ValueError("Pregnancy week range is unrealistic")
    if (df["bmi"] < 12).any() or (df["bmi"] > 60).any():
        raise ValueError("BMI values are unrealistic")
    if (df["systolic_bp"] < 60).any() or (df["systolic_bp"] > 220).any():
        raise ValueError("Systolic BP values are unrealistic")
    if df.duplicated().any():
        raise ValueError("Dataset contains duplicate rows")
    counts = df["risk_level"].value_counts(normalize=True)
    expected = {"Low": 0.4, "Moderate": 0.3, "High": 0.2, "Emergency": 0.1}
    for label, expected_ratio in expected.items():
        ratio = counts.get(label, 0.0)
        if abs(ratio - expected_ratio) > 0.08:
            raise ValueError(f"Class distribution deviates too much for {label}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic maternal risk data")
    parser.add_argument("--samples", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str, default=str(ROOT / "ml" / "data" / "synthetic" / "pregnancy_risk_v1.csv"))
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = build_dataset(samples=args.samples, seed=args.seed)
    validate_dataset(df)
    df.to_csv(output_path, index=False)
    print(f"Saved synthetic dataset to {output_path}")
    print(df["risk_level"].value_counts().to_string())


if __name__ == "__main__":
    main()
