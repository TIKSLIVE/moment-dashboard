export type Seller = {
  id: string;
  sellerId: string;
  name: string;
  active: boolean;
  createdAt: string;
  updatedAt: string;
};

export type EventRecord = {
  id: string;
  eventId: string;
  sellerId: string;
  name: string;
  start: string | null;
  end: string | null;
  currency: string;
  saleStatus: string;
  lastSyncedAt: string | null;
  sellerName: string;
};

export type TransactionRecord = {
  id: string;
  transactionId: string;
  eventId: string;
  sellerId: string;
  createdAt: string;
  updatedAt: string;
  currency: string;
  regularPrice: number;
  realPrice: number;
  paymentCharge: number;
  innerCharge: number;
  outerCharge: number;
  email: string;
  status: string;
  ticketTypeNames: string[];
  ticketCategoryName: string;
  quantity: number;
};

export type EventAccessRecord = {
  id: string;
  eventId: string;
  accessToken: string;
  organizerName: string;
  active: boolean;
  createdAt: string;
  lastViewedAt: string | null;
};

export type SyncStateRecord = {
  id: string;
  eventId: string;
  lastTransactionsSyncAt: string | null;
  lastWebhookAt: string | null;
  syncStatus: string;
  lastError: string | null;
  updatedAt: string;
};

export type SalesSeriesItem = {
  label: string;
  value: number;
};

export type DashboardKpis = {
  totalTransactions: number;
  totalTickets: number;
  grossRevenue: number;
  realRevenue: number;
  paymentCharge: number;
  innerCharge: number;
  outerCharge: number;
  cancellations: number;
  partialRefunds: number;
  averageBasket: number;
};

export type OrganizerDashboard = {
  event: EventRecord;
  access: EventAccessRecord;
  syncState: SyncStateRecord;
  transactions: TransactionRecord[];
  kpis: DashboardKpis;
  salesByDay: SalesSeriesItem[];
  salesByHour: SalesSeriesItem[];
  salesByTicketType: SalesSeriesItem[];
  salesByCategory: SalesSeriesItem[];
};
