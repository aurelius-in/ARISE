from __future__ import annotations

import pandas as pd
import numpy as np
from typing import Optional


def demo_candidates(n: int = 200, seed: int = 7) -> pd.DataFrame:
    """Generate a demo candidates dataframe with plausible columns.

    Columns: name, type, dose, pulse_hours, target_genes
    """
    rng = np.random.default_rng(seed)
    types = rng.choice(["TF_combo", "SmallMolecule", "CRISPRi", "CRISPRa"], size=n, p=[0.35, 0.35, 0.15, 0.15])
    doses = np.round(rng.lognormal(mean=0.2, sigma=0.6, size=n), 3)
    pulses = rng.choice([6, 12, 24, 36, 48, 72], size=n, p=[0.10, 0.20, 0.35, 0.15, 0.15, 0.05])
    genes = rng.choice(["OSK", "OSKM", "FOXO3", "SIRT1", "KLF4", "MYC", "NANOG", "GATA4", "REST", "TEAD1"], size=n)
    names = [f"cand_{i:04d}" for i in range(n)]
    df = pd.DataFrame({
        "name": names,
        "type": types,
        "dose": doses,
        "pulse_hours": pulses,
        "target_genes": genes,
    })
    return df


def read_candidates_csv(file_obj: object) -> pd.DataFrame:
    """Read user-uploaded CSV and validate required columns."""
    df = pd.read_csv(file_obj)
    required = {"name", "type", "dose", "pulse_hours", "target_genes"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return df

