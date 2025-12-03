/**
 * API configuration
 */

const getBaseUrl = (): string => {
  // For both client and server-side, use the environment variable
  return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
};

export const apiConfig = {
  baseUrl: getBaseUrl(),

  endpoints: {
    chat: "/chat",
    chatStream: "/chat/stream",
    health: "/health",
    conversations: "/conversations",
    jobs: {
      create: "/jobs/scan",
      get: (id: string) => `/jobs/${id}`,
      list: "/jobs",
      cancel: (id: string) => `/jobs/${id}`,
    },
  },

  timeout: 30000, // 30 seconds

  retryConfig: {
    maxRetries: 3,
    retryDelay: 1000,
    retryableStatuses: [408, 429, 500, 502, 503, 504],
  },

  headers: {
    "Content-Type": "application/json",
  },
} as const;

export type ApiConfig = typeof apiConfig;
