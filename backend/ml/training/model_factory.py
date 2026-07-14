from typing import Any
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


def create_model(config) -> Any:
    model_type = getattr(config, "model_type", "rf")
    if model_type in ("rf", "random_forest"):
        params = {}
        if getattr(config, "n_estimators", None) is not None:
            params["n_estimators"] = config.n_estimators
        if getattr(config, "max_depth", None) is not None:
            params["max_depth"] = config.max_depth
        return RandomForestClassifier(random_state=config.random_seed, **params)

    if model_type in ("logistic", "logistic_regression"):
        lr = getattr(config, "learning_rate", None)
        C = 1.0
        if lr:
            C = 1.0 / lr
        return LogisticRegression(C=C, max_iter=1000, random_state=config.random_seed)

    if model_type in ("xgboost", "xgb"):
        try:
            from xgboost import XGBClassifier

            params = {}
            if getattr(config, "n_estimators", None) is not None:
                params["n_estimators"] = config.n_estimators
            if getattr(config, "max_depth", None) is not None:
                params["max_depth"] = config.max_depth
            return XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=config.random_seed, **params)
        except Exception as e:
            raise ImportError("xgboost is not available: %s" % e)

    if model_type in ("lightgbm", "lgbm"):
        try:
            from lightgbm import LGBMClassifier

            params = {}
            if getattr(config, "n_estimators", None) is not None:
                params["n_estimators"] = config.n_estimators
            if getattr(config, "max_depth", None) is not None:
                params["max_depth"] = config.max_depth
            return LGBMClassifier(random_state=config.random_seed, **params)
        except Exception as e:
            raise ImportError("lightgbm is not available: %s" % e)

    raise ValueError(f"Unknown model type: {model_type}")
