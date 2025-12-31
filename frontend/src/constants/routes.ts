/**
 * Application route constants
 */

export const ROUTES = {
  HOME: "/",

  API: {
    CHAT: "/api/chat",
  },
} as const;

export type Routes = typeof ROUTES;
