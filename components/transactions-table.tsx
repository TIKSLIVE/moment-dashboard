import {
  formatApiLabel,
  formatDateTime,
  formatMoney,
  formatNumber,
  toStatusClass
} from "@/lib/format";
import type { TransactionRecord } from "@/types/domain";

export function TransactionsTable({
  transactions
}: {
  transactions: TransactionRecord[];
}) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Transaction ID</th>
            <th>Email client</th>
            <th>Types de billets</th>
            <th>Quantite</th>
            <th>Montant brut</th>
            <th>Montant reel</th>
            <th>Statut</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.id}>
              <td>{formatDateTime(transaction.createdAt)}</td>
              <td>{transaction.transactionId}</td>
              <td>{transaction.email}</td>
              <td>{transaction.ticketTypeNames.join(", ")}</td>
              <td>{formatNumber(transaction.quantity)}</td>
              <td>{formatMoney(transaction.regularPrice, transaction.currency)}</td>
              <td>{formatMoney(transaction.realPrice, transaction.currency)}</td>
              <td>
                <span className={`status ${toStatusClass(transaction.status)}`}>
                  {formatApiLabel(transaction.status)}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
