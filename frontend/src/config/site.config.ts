/**
 * Site-wide configuration
 */

export const siteConfig = {
  name: "CMatrix",

  metadata: {
    title: "CMatrix",
    description:
      "Advanced AI agent for security scanning, system monitoring, log analysis, and configuration deployment",
    keywords: ["AI", "Security", "Orchestration", "Automation", "CMatrix"],
    author: "KAI Team",
    generator: "CMatrix",
  },

  ui: {
    animations: {
      typewriterSpeed: 150,
    },
  },
} as const;

export type SiteConfig = typeof siteConfig;
