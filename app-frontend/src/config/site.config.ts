/**
 * Site-wide configuration
 */

export const siteConfig = {
  name: "CMatrix",

  metadata: {
    title: "CMatrix | Autonomous Agentic Red Team Platform",
    description:
      "CMatrix orchestrates specialized AI security agents to perform autonomous penetration testing, vulnerability assessment, and red-team operations — powered by advanced LLM reasoning.",
    keywords: [
      "Autonomous AI",
      "Red Team",
      "Security Automation",
      "Penetration Testing",
      "DeepHat",
      "AI Security Agent",
      "Cybersecurity",
    ],
    author: "CMatrix Team",
    generator: "CMatrix V1",
  },

  ui: {
    animations: {
      typewriterSpeed: 150,
    },
  },
} as const;

export type SiteConfig = typeof siteConfig;
