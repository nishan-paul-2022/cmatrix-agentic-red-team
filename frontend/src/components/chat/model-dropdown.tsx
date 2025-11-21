import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { ChevronDown, Cpu } from "lucide-react";
import { llmService, ConfigurationProfile } from "@/lib/api/llm";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export function ModelDropdown() {
  const [profiles, setProfiles] = useState<ConfigurationProfile[]>([]);
  const [activeProfile, setActiveProfile] = useState<ConfigurationProfile | null>(null);

  const fetchProfiles = async () => {
    try {
      const data = await llmService.getProfiles();
      setProfiles(data);

      // Find active profile
      const active = data.find((p) => p.is_active);
      setActiveProfile(active || null);
    } catch (error) {
      console.error("Failed to fetch profiles", error);
    }
  };

  useEffect(() => {
    fetchProfiles();
  }, []);

  const handleSelectProfile = async (profileId: number) => {
    try {
      await llmService.activateProfile(profileId);
      await fetchProfiles();
    } catch (error) {
      console.error("Failed to activate profile", error);
    }
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="outline"
          size="sm"
          className="gap-2 cyber-border terminal-text min-w-[200px] justify-between"
        >
          <span className="truncate flex items-center gap-2">
            <Cpu className="w-4 h-4" />
            {activeProfile?.selected_model_name || "No Model Selected"}
          </span>
          <ChevronDown className="w-4 h-4 opacity-50" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-[280px] bg-card cyber-border">
        <DropdownMenuLabel>Switch Profile/Model</DropdownMenuLabel>
        <DropdownMenuSeparator />
        {profiles.map((profile) => (
          <DropdownMenuItem
            key={profile.id}
            onClick={() => handleSelectProfile(profile.id)}
            className="cursor-pointer flex-col items-start gap-1"
          >
            <div className="flex items-center justify-between w-full">
              <span className="font-medium">{profile.name}</span>
              {profile.is_active && (
                <div className="w-2 h-2 bg-primary rounded-full" />
              )}
            </div>
            <span className="text-xs text-muted-foreground">
              {profile.api_provider} • {profile.selected_model_name || "No model"}
            </span>
          </DropdownMenuItem>
        ))}

        {profiles.length === 0 && (
          <div className="text-center text-muted-foreground py-4 text-sm">
            No profiles configured
          </div>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
