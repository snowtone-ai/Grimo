import type { Metadata, Viewport } from "next";
import type { ReactNode } from "react";
import Script from "next/script";
import { SerwistProvider } from "@serwist/next/react";
import "./globals.css";

export const metadata: Metadata = {
  applicationName: "Grimo",
  title: { default: "Grimo", template: "%s | Grimo" },
  description: "グリモと触れ合うためのタスク管理PWA",
  icons: {
    icon: "/icons/grimo-icon-192.png",
    apple: "/icons/grimo-apple-touch-icon.png",
  },
  appleWebApp: { capable: true, title: "Grimo", statusBarStyle: "default" },
  formatDetection: { telephone: false },
};

export const viewport: Viewport = {
  themeColor: "#eef7fb",
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ja">
      <body>
        <SerwistProvider swUrl="/sw.js" disable={process.env.NODE_ENV === "development"}>
          {children}
        </SerwistProvider>
        <Script src="https://accounts.google.com/gsi/client" strategy="afterInteractive" />
      </body>
    </html>
  );
}
