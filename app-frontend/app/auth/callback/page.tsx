"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuthCallback } from "@/contexts/auth-context";
import { Suspense } from "react";

// ─── Inner component (needs Suspense for useSearchParams) ─────────────────────

function CallbackHandler() {
  const searchParams = useSearchParams();
  const setToken = useAuthCallback();
  const router = useRouter();
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const token = searchParams.get("token");
    const error = searchParams.get("error");

    // Defer the state updates to avoid React's synchronous setState check in Effects
    const handleResult = () => {
      if (error) {
        const messages: Record<string, string> = {
          access_denied: "You denied access to your Google account.",
          email_not_verified: "Your Google email address is not verified.",
          oauth_failed: "Google authentication failed. Please try again.",
          server_error: "A server error occurred. Please try again.",
          missing_code: "Authorization code was missing from Google's response.",
          invalid_state: "The login state mismatch. Potential CSRF attempt.",
        };
        setErrorMessage(messages[error] ?? `Authentication error: ${error.replace(/_/g, " ")}.`);
        setStatus("error");
        return;
      }

      if (!token) {
        setErrorMessage("No authentication token received.");
        setStatus("error");
        return;
      }

      // Store the token and hydrate the user
      setToken(token);
      setStatus("success");

      // Short delay before the final redirect for smooth UX
      const timer = setTimeout(() => {
        router.replace("/chat");
      }, 1000);

      return timer;
    };

    const timerId = handleResult();
    return () => {
      if (timerId) clearTimeout(timerId);
    };
  }, [searchParams, setToken, router]);

  return (
    <div className="bg-background flex min-h-screen flex-col items-center justify-center">
      <div className="matrix-rain" />

      <div className="callback-card">
        {status === "loading" && (
          <>
            <div className="loading-spinner mb-6" />
            <p className="text-primary font-mono text-sm tracking-widest">AUTHENTICATING…</p>
            <p className="text-muted-foreground mt-2 text-xs">Verifying your Google account</p>
          </>
        )}

        {status === "success" && (
          <>
            <div className="callback-success-icon">✓</div>
            <p className="text-primary font-mono text-lg font-bold tracking-widest">
              AUTHENTICATED
            </p>
            <p className="text-muted-foreground mt-2 text-sm">Redirecting to dashboard…</p>
          </>
        )}

        {status === "error" && (
          <>
            <div className="callback-error-icon">✕</div>
            <p className="text-destructive font-mono text-lg font-bold tracking-widest">
              AUTH FAILED
            </p>
            <p className="text-muted-foreground mt-2 max-w-sm text-center text-sm">
              {errorMessage}
            </p>
            <button
              id="retry-login-btn"
              onClick={() => router.replace("/")}
              className="landing-btn-primary mt-6"
            >
              ← Back to Home
            </button>
          </>
        )}
      </div>
    </div>
  );
}

// ─── Page export (Suspense boundary required for useSearchParams) ─────────────

export default function AuthCallbackPage() {
  return (
    <Suspense
      fallback={
        <div className="bg-background flex min-h-screen items-center justify-center">
          <div className="loading-spinner" />
        </div>
      }
    >
      <CallbackHandler />
    </Suspense>
  );
}
