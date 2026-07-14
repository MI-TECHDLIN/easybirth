from typing import Dict, Any, Optional
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)
import numpy as np


def compute_metrics(y_true, y_pred, y_proba: Optional[np.ndarray] = None, positive_label=None) -> Dict[str, Any]:
    metrics = {}
    metrics["accuracy"] = float(accuracy_score(y_true, y_pred))
    # If binary, use pos_label
    average = "binary" if len(set(y_true)) == 2 else "macro"
    if average == "binary":
        pos = positive_label if positive_label is not None else 1
        metrics["precision"] = float(precision_score(y_true, y_pred, pos_label=pos))
        metrics["recall"] = float(recall_score(y_true, y_pred, pos_label=pos))
        metrics["f1"] = float(f1_score(y_true, y_pred, pos_label=pos))
    else:
        metrics["precision_macro"] = float(precision_score(y_true, y_pred, average="macro", zero_division=0))
        metrics["recall_macro"] = float(recall_score(y_true, y_pred, average="macro", zero_division=0))
        metrics["f1_macro"] = float(f1_score(y_true, y_pred, average="macro", zero_division=0))

    # ROC AUC when probabilities are provided and binary
    if y_proba is not None:
        try:
            if y_proba.ndim == 1 or y_proba.shape[1] == 1:
                metrics["roc_auc"] = float(roc_auc_score(y_true, y_proba.ravel()))
            else:
                # try taking prob of positive class (last column)
                metrics["roc_auc_macro"] = float(roc_auc_score(y_true, y_proba, multi_class="ovo", average="macro"))
        except Exception:
            metrics["roc_auc"] = None
    else:
        metrics["roc_auc"] = None

    # Confusion matrix
    try:
        cm = confusion_matrix(y_true, y_pred)
        metrics["confusion_matrix"] = cm.tolist()
    except Exception:
        metrics["confusion_matrix"] = None

    return metrics
