import { notFound } from "next/navigation";
import { MetricGrid } from "@/components/metric-grid";
import { MultiColorBarChart, SalesBarChart } from "@/components/charts";
import { TransactionsTable } from "@/components/transactions-table";
import {
  formatApiLabel,
  formatDateTime,
  formatRelativeStatus,
  toStatusClass
} from "@/lib/format";
import { getDashboardByToken } from "@/lib/repository";

export default async function OrganizerDashboardPage({
  params
}: {
  params: Promise<{ token: string }>;
}) {
  const { token } = await params;
  const dashboard = await getDashboardByToken(token);

  if (!dashboard) {
    notFound();
  }

  return (
    <main className="shell">
      <section className="panel panel-inner">
        <div className="split">
          <div>
            <p className="label">Dashboard organisateur</p>
            <h1 className="section-title" style={{ fontSize: 42 }}>
              {dashboard.event.name}
            </h1>
            <p className="subtitle">
              {dashboard.access.organizerName} • {dashboard.event.sellerName} •{" "}
              {dashboard.event.currency}
            </p>
          </div>
          <span className={`status ${toStatusClass(dashboard.syncState.syncStatus)}`}>
            {formatApiLabel(dashboard.syncState.syncStatus)}
          </span>
        </div>
        <div className="grid cols-3" style={{ marginTop: 24 }}>
          <div className="card">
            <p className="label">Date / heure</p>
            <p className="metric" style={{ fontSize: 22 }}>
              {formatDateTime(dashboard.event.start)}
            </p>
          </div>
          <div className="card">
            <p className="label">saleStatus</p>
            <p className="metric" style={{ fontSize: 22 }}>
              {formatApiLabel(dashboard.event.saleStatus)}
            </p>
          </div>
          <div className="card">
            <p className="label">Derniere synchronisation</p>
            <p className="metric" style={{ fontSize: 22 }}>
              {formatRelativeStatus(dashboard.event.lastSyncedAt)}
            </p>
          </div>
        </div>
      </section>

      <section className="panel panel-inner" style={{ marginTop: 20 }}>
        <p className="label">KPI ventes</p>
        <h2 className="section-title">Resume de vente</h2>
        <MetricGrid kpis={dashboard.kpis} currency={dashboard.event.currency} />
      </section>

      <section className="grid cols-2" style={{ marginTop: 20 }}>
        <div className="panel panel-inner">
          <p className="label">Analyse</p>
          <h2 className="section-title">Ventes par jour</h2>
          <SalesBarChart data={dashboard.salesByDay} />
        </div>
        <div className="panel panel-inner">
          <p className="label">Analyse</p>
          <h2 className="section-title">Ventes par heure</h2>
          <SalesBarChart data={dashboard.salesByHour} color="#124c46" />
        </div>
        <div className="panel panel-inner">
          <p className="label">Billetterie</p>
          <h2 className="section-title">Par type de billet</h2>
          <MultiColorBarChart data={dashboard.salesByTicketType} />
        </div>
        <div className="panel panel-inner">
          <p className="label">Billetterie</p>
          <h2 className="section-title">Par categorie</h2>
          <MultiColorBarChart data={dashboard.salesByCategory} />
        </div>
      </section>

      <section className="panel panel-inner" style={{ marginTop: 20 }}>
        <div className="split">
          <div>
            <p className="label">Transactions recentes</p>
            <h2 className="section-title">Detail lecture seule</h2>
          </div>
          <span className="muted">
            Webhook: {formatDateTime(dashboard.syncState.lastWebhookAt)}
          </span>
        </div>
        <TransactionsTable transactions={dashboard.transactions} />
      </section>
    </main>
  );
}
