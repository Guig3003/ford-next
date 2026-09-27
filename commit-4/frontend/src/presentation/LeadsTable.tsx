import type { Lead } from "../domain/types";

export default function LeadsTable({ concessionaria }: { concessionaria?: string }) {
  const leads: Lead[] = [
    { vin: "VIN-001", score: 0.92, nomeModelo: "Ranger", concessionaria: concessionaria ?? "Rede Ford" },
    { vin: "VIN-002", score: 0.86, nomeModelo: "Ka", concessionaria: concessionaria ?? "Rede Ford" },
  ];

  return (
    <div className="tabela-wrap">
      <table className="tabela-leads">
        <thead>
          <tr>
            <th>VIN</th>
            <th>Modelo</th>
            <th>Score</th>
            <th>Concessionária</th>
          </tr>
        </thead>
        <tbody>
          {leads.map((lead) => (
            <tr key={lead.vin}>
              <td>{lead.vin}</td>
              <td>{lead.nomeModelo}</td>
              <td>{lead.score.toFixed(2)}</td>
              <td>{lead.concessionaria}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
