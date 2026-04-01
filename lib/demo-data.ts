import type {
  EventAccessRecord,
  EventRecord,
  Seller,
  SyncStateRecord,
  TransactionRecord
} from "@/types/domain";

const iso = (value: string) => new Date(value).toISOString();

export const demoSellers: Seller[] = [
  {
    id: "seller_1",
    sellerId: process.env.VIVENU_DEMO_SELLER_ID ?? "seller_moment_fr",
    name: "MOMENT France",
    active: true,
    createdAt: iso("2026-03-01T10:00:00Z"),
    updatedAt: iso("2026-03-29T09:12:00Z")
  }
];

export const demoEvents: EventRecord[] = [
  {
    id: "evt_1",
    eventId: process.env.VIVENU_DEMO_EVENT_ID ?? "viv_event_12345",
    sellerId: process.env.VIVENU_DEMO_SELLER_ID ?? "seller_moment_fr",
    name: "Sunset Rooftop Session",
    start: iso("2026-05-15T18:30:00Z"),
    end: iso("2026-05-16T00:00:00Z"),
    currency: "EUR",
    saleStatus: "onSale",
    lastSyncedAt: iso("2026-04-01T10:00:00Z"),
    sellerName: "MOMENT France"
  }
];

export const demoAccess: EventAccessRecord[] = [
  {
    id: "access_1",
    eventId: process.env.VIVENU_DEMO_EVENT_ID ?? "viv_event_12345",
    accessToken: process.env.ORGANIZER_ACCESS_TOKEN ?? "demo-organizer-token",
    organizerName: "Rooftop Collective",
    active: true,
    createdAt: iso("2026-03-28T08:00:00Z"),
    lastViewedAt: iso("2026-04-01T09:50:00Z")
  }
];

export const demoSyncStates: SyncStateRecord[] = [
  {
    id: "sync_1",
    eventId: process.env.VIVENU_DEMO_EVENT_ID ?? "viv_event_12345",
    lastTransactionsSyncAt: iso("2026-04-01T10:00:00Z"),
    lastWebhookAt: iso("2026-04-01T09:56:00Z"),
    syncStatus: "synchronized",
    lastError: null,
    updatedAt: iso("2026-04-01T10:00:00Z")
  }
];

export const demoTransactions: TransactionRecord[] = [
  {
    id: "txn_1",
    transactionId: "tx-001",
    eventId: process.env.VIVENU_DEMO_EVENT_ID ?? "viv_event_12345",
    sellerId: process.env.VIVENU_DEMO_SELLER_ID ?? "seller_moment_fr",
    createdAt: iso("2026-03-30T09:00:00Z"),
    updatedAt: iso("2026-03-30T09:00:00Z"),
    currency: "EUR",
    regularPrice: 39,
    realPrice: 36,
    paymentCharge: 1.8,
    innerCharge: 0.7,
    outerCharge: 0.5,
    email: "lea@example.com",
    status: "COMPLETE",
    ticketTypeNames: ["Early Bird"],
    ticketCategoryName: "General Admission",
    quantity: 2
  },
  {
    id: "txn_2",
    transactionId: "tx-002",
    eventId: process.env.VIVENU_DEMO_EVENT_ID ?? "viv_event_12345",
    sellerId: process.env.VIVENU_DEMO_SELLER_ID ?? "seller_moment_fr",
    createdAt: iso("2026-03-30T18:30:00Z"),
    updatedAt: iso("2026-03-31T08:10:00Z"),
    currency: "EUR",
    regularPrice: 78,
    realPrice: 74,
    paymentCharge: 3.4,
    innerCharge: 1.4,
    outerCharge: 1.2,
    email: "sam@example.com",
    status: "COMPLETE",
    ticketTypeNames: ["Regular", "Drink add-on"],
    ticketCategoryName: "VIP",
    quantity: 3
  },
  {
    id: "txn_3",
    transactionId: "tx-003",
    eventId: process.env.VIVENU_DEMO_EVENT_ID ?? "viv_event_12345",
    sellerId: process.env.VIVENU_DEMO_SELLER_ID ?? "seller_moment_fr",
    createdAt: iso("2026-03-31T20:15:00Z"),
    updatedAt: iso("2026-03-31T20:50:00Z"),
    currency: "EUR",
    regularPrice: 26,
    realPrice: 0,
    paymentCharge: 0,
    innerCharge: 0,
    outerCharge: 0,
    email: "nora@example.com",
    status: "CANCELED",
    ticketTypeNames: ["Regular"],
    ticketCategoryName: "General Admission",
    quantity: 1
  },
  {
    id: "txn_4",
    transactionId: "tx-004",
    eventId: process.env.VIVENU_DEMO_EVENT_ID ?? "viv_event_12345",
    sellerId: process.env.VIVENU_DEMO_SELLER_ID ?? "seller_moment_fr",
    createdAt: iso("2026-04-01T08:00:00Z"),
    updatedAt: iso("2026-04-01T08:00:00Z"),
    currency: "EUR",
    regularPrice: 52,
    realPrice: 48,
    paymentCharge: 2.2,
    innerCharge: 0.8,
    outerCharge: 0.8,
    email: "max@example.com",
    status: "PARTIALLY_CANCELED",
    ticketTypeNames: ["Regular"],
    ticketCategoryName: "General Admission",
    quantity: 2
  }
];
