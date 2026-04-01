import crypto from "node:crypto";

export function generateAccessToken() {
  return crypto.randomBytes(32).toString("hex");
}

export function buildOrganizerUrl(token: string) {
  const appUrl = process.env.APP_URL ?? "http://localhost:3000";
  return `${appUrl}/o/${token}`;
}
