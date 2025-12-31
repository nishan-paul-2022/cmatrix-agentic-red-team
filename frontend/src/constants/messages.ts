/**
 * Message and text constants
 */

export const MESSAGES = {
  SYSTEM: {
    PROCESSING: "[PROCESSING QUERY...]",
    SECURITY_NOTICE: "CMatrix can make mistakes. Check important info.",
  },

  LABELS: {
    NEURAL_INTERFACE: "Agentic AI for Security",
  },

  PLACEHOLDERS: {
    INPUT: "How can I help you today?",
  },

  ERRORS: {
    GENERIC: "Sorry, I encountered an error. Please try again.",
    NO_RESPONSE: "No response body",
    FETCH_FAILED: "Failed to fetch",
  },

  WELCOME: {
    TITLE: "CMatrix",
    SUBTITLE: "Agentic AI for Security",
    DESCRIPTION: "AI-powered platform that unifies Red, Blue, and Purple teaming into one autonomous system for continuous attack simulation, defense, and security validation.",
  },

  SUGGESTIONS: {
    SECURITY_SCAN: {
      TITLE: "Security Scan",
      DESCRIPTION: "Analyze system vulnerabilities",
      PROMPT: "Scan my web application for vulnerabilities",
    },
    SYSTEM_STATUS: {
      TITLE: "System Status",
      DESCRIPTION: "Monitor infrastructure health",
      PROMPT: "Check the status of critical services",
    },
  },
} as const;

export type Messages = typeof MESSAGES;
