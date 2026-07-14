import numpy as np

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

    import pandas as pd

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


def test_scaler_fitted_on_train_only(tmp_path):
    # Create small dataset and run training

    df = _make_synthetic_df(120)
    data_file = tmp_path / "data2.csv"
    df.to_csv(data_file, index=False)

    trainer = Trainer(random_state=7)
    artifacts = trainer.train(data_path=data_file)

    numeric = ["bmi", "map", "pulse_pressure", "age", "weeks_pregnant"]
    scaler = artifacts["scaler"]
    X_train = artifacts["X_train"]

    # scaler.mean_ should equal mean of training numeric features
    import numpy as _np

    expected = _np.mean(X_train[numeric].to_numpy(), axis=0)
    assert _np.allclose(scaler.mean_, expected, atol=1e-6)


def test_reproducible_training(tmp_path):
    from tests.integration.test_end_to_end_pipeline import _make_synthetic_df

    df = _make_synthetic_df(180)
    data_file = tmp_path / "data3.csv"
    df.to_csv(data_file, index=False)

    trainer1 = Trainer(random_state=99)
    a1 = trainer1.train(data_path=data_file)

    trainer2 = Trainer(random_state=99)
    a2 = trainer2.train(data_path=data_file)

    # Models coefficients should match exactly for same seed
    import numpy as _np

    assert _np.allclose(a1["model"].coef_, a2["model"].coef_)
    assert _np.array_equal(a1["preds_test"], a2["preds_test"])
