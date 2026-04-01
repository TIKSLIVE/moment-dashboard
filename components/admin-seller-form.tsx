export function AdminSellerForm() {
  return (
    <div className="panel panel-inner">
      <div className="split">
        <div>
          <p className="label">Admin MOMENT</p>
          <h2 className="section-title">Ajouter un seller vivenu</h2>
        </div>
        <span className="status pending">Cle API cote serveur</span>
      </div>
      <form className="form-grid">
        <label className="field">
          <span>Nom interne</span>
          <input placeholder="MOMENT France" />
        </label>
        <label className="field">
          <span>sellerId</span>
          <input placeholder="seller_moment_fr" />
        </label>
        <label className="field full">
          <span>API key</span>
          <input placeholder="sk_live_..." type="password" />
        </label>
        <div className="field">
          <button type="button" className="button">
            Enregistrer le seller
          </button>
        </div>
      </form>
    </div>
  );
}
