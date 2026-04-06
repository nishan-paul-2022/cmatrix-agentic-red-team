"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/auth-context";

export default function SetupPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isCheckingStatus, setIsCheckingStatus] = useState(true);
  const { setup, checkSetupStatus, isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // Check if setup is already complete
    const checkStatus = async () => {
      try {
        const isComplete = await checkSetupStatus();
        if (isComplete) {
          // Setup already done, redirect to login
          router.push("/login");
        }
      } catch (error) {
        console.error("Failed to check setup status:", error);
      } finally {
        setIsCheckingStatus(false);
      }
    };

    checkStatus();
  }, [checkSetupStatus, router]);

  useEffect(() => {
    // If already authenticated, redirect to home
    if (isAuthenticated) {
      router.push("/");
    }
  }, [isAuthenticated, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    // Validation
    if (username.length < 3) {
      setError("Username must be at least 3 characters long");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters long");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setIsLoading(true);

    try {
      await setup(username, password);
      router.push("/");
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : "Setup failed";

      // If setup is already complete, redirect to login
      if (
        errorMessage.toLowerCase().includes("already complete") ||
        errorMessage.toLowerCase().includes("already exists")
      ) {
        router.push("/login");
        return;
      }

      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  if (isCheckingStatus) {
    return (
      <div className="bg-background flex min-h-screen items-center justify-center">
        <div className="matrix-rain"></div>
        <div className="z-10 text-center">
          <div className="loading-spinner mb-4"></div>
          <p className="text-primary">Checking system status...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-background flex min-h-screen items-center justify-center">
      <div className="matrix-rain"></div>

      <div className="bg-card border-primary/20 shadow-glow z-10 w-full max-w-md space-y-6 rounded-lg border p-8">
        <div className="text-center">
          <h1 className="text-primary mb-2 text-3xl font-bold">CMatrix Setup</h1>
          <p className="text-muted-foreground">Create your admin credentials</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="username" className="text-foreground mb-2 block text-sm font-medium">
              Username
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="bg-background border-primary/30 text-foreground focus:ring-primary/50 w-full rounded-md border px-4 py-2 focus:ring-2 focus:outline-none"
              placeholder="Enter username"
              required
              minLength={3}
              disabled={isLoading}
            />
          </div>

          <div>
            <label htmlFor="password" className="text-foreground mb-2 block text-sm font-medium">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="bg-background border-primary/30 text-foreground focus:ring-primary/50 w-full rounded-md border px-4 py-2 focus:ring-2 focus:outline-none"
              placeholder="Enter password (min 8 characters)"
              required
              minLength={8}
              disabled={isLoading}
            />
          </div>

          <div>
            <label
              htmlFor="confirmPassword"
              className="text-foreground mb-2 block text-sm font-medium"
            >
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="bg-background border-primary/30 text-foreground focus:ring-primary/50 w-full rounded-md border px-4 py-2 focus:ring-2 focus:outline-none"
              placeholder="Confirm password"
              required
              minLength={8}
              disabled={isLoading}
            />
          </div>

          {error && (
            <div className="rounded-md border border-red-500/30 bg-red-500/10 p-3">
              <p className="text-sm text-red-400">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="bg-primary text-primary-foreground hover:bg-primary/90 focus:ring-primary/50 w-full rounded-md px-4 py-2 font-medium transition-colors focus:ring-2 focus:outline-none disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isLoading ? "Setting up..." : "Complete Setup"}
          </button>
        </form>
      </div>
    </div>
  );
}
