"""Split temporal de treino/teste para o modelo de risco de evasão.

Split temporal (em vez de aleatório) simula a situação real de produção: o modelo é
treinado só com o passado e avaliado contra dados que, na época do treino, ainda não
haviam acontecido.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from src.domain.risk_label import compute_em_risco

TRAIN_FRACTION_PADRAO = 0.8
THRESHOLDS_COMPARACAO_PADRAO: tuple[float, ...] = (1.2, 1.5, 2.0)
FEATURE_COLUMNS: tuple[str, ...] = ("idade_dias", "gap_com_fallback", "n_servicos")
TARGET_COLUMN = "em_risco"
TREE_MAX_DEPTH_PADRAO = 4
RANDOM_STATE_PADRAO = 42

RiskClassifier = Pipeline | DecisionTreeClassifier


def compute_cutoff_date(dates: pd.Series, train_fraction: float = TRAIN_FRACTION_PADRAO) -> pd.Timestamp:
    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction deve estar entre 0 e 1 (exclusive)")
    return dates.dropna().quantile(train_fraction)


def temporal_train_test_split(
    df: pd.DataFrame,
    date_col: str,
    train_fraction: float = TRAIN_FRACTION_PADRAO,
    cutoff_date: pd.Timestamp | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Timestamp]:
    dados = df.dropna(subset=[date_col]).sort_values(date_col)

    if cutoff_date is None:
        cutoff_date = compute_cutoff_date(dados[date_col], train_fraction)

    treino = dados[dados[date_col] <= cutoff_date].copy()
    teste = dados[dados[date_col] > cutoff_date].copy()

    return treino, teste, cutoff_date


def _feature_matrix_e_alvo(
    df: pd.DataFrame, feature_columns: tuple[str, ...], target_column: str
) -> tuple[pd.DataFrame, pd.Series]:
    dados = df.dropna(subset=[*feature_columns, target_column])
    X = dados[list(feature_columns)]
    y = dados[target_column].astype("boolean").astype(int)

    return X, y


def train_logistic_regression(
    treino: pd.DataFrame,
    feature_columns: tuple[str, ...] = FEATURE_COLUMNS,
    target_column: str = TARGET_COLUMN,
) -> Pipeline:
    X_treino, y_treino = _feature_matrix_e_alvo(treino, feature_columns, target_column)

    modelo = make_pipeline(StandardScaler(), LogisticRegression())
    modelo.fit(X_treino, y_treino)

    return modelo


def evaluate_auc(
    modelo: RiskClassifier,
    teste: pd.DataFrame,
    feature_columns: tuple[str, ...] = FEATURE_COLUMNS,
    target_column: str = TARGET_COLUMN,
) -> float:
    X_teste, y_teste = _feature_matrix_e_alvo(teste, feature_columns, target_column)
    y_proba = modelo.predict_proba(X_teste)[:, 1]

    return roc_auc_score(y_teste, y_proba)


def precision_at_top_k(y_true: pd.Series, y_score: np.ndarray, k_fraction: float) -> float:
    if not 0 < k_fraction <= 1:
        raise ValueError("k_fraction deve estar entre 0 (exclusive) e 1 (inclusive)")

    y_true_array = np.asarray(y_true)
    y_score_array = np.asarray(y_score)

    n = len(y_true_array)
    k = max(1, math.ceil(n * k_fraction))

    top_k_idx = np.argsort(-y_score_array, kind="stable")[:k]

    return float(y_true_array[top_k_idx].mean())
