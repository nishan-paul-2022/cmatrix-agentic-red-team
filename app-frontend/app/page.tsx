"use client";

import { useCallback, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/auth-context";
import NextImage from "next/image";

// ─── Feature card data ────────────────────────────────────────────────────────

const FEATURES = [
  {
    icon: "🕸️",
    title: "Multi-Agent Architecture",
    description:
      "Six specialized agents — Network, Web, Auth, Config, Intel, API — orchestrated by a master controller for comprehensive red-team coverage.",
  },
  {
    icon: "⚡",
    title: "Real-Time Streaming",
    description:
      "Watch your agents think and act in real time with live-streamed responses and step-by-step attack chain transparency.",
  },
  {
    icon: "🔐",
    title: "Google OAuth Security",
    description:
      "Enterprise-grade authentication via Google OAuth 2.0. No passwords stored. Your identity is managed by Google.",
  },
  {
    icon: "🧠",
    title: "AI-Powered Reasoning",
    description:
      "Powered by state-of-the-art LLMs with ReWOO reasoning, semantic memory, and intelligent tool selection.",
  },
  {
    icon: "📋",
    title: "Approval Workflows",
    description:
      "Human-in-the-loop approval gates for high-risk operations. Every destructive action requires explicit sign-off.",
  },
  {
    icon: "📊",
    title: "Audit & Reporting",
    description:
      "Immutable audit logs for every agent action. Export full engagement reports with CVE correlation and risk scoring.",
  },
];

// ─── Component ────────────────────────────────────────────────────────────────

export default function LandingPage() {
  const { user, isAuthenticated, isLoading, loginWithGoogle } = useAuth();
  const [oauthLoading, setOauthLoading] = useState(false);
  const [oauthError, setOauthError] = useState("");
  const router = useRouter();

  const handleGetStarted = useCallback(async () => {
    setOauthError("");
    setOauthLoading(true);
    try {
      await loginWithGoogle();
    } catch {
      setOauthError("Failed to connect to Google. Please try again.");
      setOauthLoading(false);
    }
  }, [loginWithGoogle]);

  return (
    <div className="landing-page">
      {/* Matrix rain background */}
      <div className="matrix-rain" />

      {/* Grid overlay */}
      <div className="landing-grid" />

      {/* ── NAV ──────────────────────────────────────────────────────────── */}
      <nav className="landing-nav">
        <div className="landing-nav-inner">
          <div className="landing-logo">
            <span className="landing-logo-bracket">[</span>
            <span className="landing-logo-text">CMatrix</span>
            <span className="landing-logo-bracket">]</span>
          </div>
        </div>
      </nav>

      {/* ── HERO ─────────────────────────────────────────────────────────── */}
      <section className="landing-hero">
        {/* Headline */}
        <h1 className="landing-headline">
          Autonomous
          <br />
          <span className="landing-headline-accent">Red Team</span>
          <br />
          Intelligence
        </h1>

        {/* Sub-headline */}
        <p className="landing-subheadline">
          CMatrix orchestrates specialized AI agents to perform comprehensive penetration testing,
          vulnerability assessment, and security intelligence — all in a single, auditable platform.
        </p>

        {/* ── CTA ── */}
        {isLoading ? (
          <div className="landing-cta-loading">
            <div className="loading-spinner" />
            <span>Checking session…</span>
          </div>
        ) : isAuthenticated && user ? (
          /* ── Authenticated state ── */
          <div className="landing-authenticated">
            <div className="landing-user-card">
              {user.avatar_url ? (
                <NextImage
                  src={user.avatar_url}
                  alt={user.username}
                  width={64}
                  height={64}
                  className="landing-avatar"
                  referrerPolicy="no-referrer"
                />
              ) : (
                <div className="landing-avatar-placeholder">
                  {user.username.charAt(0).toUpperCase()}
                </div>
              )}
              <div className="landing-user-info">
                <p className="landing-welcome">Welcome back,</p>
                <p className="landing-username">{user.username}</p>
                {user.email && <p className="landing-user-email">{user.email}</p>}
              </div>
            </div>

            <button
              id="start-chatting-btn"
              onClick={() => router.push("/chat")}
              className="landing-btn-primary"
            >
              <span>Talk to AI Agent</span>
              <span className="landing-btn-arrow">→</span>
            </button>
          </div>
        ) : (
          /* ── Unauthenticated state ── */
          <div className="landing-cta-group">
            <button
              id="get-started-btn"
              onClick={handleGetStarted}
              disabled={oauthLoading}
              className="landing-btn-primary"
            >
              {oauthLoading ? (
                <>
                  <div className="landing-btn-spinner" />
                  <span>Redirecting to Google…</span>
                </>
              ) : (
                <>
                  <GoogleIcon />
                  <span>Get Started with Google</span>
                </>
              )}
            </button>

            {oauthError && <p className="landing-oauth-error">{oauthError}</p>}

            <p className="landing-auth-note">
              Secure login via Google OAuth 2.0 · No password required
            </p>
          </div>
        )}
      </section>

      {/* ── FEATURES ─────────────────────────────────────────────────────── */}
      <section className="landing-features">
        <div className="landing-features-header">
          <h2 className="landing-section-title">Built for Security Professionals</h2>
          <p className="landing-section-sub">
            Every component is designed around the PTES and OWASP frameworks, giving you the tools
            professionals trust.
          </p>
        </div>

        <div className="landing-features-grid">
          {FEATURES.map((f) => (
            <div key={f.title} className="landing-feature-card group">
              <div className="landing-feature-icon">{f.icon}</div>
              <h3 className="landing-feature-title">{f.title}</h3>
              <p className="landing-feature-desc">{f.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── FOOTER ───────────────────────────────────────────────────────── */}
      <footer className="landing-footer">
        <div className="landing-footer-inner">
          <span className="landing-logo">
            <span className="landing-logo-bracket">[</span>
            <span className="landing-logo-text">CMatrix</span>
            <span className="landing-logo-bracket">]</span>
          </span>
          <span className="landing-footer-copy">© {new Date().getFullYear()} CMatrix</span>
        </div>
      </footer>
    </div>
  );
}

// ─── Google icon SVG ─────────────────────────────────────────────────────────

function GoogleIcon() {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <path
        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
        fill="#4285F4"
      />
      <path
        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
        fill="#34A853"
      />
      <path
        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"
        fill="#FBBC05"
      />
      <path
        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
        fill="#EA4335"
      />
    </svg>
  );
}
