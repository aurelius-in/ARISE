from __future__ import annotations

import numpy as np
import pandas as pd


def rejuvenation_score(row: pd.Series) -> float:
    """Toy rejuvenation scorer with plausible dependencies.
    Higher is better (0-100).
    """
    base = 50.0
    boost = 0.0
    if row["type"] in ["TF_combo", "CRISPRa"]:
        boost += 8.0
    if row["target_genes"] in ["OSK", "OSKM", "FOXO3", "SIRT1", "KLF4"]:
        boost += 10.0
    boost += np.clip(12 - abs(row["pulse_hours"] - 24), 0, 12) * 0.8
    dose_term = 8.0 * np.exp(-((row["dose"] - 1.2) ** 2) / 0.8)
    noise = np.random.normal(0, 3)
    return float(np.clip(base + boost + dose_term + noise, 0, 100))


def safety_risk(row: pd.Series) -> float:
    """Toy safety risk score where lower is safer (0-100).
    Penalizes MYC/OSKM and long pulses.
    """
    risk = 30.0
    if row["target_genes"] in ["MYC", "OSKM"]:
        risk += 35.0
    if row["pulse_hours"] >= 36:
        risk += 15.0
    risk += 10.0 * (row["dose"] > 2.0)
    risk += np.random.normal(0, 4)
    return float(np.clip(risk, 0, 100))


def confidence_score(row: pd.Series) -> float:
    """Toy confidence that rises for common modalities/genes and 24h-adjacent pulses."""
    base = 55.0
    if row["type"] == "SmallMolecule":
        base += 10.0
    if row["target_genes"] in ["OSK", "FOXO3", "SIRT1", "KLF4"]:
        base += 8.0
    base -= 0.3 * abs(row["pulse_hours"] - 24)
    base += np.random.normal(0, 5)
    return float(np.clip(base, 10, 100))

