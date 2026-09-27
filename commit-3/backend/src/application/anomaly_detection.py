"""Detecção de anomalias no VIN Share e no histórico de serviço."""
from __future__ import annotations

import pandas as pd


def detect_anomalias(df: pd.DataFrame, col: str = "vin_share") -> pd.DataFrame:
    """Marca valores fora do comportamento esperado do histórico."""
    media = df[col].mean()
    desvio = df[col].std(ddof=0)
    zscore = (df[col] - media) / desvio if desvio else 0
    resultado = df.copy()
    resultado["anomalia"] = zscore.abs() > 3
    return resultado
