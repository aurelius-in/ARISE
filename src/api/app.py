from __future__ import annotations

from fastapi import FastAPI, UploadFile, File
import pandas as pd

from src.core.pipeline import score_dataframe


app = FastAPI(title="ARISE API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/score")
async def score_csv(file: UploadFile = File(...), top_k: int = 20):
    df = pd.read_csv(file.file)
    df_scored = score_dataframe(df)
    top = df_scored.head(int(top_k)).to_dict(orient="records")
    return {"count": len(top), "items": top}


