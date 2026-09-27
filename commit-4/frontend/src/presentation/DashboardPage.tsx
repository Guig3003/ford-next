import { useCallback, useEffect, useRef, useState } from "react";
import { useAnomaliesData } from "../application/useAnomaliesData";
import { useCatalogo } from "../application/useCatalogo";
import { useVinShareData } from "../application/useVinShareData";
import type { VinShareFiltros } from "../domain/types";
import AcaoPrioritariaKpiCard from "./AcaoPrioritariaKpiCard";
import AnomaliasPanel from "./AnomaliasPanel";
import FiltrosBar from "./FiltrosBar";
import KpiCard, { formatarInteiro, type ComparacaoKpi } from "./KpiCard";
import LeadsTable from "./LeadsTable";
import ResumoFiltros from "./ResumoFiltros";
import ScoreDistributionChart from "./ScoreDistributionChart";
import TrendChart from "./TrendChart";
import VinShareConcessionariaChart from "./VinShareConcessionariaChart";
import VinShareModeloChart from "./VinShareModeloChart";

function limparVazios(filtros: VinShareFiltros): VinShareFiltros {
  const resultado: VinShareFiltros = {};
  for (const [chave, valor] of Object.entries(filtros)) {
    if (valor !== undefined && valor !== "") {
      resultado[chave as keyof VinShareFiltros] = valor;
    }
  }
  return resultado;
}

function paraCompetencia(dataIso?: string): string | undefined {
  return dataIso?.slice(0, 7);
}

export default function DashboardPage() {
  const [filtros, setFiltros] = useState<VinShareFiltros>({});
  const { data, loading, error, recarregar } = useVinShareData(filtros);
  const { data: catalogo } = useCatalogo();
  const periodoPadraoAplicado = useRef(false);

  useEffect(() => {
    if (periodoPadraoAplicado.current || !catalogo?.periodoDisponivel) return;
    periodoPadraoAplicado.current = true;

    setFiltros((atual) =>
      atual.periodoInicio || atual.periodoFim
        ? atual
        : {
            ...atual,
            periodoInicio: catalogo.periodoDisponivel!.inicio,
            periodoFim: catalogo.periodoDisponivel!.fim
          }
    );
  }, [catalogo]);

  const { data: referencia } = useVinShareData({
    periodoInicio: filtros.periodoInicio,
    periodoFim: filtros.periodoFim
  });

  const {
    data: anomalias,
    loading: carregandoAnomalias,
    error: erroAnomalias,
    recarregar: recarregarAnomalias
  } = useAnomaliesData();

  const atualizarFiltros = useCallback((alteracao: Partial<VinShareFiltros>) => {
    setFiltros((atual) => limparVazios({ ...atual, ...alteracao }));
  }, []);

  const limparFiltros = useCallback(() => {
    setFiltros({});
  }, []);

  const filtrarPelaAnomalia = useCallback((filtro: Partial<VinShareFiltros>) => {
    setFiltros((atual) => limparVazios({ ...atual, ...filtro }));

    const suave = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    window.scrollTo({ top: 0, behavior: suave ? "smooth" : "auto" });
  }, []);

  const temFiltroDemografico = Boolean(
    filtros.concessionaria || filtros.modelo || filtros.faixaIdade || filtros.tipoServico
  );

  const comparacao: ComparacaoKpi | undefined =
    temFiltroDemografico && referencia
      ? { base: referencia.vinShareEstimado, rotuloBase: "média da rede" }
      : undefined;

  const contexto = data
    ? `${formatarInteiro(data.totalComServico)} de ${formatarInteiro(
        data.totalVeiculosElegiveis
      )} veículos elegíveis passaram pela rede oficial`
    : undefined;

  return (
    <div className="pagina">
      <header className="cabecalho">
        <div className="marca">
          <span className="marca-selo" aria-hidden="true">Ford</span>
          <div>
            <h1 className="cabecalho-titulo">VIN Share Intelligence Hub</h1>
            <p className="cabecalho-subtitulo">
              Retenção de pós-venda da rede Ford: onde o VIN Share está caindo, por que, e quem
              contatar primeiro.
            </p>
          </div>
        </div>
      </header>

      <main className="conteudo">
        <section className="secao" aria-labelledby="secao-filtros">
          <h2 className="secao-titulo" id="secao-filtros">Filtros</h2>
          <FiltrosBar
            filtros={filtros}
            onChange={atualizarFiltros}
            onLimpar={limparFiltros}
            catalogo={catalogo}
          />
          <ResumoFiltros filtros={filtros} />
        </section>

        <section className="secao" aria-labelledby="secao-kpi">
          <h2 className="secao-titulo" id="secao-kpi">Indicadores</h2>
          <div className="indicadores">
            <KpiCard
              label="VIN Share estimado"
              valor={data?.vinShareEstimado}
              contexto={contexto}
              comparacao={comparacao}
              loading={loading}
              erro={error ? error.message : null}
              onTentarNovamente={recarregar}
            />

            <KpiCard
              label="Anomalias detectadas"
              valor={anomalias?.length}
              unidade=""
              casasDecimais={0}
              loading={carregandoAnomalias}
              erro={erroAnomalias ? erroAnomalias.message : null}
              onTentarNovamente={recarregarAnomalias}
            />

            <AcaoPrioritariaKpiCard concessionaria={filtros.concessionaria} />
          </div>
        </section>

        <section className="secao" aria-labelledby="secao-tendencia">
          <h2 className="secao-titulo" id="secao-tendencia">Tendência de VIN Share</h2>
          <TrendChart
            periodoInicio={paraCompetencia(filtros.periodoInicio)}
            periodoFim={paraCompetencia(filtros.periodoFim)}
            modelos={catalogo?.modelos ?? []}
          />
        </section>

        <section className="secao" aria-labelledby="secao-leads">
          <h2 className="secao-titulo" id="secao-leads">Leads priorizados</h2>
          <LeadsTable concessionaria={filtros.concessionaria} />
        </section>
      </main>
    </div>
  );
}
