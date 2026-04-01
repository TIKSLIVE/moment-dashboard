import { NextResponse } from "next/server";

export async function GET(request: Request) {
  const authorization = request.headers.get("authorization");
  const expected = `Bearer ${process.env.CRON_SECRET ?? "change-me"}`;

  if (authorization !== expected) {
    return NextResponse.json({ ok: false, error: "Unauthorized" }, { status: 401 });
  }

  return NextResponse.json({
    ok: true,
    processedAt: new Date().toISOString(),
    message:
      "Cron endpoint ready. Iterate active events, fetch updated transactions, upsert, then recompute aggregates."
  });
}
