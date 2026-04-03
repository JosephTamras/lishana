import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono, Noto_Sans_Syriac_Eastern } from "next/font/google";
import "./globals.css";
import { LayoutWrapper } from "./components/LayoutWrapper";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const notoSansSyriacEastern = Noto_Sans_Syriac_Eastern({
  variable: "--font-syriac",
  subsets: ["syriac"],
});

export const metadata: Metadata = {
  title: "Lishana",
  description: "An Assyrian-English dictionary powered by Typesense and InstantSearch.",
  icons: {
    icon: "/favicon.ico",
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} ${notoSansSyriacEastern.variable} antialiased bg-white text-slate-900 transition-colors min-h-screen`}
      >
        <LayoutWrapper>{children}</LayoutWrapper>
      </body>
    </html>
  );
}
