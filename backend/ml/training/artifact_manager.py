import os
import json
from typing import Any, Dict, Optional
import joblib
from datetime import datetime


class ArtifactManager:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def _path(self, name: str) -> str:
        return os.path.join(self.base_dir, name)

    def save_model(self, model: Any, name: str = "model.joblib") -> str:
        path = self._path(name)
        joblib.dump(model, path)
        return path

    def save_preprocessor(self, preprocessor: Any, name: str = "preprocessor.joblib") -> str:
        path = self._path(name)
        joblib.dump(preprocessor, path)
        return path

    def save_json(self, obj: Dict, name: str) -> str:
        path = self._path(name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2)
        return path

    def save_training_summary(self, summary: Dict) -> str:
        summary.setdefault("created_at", datetime.utcnow().isoformat())
        return self.save_json(summary, "training_summary.json")
