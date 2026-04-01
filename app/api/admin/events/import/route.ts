import { NextResponse } from "next/server";
import { z } from "zod";
import { buildOrganizerUrl, generateAccessToken } from "@/lib/access";

const importSchema = z.object({
  sellerId: z.string().min(2),
  eventId: z.string().min(2),
  organizerName: z.string().min(2)
});

export async function POST(request: Request) {
  const payload = importSchema.parse(await request.json());
  const token = generateAccessToken();

  return NextResponse.json({
    ok: true,
    message:
      "Event import request accepted. Call GET /api/events/{id} and GET /api/transactions/rich here in production.",
    event: {
      eventId: payload.eventId,
      sellerId: payload.sellerId
    },
    access: {
      organizerName: payload.organizerName,
      token,
      url: buildOrganizerUrl(token)
    }
  });
}
