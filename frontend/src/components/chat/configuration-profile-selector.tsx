import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Settings, ChevronDown, CheckCircle2 } from "lucide-react";
import { llmService, ConfigurationProfile } from "@/lib/api/llm";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { SettingsSidebar } from "@/components/chat/settings-sidebar";

interface ConfigurationProfileSelectorProps {
  onProfileChange?: () => void;
  onActiveProfileChange?: (profile: ConfigurationProfile | null) => void;
}

export function ConfigurationProfileSelector({
  onProfileChange,
  onActiveProfileChange,
}: ConfigurationProfileSelectorProps) {
  const [profiles, setProfiles] = useState<ConfigurationProfile[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

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
      setIsModalOpen(false);
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

  return (
    <>
      <Button
        variant="outline"
        size="sm"
        className="gap-2 cyber-border terminal-text min-w-[180px] justify-between"
        onClick={() => {
            setIsModalOpen(true);
            fetchProfiles();
        }}
      >
        <span className="truncate">
          {activeProfile?.name || "Select Profile"}
        </span>
        <ChevronDown className="w-4 h-4 opacity-50" />
      </Button>

      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent className="bg-card cyber-border">
          <DialogHeader>
            <div className="flex items-center justify-between">
              <DialogTitle>Configuration Profiles</DialogTitle>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  setIsModalOpen(false);
                  setIsSidebarOpen(true);
                }}
              >
                <Settings className="w-4 h-4 mr-2" />
                Settings
              </Button>
            </div>
          </DialogHeader>

          <div className="space-y-2 mt-4">
            {profiles.map((profile) => {
                const isActive = activeProfile?.id === profile.id;
                return (
              <div
                key={profile.id}
                className={`p-3 rounded-lg border cursor-pointer hover:bg-secondary/50 transition-colors ${
                  isActive
                    ? "border-primary bg-primary/10"
                    : "border-border"
                }`}
                onClick={() => handleActivateProfile(profile.id)}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium">{profile.name}</div>
                    <div className="text-xs text-muted-foreground">
                      {profile.api_provider} • {profile.selected_model_name || "No model"}
                    </div>
                  </div>
                  {isActive && (
                    <CheckCircle2 className="w-5 h-5 text-primary" />
                  )}
                </div>
              </div>
            )})}

            {profiles.length === 0 && (
              <div className="text-center text-muted-foreground py-8">
                No profiles configured. Click Settings to create one.
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>

      <SettingsSidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        onProfilesChange={() => {
          fetchProfiles();
          onProfileChange?.();
        }}
      />
    </>
  );
}
