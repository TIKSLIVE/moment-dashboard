import crypto from "node:crypto";
import { NextResponse } from "next/server";

function validateSignature(payload: string, signature: string | null) {
  if (!signature) return false;

  const secret = process.env.VIVENU_WEBHOOK_HMAC_KEY ?? "change-me";
  const digest = crypto.createHmac("sha256", secret).update(payload).digest("hex");
  const expected = Buffer.from(digest);
  const received = Buffer.from(signature);

  if (expected.length !== received.length) {
    return false;
  }

  return crypto.timingSafeEqual(expected, received);
}

export async function POST(request: Request) {
  const payload = await request.text();
  const signature = request.headers.get("x-vivenu-signature");

  if (!validateSignature(payload, signature)) {
    return NextResponse.json({ ok: false, error: "Invalid signature" }, { status: 401 });
  }

  return NextResponse.json({
    ok: true,
    receivedAt: new Date().toISOString(),
    message:
      "Webhook accepted. Map transaction.complete, transaction.canceled and transaction.partiallyCanceled to transaction upserts and sync_state updates."
  });
}
