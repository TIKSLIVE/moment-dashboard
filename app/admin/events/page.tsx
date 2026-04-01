import { AdminEventForm } from "@/components/admin-event-form";
import { AppNav } from "@/components/nav";
import { buildOrganizerUrl } from "@/lib/access";
import { formatDateTime } from "@/lib/format";
import { listEvents } from "@/lib/repository";

export default async function AdminEventsPage() {
  const events = await listEvents();

  return (
    <main className="shell">
      <AppNav current="/admin/events" />
      <div className="grid">
        <AdminEventForm />
        <section className="panel panel-inner">
          <div className="split">
            <div>
              <p className="label">Pilotage evenements</p>
              <h2 className="section-title">Import, sync et acces organisateur</h2>
            </div>
            <span className="status synchronized">{events.length} evenement(s)</span>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Evenement</th>
                  <th>Seller</th>
                  <th>Etat</th>
                  <th>Derniere sync</th>
                  <th>Lien prive</th>
                </tr>
              </thead>
              <tbody>
                {events.map((event) => (
                  <tr key={event.id}>
                    <td>
                      <div>{event.name}</div>
                      <div className="muted">{event.eventId}</div>
                    </td>
                    <td>{event.sellerName}</td>
                    <td>
                      <span className={`status ${event.syncState?.syncStatus ?? "pending"}`}>
                        {event.syncState?.syncStatus ?? "pending"}
                      </span>
                    </td>
                    <td>{formatDateTime(event.lastSyncedAt)}</td>
                    <td>
                      {event.access ? (
                        <a
                          href={buildOrganizerUrl(event.access.accessToken)}
                          className="button-secondary"
                        >
                          Ouvrir
                        </a>
                      ) : (
                        "Aucun lien"
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </main>
  );
}
