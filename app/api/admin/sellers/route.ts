import { NextResponse } from "next/server";
import { z } from "zod";
import { encryptString } from "@/lib/crypto";

const sellerSchema = z.object({
  name: z.string().min(2),
  sellerId: z.string().min(2),
  apiKey: z.string().min(8)
});

export async function POST(request: Request) {
  const payload = sellerSchema.parse(await request.json());

  return NextResponse.json({
    ok: true,
    message: "Seller payload validated. Persist with Prisma in production.",
    seller: {
      ...payload,
      apiKeyEncrypted: encryptString(payload.apiKey)
    }
  });
}
