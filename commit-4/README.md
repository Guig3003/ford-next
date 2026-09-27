# Commit 4 — Camada de apresentação (componentes e telas)

## Objetivo
Entregar a interface completa do aplicativo com tema, componentes reutilizáveis e telas do Expo Router.

## Arquivos que entram aqui
- `src/presentation/` — componentes React Native
  - `HomeScreen.tsx` — painel principal com KPIs
  - `TrendScreen.tsx` — gráfico de tendência e rankings
  - `AnomaliesScreen.tsx` — painel de anomalias
  - `LeadsScreen.tsx` — fila de leads com ação prioritária
  - Componentes menores (Card, KpiCard, LeadsTable, etc.)
  - `theme.ts` — cores, tipografia e espaçamento
  - `styles.ts` — estilos globais
- `app/` — estrutura de rotas Expo Router
  - `(tabs)/index.tsx` — abas de navegação
  - `(tabs)/trend.tsx`, `anomalias.tsx`, `leads.tsx`
  - `filtros-modal.tsx` — modal de filtros

## O que o usuário vê
Interfae completa, responsiva, 100% offline, pronta para usar no Android/iOS/web.
