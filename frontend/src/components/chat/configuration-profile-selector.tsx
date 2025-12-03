import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { ChevronDown, CheckCircle2 } from "lucide-react";
import { llmService, ConfigurationProfile } from "@/lib/api/llm";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

interface ConfigurationProfileSelectorProps {
  onProfileChange?: () => void;
  onActiveProfileChange?: (profile: ConfigurationProfile | null) => void;
}

export function ConfigurationProfileSelector({
  onProfileChange,
  onActiveProfileChange,
}: ConfigurationProfileSelectorProps) {
  const [profiles, setProfiles] = useState<ConfigurationProfile[]>([]);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const fetchProfiles = async () => {
    try {
      const data = await llmService.getProfiles();
      setProfiles(data);
    } catch (error) {
      console.error("Failed to fetch profiles", error);
    }
  };

  useEffect(() => {
    fetchProfiles();
  }, []);

  const handleActivateProfile = async (profileId: number) => {
    try {
      await llmService.activateProfile(profileId);
      await fetchProfiles();
      setIsDropdownOpen(false);
      onProfileChange?.();
    } catch (error) {
      console.error("Failed to activate profile", error);
    }
  };

  const activeProfile = profiles.find((p) => p.is_active);

  useEffect(() => {
    if (activeProfile && onActiveProfileChange) {
      onActiveProfileChange(activeProfile);
    } else if (!activeProfile && onActiveProfileChange) {
      // Handle case where no profile is active
      onActiveProfileChange(null);
    }
  }, [activeProfile?.id, onActiveProfileChange]); // Only trigger if ID changes

  const hasProfiles = profiles.length > 0;

  return (
    <DropdownMenu open={isDropdownOpen} onOpenChange={setIsDropdownOpen}>
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <span tabIndex={0} className="inline-block">
              {" "}
              {/* Wrapper for disabled button tooltip */}
              <DropdownMenuTrigger asChild>
                <Button
                  variant="outline"
                  size="sm"
                  className="gap-2 cyber-border terminal-text min-w-[180px] justify-between cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                  onClick={() => {
                    fetchProfiles();
                  }}
                  disabled={!hasProfiles}
                >
                  <span className="truncate">{activeProfile?.name || "Load Configuration"}</span>
                  <ChevronDown className="w-4 h-4 opacity-50" />
                </Button>
              </DropdownMenuTrigger>
            </span>
          </TooltipTrigger>
          {!hasProfiles && (
            <TooltipContent>
              <p>
                Setup Required • Open Settings <span className="text-primary">⚙️</span>
              </p>
            </TooltipContent>
          )}
        </Tooltip>
      </TooltipProvider>

      <DropdownMenuContent
        align="start"
        className="w-[320px] bg-card cyber-border max-h-[400px] overflow-y-auto custom-scrollbar"
      >
        {profiles.length === 0 ? (
          <div className="text-center text-muted-foreground py-8 px-4 text-sm">
            No profiles configured. Click Settings to create one.
          </div>
        ) : (
          profiles.map((profile) => {
            const isActive = activeProfile?.id === profile.id;
            return (
              <DropdownMenuItem
                key={profile.id}
                className={`p-3 cursor-pointer focus:bg-secondary/50 ${
                  isActive ? "bg-primary/10" : ""
                }`}
                onClick={() => handleActivateProfile(profile.id)}
              >
                <div className="flex items-center justify-between w-full">
                  <div className="flex-1 min-w-0">
                    <div className="font-medium truncate">{profile.name}</div>
                    <div className="text-xs text-muted-foreground truncate">
                      {profile.api_provider} • {profile.selected_model_name || "No model"}
                    </div>
                  </div>
                  {isActive && <CheckCircle2 className="w-5 h-5 text-primary ml-2 flex-shrink-0" />}
                </div>
              </DropdownMenuItem>
            );
          })
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
