# Commit 3 — Camada de aplicação (hooks e contexto de filtros)

## Objetivo
Implementar os hooks de dados reutilizáveis (useLeads, useVinShareData, useTrendData, etc.) e o contexto React para compartilhar filtros entre telas.

## Arquivos que entram aqui
- `src/application/` — pasta com todos os hooks
  - `useLeads.ts` — buscar leads com filtro
  - `useVinShareData.ts` — dados de VIN Share para KPI
  - `useTrendData.ts` — histórico mensal de VIN Share
  - `useAnomaliesData.ts` — detectar anomalias
  - `useCatalogo.ts` — modelos, concessionárias, período disponível
  - E mais...
- `src/infrastructure/mockData.ts` — gerador de dados determinístico
- Testes dos hooks

## O que faz
Cada hook é uma abstração entre a data source (mockData) e os componentes React, garantindo que a lógica seja testável e reutilizável.

## Exemplo
```typescript
const { data, loading, error } = useLeads({ concessionaria: 'SP-001' });
```
