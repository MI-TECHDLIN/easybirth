from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
import json
from datetime import datetime


@dataclass
class TrainingConfig:
    random_seed: int = 42
    model_type: str = "rf"
    learning_rate: Optional[float] = None
    max_depth: Optional[int] = None
    n_estimators: int = 100
    cross_validation_folds: int = 5
    scoring_metric: str = "recall"
    save_directory: str = "artifacts"
    dataset_name: str = "pregnancy_risk_v1"
    dataset_version: str = "1.0"

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["created_at"] = datetime.utcnow().isoformat()
        return d

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @staticmethod
    def load(path: str) -> "TrainingConfig":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # ignore created_at
        fields = {k: data[k] for k in data if k in TrainingConfig.__annotations__}
        return TrainingConfig(**fields)
