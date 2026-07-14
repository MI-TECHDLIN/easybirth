import json
from pathlib import Path

import numpy as np
import pandas as pd

from ml.training.trainer import Trainer


def _make_synthetic_df(n=200):
    rng = np.random.default_rng(0)
    ages = rng.integers(18, 40, size=n)
    heights = rng.integers(140, 180, size=n).astype(float)
    weights = rng.integers(45, 100, size=n).astype(float)
    bmi = (weights / ((heights / 100) ** 2)).round(2)
    weeks = rng.integers(8, 40, size=n)
    systolic = rng.integers(100, 160, size=n)
    diastolic = (systolic - rng.integers(20, 40, size=n)).astype(int)
    risk = rng.choice(["Low", "Moderate", "High", "Emergency"], size=n, p=[0.4, 0.3, 0.2, 0.1])

    df = pd.DataFrame({
        "age": ages,
        "height_cm": heights,
        "weight_kg": weights,
        "bmi": bmi,
        "weeks_pregnant": weeks,
        "systolic_bp": systolic,
        "diastolic_bp": diastolic,
        "heart_rate": rng.integers(60, 100, size=n),
        "body_temperature": rng.normal(36.6, 0.3, size=n),
        "blood_sugar": rng.integers(70, 140, size=n).astype(float),
        "oxygen_saturation": rng.integers(95, 100, size=n),
        "hemoglobin": rng.normal(12.5, 1.0, size=n),
        "distance_to_hospital": rng.integers(1, 100, size=n),
        "travel_time_minutes": rng.integers(5, 120, size=n),
        "risk_level": risk,
    })

    return df


def test_end_to_end_pipeline(tmp_path: Path):
    df = _make_synthetic_df(200)
    data_file = tmp_path / "data.csv"
    df.to_csv(data_file, index=False)

    out_dir = tmp_path / "artifacts"
    trainer = Trainer(output_dir=out_dir, random_state=123)
    artifacts = trainer.train(data_path=data_file)

    # Ensure splits are disjoint by row content (no leakage)
    combined = pd.concat(
        [artifacts["split"].train, artifacts["split"].val, artifacts["split"].test],
        ignore_index=True,
    )
    assert combined.drop_duplicates().shape[0] == combined.shape[0]

    # Model and scaler saved
    assert (out_dir / "model.joblib").exists()
    assert (out_dir / "scaler.joblib").exists()

    # Reload saved model and scaler and ensure predictions match
    import joblib

    model_saved = joblib.load(out_dir / "model.joblib")
    scaler_saved = joblib.load(out_dir / "scaler.joblib")

    numeric = ["bmi", "map", "pulse_pressure", "age", "weeks_pregnant"]
    X_test = artifacts["X_test"]
    X_test_scaled = scaler_saved.transform(X_test[numeric])
    preds_reload = model_saved.predict(X_test_scaled)

    assert (preds_reload == artifacts["preds_test"]).all()
