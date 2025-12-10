import type { Metadata } from "next";
import { Geist, Geist_Mono, Noto_Sans_Syriac_Eastern } from "next/font/google";
import "./globals.css";

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

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} ${notoSansSyriacEastern.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
