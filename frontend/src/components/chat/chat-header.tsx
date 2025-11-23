"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Shield, LogOut, User, Settings } from "lucide-react";
import { MESSAGES } from "@/constants/messages";
import { ROUTES } from "@/constants/routes";
import { siteConfig } from "@/config/site.config";
import { useAuth } from "@/contexts/auth-context";
import { ConfigurationProfileSelector } from "./configuration-profile-selector";
import { ModelDropdown } from "./model-dropdown";

/**
 * Chat header component
 * Displays app branding, status, and navigation
 */
import { useState } from "react";
import { ConfigurationProfile } from "@/lib/api/llm";
// ... imports

export function ChatHeader() {
  const { user, logout } = useAuth();
  const [activeProfile, setActiveProfile] = useState<ConfigurationProfile | null>(null);

  return (
    <header className="border-b border-border bg-card cyber-border scan-line">
      <div className="container flex items-center justify-between h-14 px-4 mx-auto">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-secondary cyber-border">
            <Shield className="w-5 h-5 text-secondary-foreground" />
          </div>
          <div>
            <h1 className="text-lg font-semibold terminal-text">{siteConfig.name}</h1>
            <div className="text-xs text-muted-foreground">{MESSAGES.LABELS.NEURAL_INTERFACE}</div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <ConfigurationProfileSelector 
              onActiveProfileChange={setActiveProfile}
            />
            <ModelDropdown activeProfile={activeProfile} />
            <Button variant="ghost" size="sm" asChild>
              <a href="/dashboard">Dashboard</a>
            </Button>
          </div>
          <Link href={ROUTES.DEMO} className="cursor-pointer">
            <Button
              variant="outline"
              size="sm"
              className="cyber-border terminal-text cursor-pointer"
            >
              View Demo
            </Button>
          </Link>
          
          {user && (
            <div className="flex items-center gap-2 px-3 py-1 bg-secondary/20 rounded-md border border-primary/20">
              <User className="w-4 h-4 text-primary" />
              <span className="text-xs text-foreground">{user.username}</span>
            </div>
          )}
          
          <Button
            variant="outline"
            size="sm"
            onClick={logout}
            className="cyber-border terminal-text cursor-pointer"
          >
            <LogOut className="w-4 h-4 mr-1" />
            Logout
          </Button>
          
          <div className="w-2 h-2 bg-chart-1 rounded-full animate-pulse"></div>
          <div className="text-xs text-muted-foreground terminal-text">
            {MESSAGES.SYSTEM.ONLINE}
          </div>
        </div>
      </div>
    </header>
  );
}

