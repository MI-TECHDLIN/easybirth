"""Trainer utilities for training workflows.

This module provides a thin `Trainer` class that wraps the training
pipeline for easier invocation from scripts and tests.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from ml.pipelines.training_pipeline import run_training


class Trainer:
    """Simple trainer wrapper."""

    def __init__(self, output_dir: Path | None = None, random_state: int = 42):
        self.output_dir = output_dir
        self.random_state = random_state

    def train(self, data_path: Path | None = None) -> Dict[str, Any]:
        """Run training pipeline and return artifacts."""
        return run_training(
            data_path=data_path,
            output_dir=self.output_dir,
            random_state=self.random_state,
        )

