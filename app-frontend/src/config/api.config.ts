/**
 * API configuration
 */

const getBaseUrl = (): string => {
  // If we're on the client side (browser)
  if (typeof window !== "undefined") {
    // 1. Check if we're on localhost - if so, we can use the backend directly to see logs easier,
    // OR just use the /api/v1 rewrite. Relative path is more robust for deployment.
    const isLocalhost =
      window.location.hostname === "localhost" ||
      window.location.hostname === "127.0.0.1" ||
      window.location.hostname.includes("192.168.");

    if (isLocalhost) {
      // In local dev, we might want to hit the backend directly (port 3012)
      // but using /api/v1 (port 3011) also works because of next.config.mjs rewrites.
      // Let's stick with the environment variable if set, otherwise default to local backend.
      return process.env.NEXT_PUBLIC_API_URL || "http://localhost:3012/api/v1";
    }

    // 2. In production, always use the relative path.
    // This automatically handles any domain/subdomain and avoids CORS issues.
    return "/api/v1";
  }

  // If we're on the server side (SSR/API Routes)
  // Use the internal network URL if available (faster for container-to-container)
  const backendUrl = process.env.PYTHON_BACKEND_URL;
  if (backendUrl) {
    return `${backendUrl}/api/v1`;
  }

  // Fallback to the public environment variable or localhost
  return process.env.NEXT_PUBLIC_API_URL || "http://localhost:3012/api/v1";
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
