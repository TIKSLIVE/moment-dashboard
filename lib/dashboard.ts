import type {
  DashboardKpis,
  OrganizerDashboard,
  SalesSeriesItem,
  TransactionRecord
} from "@/types/domain";

function groupToSeries(
  transactions: TransactionRecord[],
  keyGetter: (transaction: TransactionRecord) => string,
  valueGetter: (transaction: TransactionRecord) => number
) {
  const groups = new Map<string, number>();

  for (const transaction of transactions) {
    const key = keyGetter(transaction);
    groups.set(key, (groups.get(key) ?? 0) + valueGetter(transaction));
  }

  return Array.from(groups.entries())
    .map(([label, value]) => ({ label, value }))
    .sort((left, right) => left.label.localeCompare(right.label));
}

export function computeKpis(transactions: TransactionRecord[]): DashboardKpis {
  const totalTransactions = transactions.length;
  const totalTickets = transactions.reduce(
    (sum, transaction) => sum + transaction.quantity,
    0
  );
  const grossRevenue = transactions.reduce(
    (sum, transaction) => sum + transaction.regularPrice,
    0
  );
  const realRevenue = transactions.reduce(
    (sum, transaction) => sum + transaction.realPrice,
    0
  );
  const paymentCharge = transactions.reduce(
    (sum, transaction) => sum + transaction.paymentCharge,
    0
  );
  const innerCharge = transactions.reduce(
    (sum, transaction) => sum + transaction.innerCharge,
    0
  );
  const outerCharge = transactions.reduce(
    (sum, transaction) => sum + transaction.outerCharge,
    0
  );
  const cancellations = transactions.filter(
    (transaction) => transaction.status === "CANCELED"
  ).length;
  const partialRefunds = transactions.filter(
    (transaction) =>
      transaction.status === "PARTIALLY_CANCELED" ||
      transaction.status === "PARTIALLYCANCELED"
  ).length;

  return {
    totalTransactions,
    totalTickets,
    grossRevenue,
    realRevenue,
    paymentCharge,
    innerCharge,
    outerCharge,
    cancellations,
    partialRefunds,
    averageBasket: totalTransactions === 0 ? 0 : grossRevenue / totalTransactions
  };
}

export function computeSalesByDay(transactions: TransactionRecord[]) {
  return groupToSeries(
    transactions,
    (transaction) => transaction.createdAt.slice(0, 10),
    (transaction) => transaction.realPrice
  );
}

export function computeSalesByHour(transactions: TransactionRecord[]) {
  return groupToSeries(
    transactions,
    (transaction) => {
      const hour = new Date(transaction.createdAt).getHours();
      return `${hour.toString().padStart(2, "0")}:00`;
    },
    (transaction) => transaction.realPrice
  );
}

export function computeSalesByTicketType(transactions: TransactionRecord[]) {
  const groups = new Map<string, number>();

  for (const transaction of transactions) {
    for (const ticketType of transaction.ticketTypeNames) {
      groups.set(ticketType, (groups.get(ticketType) ?? 0) + transaction.quantity);
    }
  }

  return Array.from(groups.entries()).map(([label, value]) => ({ label, value }));
}

export function computeSalesByCategory(transactions: TransactionRecord[]) {
  return groupToSeries(
    transactions,
    (transaction) => transaction.ticketCategoryName,
    (transaction) => transaction.quantity
  );
}

export function buildDashboard(
  base: Omit<OrganizerDashboard, "kpis" | "salesByDay" | "salesByHour" | "salesByTicketType" | "salesByCategory">
): OrganizerDashboard {
  return {
    ...base,
    kpis: computeKpis(base.transactions),
    salesByDay: computeSalesByDay(base.transactions),
    salesByHour: computeSalesByHour(base.transactions),
    salesByTicketType: computeSalesByTicketType(base.transactions),
    salesByCategory: computeSalesByCategory(base.transactions)
  };
}

export function emptySeries(): SalesSeriesItem[] {
  return [];
}
