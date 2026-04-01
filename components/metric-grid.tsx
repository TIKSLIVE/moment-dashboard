import { formatMoney, formatNumber } from "@/lib/format";
import type { DashboardKpis } from "@/types/domain";

export function MetricGrid({
  kpis,
  currency
}: {
  kpis: DashboardKpis;
  currency: string;
}) {
  const items = [
    ["Transactions", formatNumber(kpis.totalTransactions)],
    ["Billets vendus", formatNumber(kpis.totalTickets)],
    ["CA brut", formatMoney(kpis.grossRevenue, currency)],
    ["CA reel", formatMoney(kpis.realRevenue, currency)],
    ["Payment charge", formatMoney(kpis.paymentCharge, currency)],
    ["Inner charge", formatMoney(kpis.innerCharge, currency)],
    ["Outer charge", formatMoney(kpis.outerCharge, currency)],
    ["Annulations", formatNumber(kpis.cancellations)],
    ["Remboursements partiels", formatNumber(kpis.partialRefunds)],
    ["Panier moyen", formatMoney(kpis.averageBasket, currency)]
  ];

  return (
    <div className="grid cols-3">
      {items.map(([label, value]) => (
        <div key={label} className="card">
          <p className="label">{label}</p>
          <p className="metric">{value}</p>
        </div>
      ))}
    </div>
  );
}
