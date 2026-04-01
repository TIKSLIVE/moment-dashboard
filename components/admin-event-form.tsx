export function AdminEventForm() {
  return (
    <div className="panel panel-inner">
      <div className="split">
        <div>
          <p className="label">Import manuel</p>
          <h2 className="section-title">Ajouter un evenement par eventId</h2>
        </div>
        <span className="status synchronized">Sync initial + lien prive</span>
      </div>
      <form className="form-grid">
        <label className="field">
          <span>sellerId</span>
          <select defaultValue="">
            <option value="" disabled>
              Choisir un sellerId
            </option>
            <option value="seller_moment_fr">MOMENT France</option>
          </select>
        </label>
        <label className="field">
          <span>eventId</span>
          <input placeholder="viv_event_12345" />
        </label>
        <label className="field full">
          <span>Nom organisateur</span>
          <input placeholder="Rooftop Collective" />
        </label>
        <div className="field">
          <button type="button" className="button">
            Importer l’evenement
          </button>
        </div>
      </form>
    </div>
  );
}
