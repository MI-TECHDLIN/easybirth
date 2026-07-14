from sklearn.calibration import CalibratedClassifierCV
from typing import Any


def calibrate_model(estimator: Any, X_val, y_val, method: str = "sigmoid"):
    """Return a calibrated classifier fitted on validation data."""
    calib = CalibratedClassifierCV(base_estimator=estimator, method=method, cv="prefit")
    calib.fit(X_val, y_val)
    return calib
