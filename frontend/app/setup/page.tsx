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
      // Redirect happens in the setup function
    } catch (err: any) {
      setError(err.message || "Failed to complete setup");
    } finally {
      setIsLoading(false);
    }
  };

  if (isCheckingStatus) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="matrix-rain"></div>
        <div className="text-center z-10">
          <div className="loading-spinner mb-4"></div>
          <p className="text-primary">Checking system status...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-background">
      <div className="matrix-rain"></div>

      <div className="w-full max-w-md p-8 space-y-6 bg-card border border-primary/20 rounded-lg shadow-glow z-10">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-primary mb-2">CMatrix Setup</h1>
          <p className="text-muted-foreground">Create your admin credentials</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-foreground mb-2">
              Username
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-2 bg-background border border-primary/30 rounded-md text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
              placeholder="Enter username"
              required
              minLength={3}
              disabled={isLoading}
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-foreground mb-2">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 bg-background border border-primary/30 rounded-md text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
              placeholder="Enter password (min 8 characters)"
              required
              minLength={8}
              disabled={isLoading}
            />
          </div>

          <div>
            <label
              htmlFor="confirmPassword"
              className="block text-sm font-medium text-foreground mb-2"
            >
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full px-4 py-2 bg-background border border-primary/30 rounded-md text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
              placeholder="Confirm password"
              required
              minLength={8}
              disabled={isLoading}
            />
          </div>

          {error && (
            <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-md">
              <p className="text-sm text-red-400">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full px-4 py-2 bg-primary text-primary-foreground rounded-md font-medium hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary/50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? "Setting up..." : "Complete Setup"}
          </button>
        </form>

        <div className="text-center text-sm text-muted-foreground">
          <p>This is a one-time setup. All users will use these credentials.</p>
        </div>
      </div>
    </div>
  );
}
