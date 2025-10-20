import pandas as pd
import numpy as np

from src.core.pipeline import run_simulation, score_dataframe


def test_score_columns_and_sorting():
    # Deterministic seed
    df = run_simulation(n=50, seed=42)
    required = {"Rejuvenation", "SafetyRisk", "Confidence", "Composite"}
    assert required.issubset(df.columns)
    # Check sorting by Composite desc
    comps = df["Composite"].values
    assert (np.diff(comps) <= 0).all()


def test_deterministic_top_rank_with_seed():
    # The absolute scores have noise, but with a set RNG seed, the ranking should be stable
    df1 = run_simulation(n=60, seed=123)
    df2 = run_simulation(n=60, seed=123)
    top10_1 = df1.head(10)["name"].tolist()
    top10_2 = df2.head(10)["name"].tolist()
    assert top10_1 == top10_2

