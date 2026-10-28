import type { Metadata, Viewport } from "next";
import { Cormorant_Garamond, Jost } from "next/font/google";
import "./globals.css";

const cormorant = Cormorant_Garamond({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  style: ["normal", "italic"],
  variable: "--font-serif",
  display: "swap",
});

const jost = Jost({
  subsets: ["latin"],
  weight: ["300", "400", "500"],
  variable: "--font-sans",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Sri Amman Bakery",
  description:
    "Authentic traditional Indian sweets and fresh bakes handcrafted with 100% pure homemade ghee. Serving sweetness since 2022. Featuring Laddu, Mysore Pak, Jalebi, Badam Burfi, Boost Burfi, Horlicks Burfi, and Badusha.",
};

export const viewport: Viewport = {
  themeColor: "#123D32",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${cormorant.variable} ${jost.variable}`}>
      <head>
        <link rel="preload" as="image" href="/logo.png" />
        <link rel="preload" as="image" href="/sweet.png" />
        <link rel="preload" as="image" href="/sweet_tray.png" />
        <link rel="preload" as="image" href="/stir_poster.jpg" />
      </head>
      <body className="bg-[#0A241E] text-[#F7F1E5] antialiased selection:bg-[#651B24] selection:text-[#F7F1E5]">
        {children}
      </body>
    </html>
  );
}
