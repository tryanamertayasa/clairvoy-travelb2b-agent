import type { Metadata } from "next";
import { Inter, Montserrat } from "next/font/google";
import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/styles.css";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: '--font-inter',
});

const montserrat = Montserrat({
  subsets: ["latin"],
  weight: ['400', '500', '600', '700'],
  variable: '--font-montserrat',
});

export const metadata: Metadata = {
  title: "Clairvoy B2B Travel Consolidator",
  description:
    "AI-powered B2B travel consolidation platform connecting OTAs and TMCs with global suppliers using Google ADK and Gemini",
  keywords: ["B2B travel", "travel consolidator", "OTA", "TMC", "AI", "Google ADK", "Gemini", "GDS"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${montserrat.variable} ${inter.className}`}>
        <CopilotKit
          runtimeUrl="/api/copilotkit"
          agent="clairvoy_b2b_travel"
        >
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
