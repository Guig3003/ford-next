"""Gera leads prioritários a partir do score de risco e do valor do cliente."""
from __future__ import annotations

import pandas as pd


def generate_leads(df: pd.DataFrame, top_n: int = 50) -> pd.DataFrame:
    """Seleciona os maiores leads por prioridade de contato."""
    return (
        df.sort_values(["prioridade", "score_risco"], ascending=[False, False])
        .head(top_n)
        .reset_index(drop=True)
    )
