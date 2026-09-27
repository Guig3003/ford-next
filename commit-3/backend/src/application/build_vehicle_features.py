"""Build de features por veículo e cálculo de gap relativo."""
from __future__ import annotations

import pandas as pd


def compute_gap_relativo(
    dias_desde_ultimo_servico: pd.Series,
    intervalo_mediano_esperado: pd.Series,
) -> pd.Series:
    """Gap relativo = dias sem serviço / intervalo médio esperado."""
    denominador = intervalo_mediano_esperado.mask(intervalo_mediano_esperado == 0)
    return (dias_desde_ultimo_servico / denominador).rename("gap_relativo")


def build_vehicle_features(df: pd.DataFrame) -> pd.DataFrame:
    """Constrói features por VIN a partir do histórico de manutenção."""
    resultado = df.copy()
    resultado["gap_relativo"] = compute_gap_relativo(
        resultado["dias_desde_ultimo_servico"],
        resultado["intervalo_mediano_esperado"],
    )
    return resultado
