# Commit 2 — Camada de domínio e tipos de negócio

## Objetivo
Definir os contratos de dados (types, enums) e as regras de negócio puras que são compartilhadas entre application e presentation.

## Arquivos que entram aqui
- `src/domain/types.ts` — interfaces e tipos (VinShareFiltros, Lead, CompetenciaInfo, etc.)
- `src/domain/severidade.ts` — lógica de classificação de risco (baixo/médio/alto)
- `src/domain/competencia.ts` — cálculo e formatação de períodos (YYYY-MM)
- Testes correspondentes (`*.test.ts`)

## O que você vai encontrar
Regras de negócio 100% testadas e independentes de React, garantindo que qualquer camada consuma dados com o tipo correto.

## Exemplo de regra
- Severidade: gap relativo > 2.0 → alto risco
- Competência: período em mês (2024-01, 2024-02, ...)
