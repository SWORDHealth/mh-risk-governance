#!/usr/bin/env python3
"""Recompute all reported metrics (point estimates, 95% BCa CIs, confusion
matrices) from the released prediction files.

Usage: python compute_metrics.py ../aegis  (or ../cradle)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
from scipy.stats import bootstrap
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support,
)

N_BOOT = 10_000
SEED = 42


def specificity(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp = cm[0]
    return tn / (tn + fp) if (tn + fp) > 0 else 0.0


def _metric_fn(name: str):
    if name == "accuracy":
        return accuracy_score
    if name == "specificity":
        return specificity
    idx = {"precision": 0, "recall": 1, "f1": 2}[name]
    return lambda yt, yp: precision_recall_fscore_support(
        yt, yp, average="binary", zero_division=0
    )[idx]


def bootstrap_ci(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Dict[str, float]]:
    """BCa (bias-corrected & accelerated) bootstrap CIs, paired by row."""
    rng = np.random.default_rng(SEED)
    out: Dict[str, Dict[str, float]] = {}
    for name in ("accuracy", "precision", "recall", "f1", "specificity"):
        fn = _metric_fn(name)
        res = bootstrap(
            (y_true, y_pred),
            statistic=fn,
            n_resamples=N_BOOT,
            paired=True,
            vectorized=False,
            method="BCa",
            confidence_level=0.95,
            random_state=rng,
        )
        out[name] = {
            "lo": float(res.confidence_interval.low),
            "hi": float(res.confidence_interval.high),
        }
    return out


def evaluate(df: pd.DataFrame, pred_col: str, name: str) -> None:
    y_true = (df["label"] == "unsafe").astype(int).to_numpy()
    y_pred = df[pred_col].astype(int).to_numpy()
    p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="binary", zero_division=0)
    point = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": p,
        "recall": r,
        "f1": f1,
        "specificity": specificity(y_true, y_pred),
    }
    ci = bootstrap_ci(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist()
    print(f"\n=== {name} (n={len(df)}) ===")
    for k, v in point.items():
        print(f"  {k:<12} {v:.4f}  (95% CI {ci[k]['lo']:.4f} – {ci[k]['hi']:.4f})")
    print(f"  confusion_matrix [[TN,FP],[FN,TP]] = {cm}")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    d = Path(sys.argv[1])
    primary = pd.read_json(d / "classifier.jsonl", lines=True)
    gated = pd.read_json(d / "classifier_pg.jsonl", lines=True)
    evaluate(primary, "pred_unsafe", "classifier")
    evaluate(gated, "final_unsafe", "classifier + pass-gate")


if __name__ == "__main__":
    main()
