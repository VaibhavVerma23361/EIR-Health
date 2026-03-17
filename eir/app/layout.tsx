import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Eir - AI Medical Diagnosis",
  description: "Advanced multimodal AI system for medical diagnosis",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
