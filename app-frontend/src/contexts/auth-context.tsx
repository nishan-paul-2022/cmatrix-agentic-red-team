"use client";

import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { apiConfig } from "@/config/api.config";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface AuthUser {
  id: number;
  username: string;
  email?: string | null;
  avatar_url?: string | null;
  auth_provider: string;
  is_active: boolean;
  created_at: string;
}

interface AuthContextType {
  user: AuthUser | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  loginWithGoogle: () => Promise<void>;
  logout: () => void;
}

// ---------------------------------------------------------------------------
// Context
// ---------------------------------------------------------------------------

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const TOKEN_KEY = "cmatrix_auth_token";

async function fetchWithTimeout(
  resource: string,
  options: RequestInit = {},
  timeout = 10_000
): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);
  try {
    return await fetch(resource, { ...options, signal: controller.signal });
  } catch (err) {
    if (err instanceof Error && err.name === "AbortError") {
      throw new Error("Request timed out. Please check your connection.");
    }
    throw err;
  } finally {
    clearTimeout(timer);
  }
}

// ---------------------------------------------------------------------------
// Provider
// ---------------------------------------------------------------------------

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  const API_BASE = apiConfig.baseUrl;

  // -------------------------------------------------------------------------
  // Fetch the current user from /auth/me using a stored JWT
  // -------------------------------------------------------------------------
  const hydrateUser = useCallback(
    async (jwt: string) => {
      try {
        const resp = await fetchWithTimeout(`${API_BASE}/auth/me`, {
          headers: { Authorization: `Bearer ${jwt}` },
        });

        if (resp.ok) {
          const data: AuthUser = await resp.json();
          setUser(data);
          setToken(jwt);
        } else {
          // Token is invalid / expired — clear it
          localStorage.removeItem(TOKEN_KEY);
          setUser(null);
          setToken(null);
        }
      } catch {
        // Network error — don't clear token so offline users aren't logged out
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    },
    [API_BASE]
  );

  // -------------------------------------------------------------------------
  // On mount — restore session from localStorage
  // -------------------------------------------------------------------------
  useEffect(() => {
    const stored = localStorage.getItem(TOKEN_KEY);
    if (stored) {
      hydrateUser(stored);
    } else {
      setIsLoading(false);
    }
  }, [hydrateUser]);

  // -------------------------------------------------------------------------
  // Called from the OAuth callback page once a token is received
  // -------------------------------------------------------------------------
  const setTokenFromCallback = useCallback(
    (jwt: string) => {
      localStorage.setItem(TOKEN_KEY, jwt);
      hydrateUser(jwt);
    },
    [hydrateUser]
  );

  // -------------------------------------------------------------------------
  // loginWithGoogle — fetches the auth URL from backend and redirects
  // -------------------------------------------------------------------------
  const loginWithGoogle = useCallback(async () => {
    try {
      const resp = await fetchWithTimeout(`${API_BASE}/auth/google/login`, {}, 8_000);
      if (!resp.ok) throw new Error("Failed to initiate Google OAuth.");
      const { auth_url }: { auth_url: string } = await resp.json();
      window.location.href = auth_url;
    } catch (err) {
      console.error("Google OAuth init error:", err);
      throw err;
    }
  }, [API_BASE]);

  // -------------------------------------------------------------------------
  // logout — clear state & storage, send back to landing page
  // -------------------------------------------------------------------------
  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    setToken(null);
    setUser(null);
    router.push("/");
  }, [router]);

  // -------------------------------------------------------------------------
  // Expose setTokenFromCallback so the callback page can call it
  // -------------------------------------------------------------------------
  const contextValue = useMemo(
    () => ({
      user,
      token,
      isAuthenticated: !!token && !!user,
      isLoading,
      loginWithGoogle,
      logout,
      /** @internal used only by /auth/callback page */
      _setTokenFromCallback: setTokenFromCallback,
    }),
    [user, token, isLoading, loginWithGoogle, logout, setTokenFromCallback]
  );

  return (
    <AuthContext.Provider value={contextValue as AuthContextType}>{children}</AuthContext.Provider>
  );
}

// ---------------------------------------------------------------------------
// Hooks
// ---------------------------------------------------------------------------

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (ctx === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return ctx;
}

/**
 * Internal hook used by the /auth/callback page to store the token received
 * from the backend redirect without exposing it on the public AuthContextType.
 */
export function useAuthCallback(): (jwt: string) => void {
  const ctx = useContext(AuthContext) as AuthContextType & {
    _setTokenFromCallback: (jwt: string) => void;
  };
  if (!ctx) throw new Error("useAuthCallback must be used within AuthProvider");
  return ctx._setTokenFromCallback;
}
