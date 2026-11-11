import type { Metadata } from "next";
import "./globals.css";
import Navigation from "@/components/Navigation";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "GemNotes",
  description: "AI-powered notes, summaries, slides, and more.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen flex flex-col bg-gradient-to-br from-zinc-900 via-black to-zinc-800 text-white">
        <Navigation />
        <main className="flex-1 flex flex-col container mx-auto px-2 sm:px-6 py-4">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
