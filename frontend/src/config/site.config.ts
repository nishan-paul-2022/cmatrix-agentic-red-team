/**
 * Site-wide configuration
 */

export const siteConfig = {
  name: "CMatrix",
  description: "AI-Powered Security Orchestration",
  tagline: "Neural Interface Active",
  version: "1.0.0",
  
  metadata: {
    title: "CMatrix - AI-Powered Security Orchestration",
    description: "Advanced AI agent for security scanning, system monitoring, log analysis, and configuration deployment",
    keywords: ["AI", "Security", "Orchestration", "Automation", "CMatrix"],
    author: "CMatrix Team",
    generator: "CMatrix",
  },

  features: {
    chat: {
      enabled: true,
      maxHistoryLength: 10,
      streamingEnabled: true,
    },

    analytics: {
      enabled: true,
    },
  },

  ui: {
    theme: {
      defaultMode: "dark",
      cyberpunkEffects: true,
      matrixRain: true,
    },
    animations: {
      typewriterSpeed: 150,
      animationStepDuration: 2000,
    },
  },
} as const;

export type SiteConfig = typeof siteConfig;
