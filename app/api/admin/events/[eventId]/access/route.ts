import { NextResponse } from "next/server";
import { buildOrganizerUrl, generateAccessToken } from "@/lib/access";

export async function POST(
  _request: Request,
  { params }: { params: Promise<{ eventId: string }> }
) {
  const { eventId } = await params;
  const token = generateAccessToken();

  return NextResponse.json({
    ok: true,
    eventId,
    token,
    organizerUrl: buildOrganizerUrl(token)
  });
}

export async function DELETE(
  _request: Request,
  { params }: { params: Promise<{ eventId: string }> }
) {
  const { eventId } = await params;

  return NextResponse.json({
    ok: true,
    eventId,
    revoked: true
  });
}
