import { decryptString } from "@/lib/crypto";

const VIVENU_API_BASE_URL =
  process.env.VIVENU_API_BASE_URL ?? "https://vivenu.dev/api";

export type VivenuListResponse<T> = {
  docs: T[];
  total: number;
};

export type VivenuEvent = {
  _id: string;
  sellerId: string;
  name: string;
  currency?: string;
  saleStatus?: string;
  start?: string;
  end?: string;
};

export type VivenuTicket = {
  _id?: string;
  ticketTypeId?: string;
  ticketTypeName?: string;
  categoryName?: string;
  price?: number;
};

export type VivenuTransactionRich = {
  _id: string;
  sellerId: string;
  eventId: string;
  email?: string;
  currency?: string;
  regularPrice?: number;
  realPrice?: number;
  paymentCharge?: number;
  innerCharge?: number;
  outerCharge?: number;
  status?: string;
  createdAt?: string;
  updatedAt?: string;
  tickets?: VivenuTicket[];
};

type VivenuRequestOptions = {
  path: string;
  apiKeyEncrypted: string;
  method?: "GET" | "POST";
  query?: Record<string, string | number | boolean | undefined>;
  body?: unknown;
};

export async function vivenuRequest<T>({
  path,
  apiKeyEncrypted,
  method = "GET",
  query,
  body
}: VivenuRequestOptions): Promise<T> {
  const apiKey = decryptString(apiKeyEncrypted);
  const url = new URL(`${VIVENU_API_BASE_URL}${path}`);

  Object.entries(query ?? {}).forEach(([key, value]) => {
    if (value !== undefined) {
      url.searchParams.set(key, String(value));
    }
  });

  const response = await fetch(url, {
    method,
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json"
    },
    body: body ? JSON.stringify(body) : undefined,
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`vivenu request failed with ${response.status}`);
  }

  return (await response.json()) as T;
}

export async function fetchVivenuEvent(
  apiKeyEncrypted: string,
  eventId: string
) {
  return vivenuRequest<VivenuEvent>({
    path: `/events/${eventId}`,
    apiKeyEncrypted
  });
}

export async function fetchVivenuTransactionsRich(
  apiKeyEncrypted: string,
  eventId: string,
  updatedAtGt?: string,
  top = 100,
  skip = 0
) {
  return vivenuRequest<VivenuListResponse<VivenuTransactionRich>>({
    path: `/transactions/rich`,
    apiKeyEncrypted,
    query: {
      event: eventId,
      "updatedAt[$gt]": updatedAtGt,
      top,
      skip
    }
  });
}
