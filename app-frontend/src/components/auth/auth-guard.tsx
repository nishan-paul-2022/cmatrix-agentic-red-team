"use client";

import { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useAuth } from "@/contexts/auth-context";

/**
 * AuthGuard
 *
 * Public routes (no token required):
 *   /              — landing page
 *   /auth/callback — OAuth token receiver
 *
 * All other routes require authentication.
 * Unauthenticated users are redirected to the landing page (/).
 * Authenticated users visiting /auth/callback are redirected to /dashboard.
 */
export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  const PUBLIC_ROUTES = ["/", "/auth/callback"];
  const isPublic = PUBLIC_ROUTES.some((r) => pathname === r || pathname.startsWith(r + "?"));

  useEffect(() => {
    if (isLoading) return;

    if (!isAuthenticated && !isPublic) {
      // Protected route — send unauthenticated users to the landing page
      router.replace("/");
      return;
    }

    // Authenticated user hitting the raw callback page without params
    if (isAuthenticated && pathname === "/auth/callback") {
      router.replace("/dashboard");
      return;
    }
  }, [isAuthenticated, isLoading, isPublic, pathname, router]);

  // Show a minimal loader while auth resolves
  if (isLoading) {
    return (
      <div className="bg-background flex min-h-screen items-center justify-center">
        <div className="matrix-rain" />
        <div className="z-10 flex flex-col items-center gap-4">
          <div className="loading-spinner" />
          <p className="text-primary font-mono text-sm tracking-widest">INITIALIZING…</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
