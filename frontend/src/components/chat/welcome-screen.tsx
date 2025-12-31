"use client";

import { BrandLogo } from "@/components/brand-logo";
import { MESSAGES } from "@/constants/messages";

interface WelcomeScreenProps {
  onSuggestionClick: (prompt: string) => void;
}

/**
 * Welcome screen component
 * Displays when there are no messages in the chat
 */
export function WelcomeScreen({ onSuggestionClick }: WelcomeScreenProps) {
  return (
    <div className="flex flex-col items-center justify-center h-full gap-8 py-12">
      <div className="flex items-center justify-center gap-6">
        <div className="flex items-center justify-center w-20 h-20 rounded-2xl bg-secondary cyber-border">
          <BrandLogo size={48} />
        </div>
        <div className="text-left">
          <h2 className="text-4xl font-bold text-balance terminal-text">
            {MESSAGES.WELCOME.TITLE}
          </h2>
          <div className="text-sm text-muted-foreground terminal-text mt-2">
            {MESSAGES.WELCOME.SUBTITLE}
          </div>
        </div>
      </div>

      <div className="text-center space-y-4">
        <p className="text-muted-foreground text-pretty max-w-md terminal-text">
          {MESSAGES.WELCOME.DESCRIPTION}
        </p>
      </div>

      <div className="grid gap-3 mt-4 sm:grid-cols-2">
        <button
          onClick={() => onSuggestionClick(MESSAGES.SUGGESTIONS.SECURITY_SCAN.PROMPT)}
          className="px-4 py-3 text-sm text-left transition-colors border rounded-lg border-border hover:bg-accent hover:text-accent-foreground cyber-border cursor-pointer"
        >
          <div className="font-medium terminal-text">
            {MESSAGES.SUGGESTIONS.SECURITY_SCAN.TITLE}
          </div>
          <div className="text-xs text-muted-foreground">
            {MESSAGES.SUGGESTIONS.SECURITY_SCAN.DESCRIPTION}
          </div>
        </button>
        <button
          onClick={() => onSuggestionClick(MESSAGES.SUGGESTIONS.SYSTEM_STATUS.PROMPT)}
          className="px-4 py-3 text-sm text-left transition-colors border rounded-lg border-border hover:bg-accent hover:text-accent-foreground cyber-border cursor-pointer"
        >
          <div className="font-medium terminal-text">
            {MESSAGES.SUGGESTIONS.SYSTEM_STATUS.TITLE}
          </div>
          <div className="text-xs text-muted-foreground">
            {MESSAGES.SUGGESTIONS.SYSTEM_STATUS.DESCRIPTION}
          </div>
        </button>
      </div>
    </div>
  );
}
