import time
import logging
from pathlib import Path
from typing import Any, Optional, Union
from .config import TrainingConfig
from .model_factory import create_model
from .metrics import compute_metrics
from .artifact_manager import ArtifactManager
from .calibration import calibrate_model


class Trainer:
    def __init__(
        self,
        config: Optional[TrainingConfig] = None,
        output_dir: Optional[Union[str, Path]] = None,
        random_state: int = 42,
    ):
        # Backwards-compatible constructor: accepts either a TrainingConfig
        # or the older (output_dir, random_state) style used by tests.
        if config is None:
            config = TrainingConfig(random_seed=random_state, save_directory=str(output_dir or "artifacts"))

        self.config = config
        self.artifact_dir = str(output_dir or config.save_directory)
        self.artifact_manager = ArtifactManager(self.artifact_dir)
        self.logger = logging.getLogger(__name__)

    def train(self, X_train, y_train, X_val, y_val, X_test=None, y_test=None, preprocessor=None):
        start = time.time()
        # build model
        model = create_model(self.config)

        # fit
        model.fit(X_train, y_train)

        # optional calibration
        calibrated = None
        if X_val is not None and y_val is not None:
            try:
                calibrated = calibrate_model(model, X_val, y_val)
            except Exception as e:
                # Do not silently swallow calibration errors; log for visibility.
                self.logger.warning("Calibration skipped: %s", e)
                calibrated = None

        predictor = calibrated if calibrated is not None else model

        # evaluate
        y_pred_train = predictor.predict(X_train)
        y_proba_train = getattr(predictor, "predict_proba", lambda X: None)(X_train)
        train_metrics = compute_metrics(y_train, y_pred_train, y_proba_train)

        results = {
            "train_metrics": train_metrics,
            "model_type": self.config.model_type,
        }

        if X_val is not None and y_val is not None:
            y_pred_val = predictor.predict(X_val)
            y_proba_val = getattr(predictor, "predict_proba", lambda X: None)(X_val)
            results["val_metrics"] = compute_metrics(y_val, y_pred_val, y_proba_val)

        if X_test is not None and y_test is not None:
            y_pred_test = predictor.predict(X_test)
            y_proba_test = getattr(predictor, "predict_proba", lambda X: None)(X_test)
            results["test_metrics"] = compute_metrics(y_test, y_pred_test, y_proba_test)

        elapsed = time.time() - start
        results["training_time_seconds"] = elapsed

        # save artifacts (save predictor if calibration applied)
        model_to_save = predictor
        model_path = self.artifact_manager.save_model(model_to_save)
        results["artifacts"] = {"model": model_path}
        if preprocessor is not None:
            preproc_path = self.artifact_manager.save_preprocessor(preprocessor)
            results["artifacts"]["preprocessor"] = preproc_path

        # config and summary
        self.config.save(self.artifact_manager._path("training_config.json"))
        self.artifact_manager.save_training_summary({
            "dataset": self.config.dataset_name,
            "dataset_version": self.config.dataset_version,
            "metrics": results.get("test_metrics") or results.get("val_metrics") or results.get("train_metrics"),
            "training_time_seconds": elapsed,
        })

        # expose the fitted predictor for convenience (tests/demos may expect)
        results["model"] = predictor
        return results


