import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MOMENT x vivenu Dashboard",
  description: "Dashboard externe pour le suivi de ventes vivenu."
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
