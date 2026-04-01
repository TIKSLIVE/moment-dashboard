import Link from "next/link";

export default function NotFound() {
  return (
    <main className="shell">
      <section className="panel panel-inner">
        <p className="label">Lien prive introuvable</p>
        <h1 className="section-title">Ce dashboard n’est plus disponible</h1>
        <p className="subtitle">
          Le token a peut-etre ete revoque ou l’evenement n’est pas encore
          synchronise.
        </p>
        <div className="button-row">
          <Link href="/" className="button">
            Retour a l’accueil
          </Link>
        </div>
      </section>
    </main>
  );
}
