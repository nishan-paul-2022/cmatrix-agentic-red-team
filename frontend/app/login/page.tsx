"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/auth-context";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { login, isAuthenticated, checkSetupStatus } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // Check if setup is complete
    const checkStatus = async () => {
      try {
        const isComplete = await checkSetupStatus();
        if (!isComplete) {
          // Setup not done, redirect to setup
          router.push("/setup");
        }
      } catch (error) {
        console.error("Failed to check setup status:", error);
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
    setIsLoading(true);

    try {
      await login(username, password);
      // Redirect happens in the login function
    } catch (err: any) {
      setError(err.message || "Invalid username or password");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-background">
      <div className="matrix-rain"></div>

      <div className="w-full max-w-md p-8 space-y-6 bg-card border border-primary/20 rounded-lg shadow-glow z-10">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-primary mb-2">CMatrix Login</h1>
          <p className="text-muted-foreground">Enter your credentials to continue</p>
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
              disabled={isLoading}
              autoComplete="username"
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
              placeholder="Enter password"
              required
              disabled={isLoading}
              autoComplete="current-password"
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
            {isLoading ? "Logging in..." : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
}
