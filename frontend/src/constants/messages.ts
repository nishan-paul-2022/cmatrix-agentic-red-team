/**
 * Message and text constants
 */

export const MESSAGES = {
  SYSTEM: {

    OPERATIONAL: "[SYSTEM STATUS: OPERATIONAL] [AGENT: CMATRIX-CORE-V1]",
    PROCESSING: "[PROCESSING QUERY...]",

    SECURITY_NOTICE: "[SECURITY NOTICE] Neural responses may contain classified information. Handle with care.",
  },

  LABELS: {

    NEURAL_INTERFACE: "Neural Interface Active",
  },

  PLACEHOLDERS: {
    INPUT: "Enter command or query...",
  },

  ERRORS: {
    GENERIC: "Sorry, I encountered an error. Please try again.",
    NO_RESPONSE: "No response body",
    FETCH_FAILED: "Failed to fetch",
  },

  WELCOME: {
    TITLE: "CMatrix",
    SUBTITLE: "Neural Interface",
    DESCRIPTION: "Agent capabilities: security scanning, system monitoring, log analysis, configuration deployment.",
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
