"""Métricas do VIN Share por concessionária, modelo e tendência temporal."""
from __future__ import annotations

import pandas as pd


def compute_vin_share_mean(df: pd.DataFrame, value_col: str = "vin_share") -> float:
    return float(df[value_col].mean())


def compute_vin_share_by_model(df: pd.DataFrame, model_col: str = "ModelName", value_col: str = "vin_share") -> pd.DataFrame:
    return (
        df.groupby(model_col, as_index=False)[value_col]
        .mean()
        .rename(columns={value_col: "vin_share_medio"})
        .sort_values("vin_share_medio", ascending=False)
    )
