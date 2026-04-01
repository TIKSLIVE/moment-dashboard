import { AdminSellerForm } from "@/components/admin-seller-form";
import { AppNav } from "@/components/nav";
import { listSellers } from "@/lib/repository";
import { formatDateTime } from "@/lib/format";

export default async function AdminSellersPage() {
  const sellers = await listSellers();

  return (
    <main className="shell">
      <AppNav current="/admin/sellers" />
      <div className="grid">
        <AdminSellerForm />
        <section className="panel panel-inner">
          <div className="split">
            <div>
              <p className="label">Sellers configures</p>
              <h2 className="section-title">Configuration serveur vivenu</h2>
            </div>
            <span className="status synchronized">{sellers.length} actifs</span>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Nom</th>
                  <th>Seller ID</th>
                  <th>Statut</th>
                  <th>Maj</th>
                </tr>
              </thead>
              <tbody>
                {sellers.map((seller) => (
                  <tr key={seller.id}>
                    <td>{seller.name}</td>
                    <td>{seller.sellerId}</td>
                    <td>
                      <span className={`status ${seller.active ? "synchronized" : "pending"}`}>
                        {seller.active ? "active" : "inactive"}
                      </span>
                    </td>
                    <td>{formatDateTime(seller.updatedAt)}</td>
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
