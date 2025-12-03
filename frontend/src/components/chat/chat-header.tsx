"use client";

import Link from "next/link";

import { Button } from "@/components/ui/button";
import { LogOut, User, Settings, ChevronDown, Shield } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { MESSAGES } from "@/constants/messages";
import { siteConfig } from "@/config/site.config";
import { useAuth } from "@/contexts/auth-context";
import { BrandLogo } from "@/components/brand-logo";
import { ConfigurationProfileSelector } from "./configuration-profile-selector";
import { ModelDropdown } from "./model-dropdown";
import { SettingsSidebar } from "./settings-sidebar";
import { useState } from "react";
import { ConfigurationProfile } from "@/lib/api/llm";

export function ChatHeader() {
  const { user, logout } = useAuth();
  const [activeProfile, setActiveProfile] = useState<ConfigurationProfile | null>(null);
  const [isSettingsSidebarOpen, setIsSettingsSidebarOpen] = useState(false);

  return (
    <header className="border-b border-border bg-card cyber-border">
      <div className="container flex items-center justify-between h-14 px-4 mx-auto">
        <Link
          href="/"
          className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity"
        >
          <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-secondary/10 cyber-border overflow-hidden">
            <BrandLogo size={24} />
          </div>
          <div>
            <h1 className="text-lg font-semibold terminal-text">{siteConfig.name}</h1>
            <div className="text-xs text-muted-foreground">{MESSAGES.LABELS.NEURAL_INTERFACE}</div>
          </div>
        </Link>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <ConfigurationProfileSelector
              onActiveProfileChange={setActiveProfile}
              onProfileChange={() => {
                // Refresh profiles when changed
              }}
            />
            <ModelDropdown activeProfile={activeProfile} />
            <Button
              variant="outline"
              size="sm"
              asChild
              className="cursor-pointer cyber-border terminal-text hover:bg-secondary/50 transition-colors"
            >
              <a href="/dashboard">Dashboard</a>
            </Button>
            <Button
              variant="outline"
              size="sm"
              asChild
              className="cursor-pointer cyber-border terminal-text hover:bg-secondary/50 transition-colors"
            >
              <a href="/tools/cve" className="flex items-center gap-2">
                <Shield className="w-4 h-4" />
                CVE Search
              </a>
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setIsSettingsSidebarOpen(true)}
              className="cursor-pointer cyber-border terminal-text hover:bg-secondary/50 transition-colors"
            >
              <Settings className="w-4 h-4" />
            </Button>
          </div>

          {user && (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  size="sm"
                  className="flex items-center gap-2 px-3 py-1 hover:bg-secondary/50 transition-colors cursor-pointer"
                >
                  <User className="w-4 h-4 text-primary" />
                  <span className="text-sm text-foreground">{user.username}</span>
                  <ChevronDown className="w-3 h-3 opacity-50" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48 bg-card cyber-border">
                <DropdownMenuItem
                  onClick={logout}
                  className="cursor-pointer flex items-center gap-2"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          )}
        </div>
      </div>

      <SettingsSidebar
        isOpen={isSettingsSidebarOpen}
        onClose={() => setIsSettingsSidebarOpen(false)}
        onProfilesChange={() => {
          // Profiles will be refreshed automatically by the selector
        }}
      />
    </header>
  );
}
