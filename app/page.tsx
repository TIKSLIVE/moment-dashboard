import type { Route } from "next";
import Link from "next/link";

export default function HomePage() {
  const organizerAccessToken =
    process.env.ORGANIZER_ACCESS_TOKEN ?? "demo-organizer-token";

  return (
    <main className="shell">
      <section className="hero">
        <div className="panel panel-inner">
          <span className="eyebrow">MVP externe</span>
          <h1 className="title">MOMENT x vivenu Dashboard</h1>
          <p className="subtitle">
            Un cockpit de vente lecture seule par evenement, avec acces prive
            organisateur, sync serveur et administration MOMENT centralisee.
          </p>
          <div className="button-row">
            <Link href="/admin/sellers" className="button">
              Ouvrir l’admin
            </Link>
            <Link
              href={`/o/${organizerAccessToken}` as Route}
              className="button-secondary"
            >
              Voir le dashboard organisateur
            </Link>
          </div>
        </div>
        <div className="panel panel-inner stack">
          <div className="card">
            <p className="label">Acces</p>
            <p className="metric">Lien secret unique</p>
            <p className="metric-sub">
              Aucun token vivenu cote navigateur, revocation immediate.
            </p>
          </div>
          <div className="card">
            <p className="label">Sync</p>
            <p className="metric">Cron + webhook</p>
            <p className="metric-sub">
              Reconciliation toutes les 10 minutes avec mise a jour
              incrementale.
            </p>
          </div>
          <div className="card">
            <p className="label">Mode MVP</p>
            <p className="metric">Admin + organisateur</p>
            <p className="metric-sub">
              Ecrans prets pour brancher une base Postgres/Supabase et l’API
              vivenu.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
