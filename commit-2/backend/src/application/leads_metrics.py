"""Distribuição do score de risco dos leads — schema de GET /api/leads/distribuicao-score."""
from __future__ import annotations

import pandas as pd

N_FAIXAS_PADRAO = 10


def compute_score_distribution(df: pd.DataFrame, n_faixas: int = N_FAIXAS_PADRAO) -> list[dict]:
    limites = [i / n_faixas for i in range(n_faixas + 1)]
    faixas = pd.cut(df["score"], bins=limites, include_lowest=True, right=True)

    contagem = faixas.value_counts().sort_index()

    return [
        {
            "faixaInicio": round(max(intervalo.left, 0.0) * 100, 1),
            "faixaFim": round(intervalo.right * 100, 1),
            "quantidade": int(quantidade),
        }
        for intervalo, quantidade in contagem.items()
    ]
