import { demoAccess, demoEvents, demoSellers, demoSyncStates, demoTransactions } from "@/lib/demo-data";
import { buildDashboard } from "@/lib/dashboard";
import type {
  EventAccessRecord,
  EventRecord,
  OrganizerDashboard,
  Seller,
  SyncStateRecord,
  TransactionRecord
} from "@/types/domain";

function useDemoData() {
  return process.env.USE_DEMO_DATA !== "false";
}

export async function listSellers(): Promise<Seller[]> {
  if (useDemoData()) return demoSellers;
  return [];
}

export async function listEvents(): Promise<
  Array<EventRecord & { access?: EventAccessRecord; syncState?: SyncStateRecord }>
> {
  if (!useDemoData()) return [];

  return demoEvents.map((event) => ({
    ...event,
    access: demoAccess.find((access) => access.eventId === event.eventId),
    syncState: demoSyncStates.find((syncState) => syncState.eventId === event.eventId)
  }));
}

export async function getDashboardByToken(
  token: string
): Promise<OrganizerDashboard | null> {
  const access = demoAccess.find(
    (entry) => entry.accessToken === token && entry.active
  );
  if (!access) return null;

  const event = demoEvents.find(
    (entry) => entry.eventId === access.eventId
  );
  const syncState = demoSyncStates.find(
    (entry) => entry.eventId === access.eventId
  );
  const transactions = demoTransactions.filter(
    (entry) => entry.eventId === access.eventId
  );

  if (!event || !syncState) return null;

  return buildDashboard({
    event,
    access,
    syncState,
    transactions
  });
}

export async function getEventTransactions(eventId: string): Promise<TransactionRecord[]> {
  return demoTransactions.filter((entry) => entry.eventId === eventId);
}
