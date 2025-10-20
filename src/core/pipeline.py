from __future__ import annotations

from typing import Optional
import numpy as np
import pandas as pd

from .datasets import demo_candidates, read_candidates_csv
from .models import rejuvenation_score, safety_risk, confidence_score


def score_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Compute per-row scores and a composite ranking, return sorted copy."""
    df = df.copy()
    df["Rejuvenation"] = df.apply(rejuvenation_score, axis=1)
    df["SafetyRisk"] = df.apply(safety_risk, axis=1)
    df["Confidence"] = df.apply(confidence_score, axis=1)
    # Composite: high Rejuvenation, low SafetyRisk, high Confidence
    df["Composite"] = (
        df["Rejuvenation"] * 0.55 + (100.0 - df["SafetyRisk"]) * 0.30 + df["Confidence"] * 0.15
    )
    df.sort_values(by="Composite", ascending=False, inplace=True)
    return df


def run_simulation(n: int = 200, seed: int = 7, csv_file: Optional[object] = None) -> pd.DataFrame:
    """Generate or read candidates, seed RNG for determinism, then score and rank."""
    np.random.seed(seed)
    if csv_file is None:
        df = demo_candidates(n=n, seed=seed)
    else:
        df = read_candidates_csv(csv_file)
    return score_dataframe(df)

