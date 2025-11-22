import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { X, Upload, Download, Plus, Trash2, Save, Loader2, CheckCircle2, Settings } from "lucide-react";
import { llmService, ConfigurationProfile, Provider, AvailableModel } from "@/lib/api/llm";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface SettingsSidebarProps {
  isOpen: boolean;
  onClose: () => void;
  onProfilesChange: () => void;
}

export function SettingsSidebar({
  isOpen,
  onClose,
  onProfilesChange,
}: SettingsSidebarProps) {
  const [profiles, setProfiles] = useState<ConfigurationProfile[]>([]);
  const [providers, setProviders] = useState<Provider[]>([]);
  const [isCreating, setIsCreating] = useState(false);
  const [editingProfileId, setEditingProfileId] = useState<number | null>(null);

  // Form state
  const [profileName, setProfileName] = useState("");
  const [selectedProvider, setSelectedProvider] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [availableModels, setAvailableModels] = useState<AvailableModel[]>([]);
  const [selectedModelName, setSelectedModelName] = useState("");
  const [isFetchingModels, setIsFetchingModels] = useState(false);

  const fetchProfiles = async () => {
    try {
      const data = await llmService.getProfiles();
      setProfiles(data);
    } catch (error) {
      console.error("Failed to fetch profiles", error);
    }
  };

  const fetchProviders = async () => {
    try {
      const data = await llmService.getProviders();
      setProviders(data.providers);
    } catch (error) {
      console.error("Failed to fetch providers", error);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchProfiles();
      fetchProviders();
    }
  }, [isOpen]);

  const resetForm = () => {
    setProfileName("");
    setSelectedProvider("");
    setApiKey("");
    setAvailableModels([]);
    setSelectedModelName("");
    setIsCreating(false);
    setEditingProfileId(null);
  };

  const handleFetchModels = async () => {
    if (!selectedProvider || !apiKey) return;
    setIsFetchingModels(true);
    try {
      const response = await llmService.fetchModels(selectedProvider, apiKey);
      setAvailableModels(response.models);
    } catch (error) {
      console.error("Failed to fetch models", error);
      alert("Failed to fetch models. Please check your API key.");
    } finally {
      setIsFetchingModels(false);
    }
  };

  const handleSaveProfile = async () => {
    if (!profileName || !selectedProvider || !apiKey) {
      alert("Please fill all fields (Model selection is optional)");
      return;
    }

    try {
      if (editingProfileId) {
        // Update existing profile
        await llmService.updateProfile(editingProfileId, {
          name: profileName,
          api_provider: selectedProvider,
          api_key: apiKey,
          selected_model_name: selectedModelName,
        });
      } else {
        // Create new profile
        await llmService.createProfile({
          name: profileName,
          api_provider: selectedProvider,
          api_key: apiKey,
          selected_model_name: selectedModelName,
        });
      }

      resetForm();
      await fetchProfiles();
      onProfilesChange();
    } catch (error) {
      console.error("Failed to save profile", error);
      alert("Failed to save profile");
    }
  };

  const handleEditProfile = (profile: ConfigurationProfile) => {
    setEditingProfileId(profile.id);
    setProfileName(profile.name);
    setSelectedProvider(profile.api_provider);
    setSelectedModelName(profile.selected_model_name || "");
    setIsCreating(true);
    // Note: We can't pre-fill API key since it's masked
  };

  const handleActivateProfile = async (profileId: number) => {
    try {
      await llmService.activateProfile(profileId);
      await fetchProfiles();
      onProfilesChange();
    } catch (error) {
      console.error("Failed to activate profile", error);
    }
  };

  const handleDeleteProfile = async (profileId: number) => {
    if (!confirm("Are you sure you want to delete this profile?")) return;
    try {
      await llmService.deleteProfile(profileId);
      await fetchProfiles();
      onProfilesChange();
    } catch (error) {
      console.error("Failed to delete profile", error);
    }
  };

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      await llmService.importConfig(file);
      await fetchProfiles();
      onProfilesChange();
      alert("Configuration imported successfully!");
    } catch (error) {
      console.error("Failed to import config", error);
      alert("Failed to import configuration");
    }
  };

  const handleExport = async () => {
    try {
      const config = await llmService.exportConfig();
      const blob = new Blob([JSON.stringify(config, null, 2)], {
        type: "application/json",
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "llm-config.json";
      a.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Failed to export config", error);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/50" onClick={onClose}>
      <div
        className="fixed right-0 top-0 h-full w-full max-w-2xl bg-card border-l border-border overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold">Configuration Settings</h2>
            <Button variant="ghost" size="icon" onClick={onClose}>
              <X className="w-5 h-5" />
            </Button>
          </div>

          {/* Import/Export */}
          <div className="flex gap-2 mb-6">
            <Button variant="outline" size="sm" onClick={handleExport}>
              <Download className="w-4 h-4 mr-2" />
              Export Config
            </Button>
            <label>
              <Button variant="outline" size="sm" asChild>
                <span>
                  <Upload className="w-4 h-4 mr-2" />
                  Import Config
                </span>
              </Button>
              <input
                type="file"
                accept=".json"
                className="hidden"
                onChange={handleImport}
              />
            </label>
          </div>

          {/* Profiles List */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold">Configuration Profiles</h3>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsCreating(true)}
              >
                <Plus className="w-4 h-4 mr-2" />
                Add Profile
              </Button>
            </div>

            {/* Create/Edit Profile Form */}
            {isCreating && (
              <div className="p-4 border border-border rounded-lg bg-secondary/20 space-y-3">
                <h4 className="font-medium">
                  {editingProfileId ? "Edit Profile" : "New Profile"}
                </h4>
                
                <Input
                  placeholder="Profile name"
                  value={profileName}
                  onChange={(e) => setProfileName(e.target.value)}
                />

                <Select
                  value={selectedProvider}
                  onValueChange={setSelectedProvider}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select API Provider" />
                  </SelectTrigger>
                  <SelectContent>
                    {providers.map((provider) => (
                      <SelectItem key={provider.id} value={provider.id}>
                        {provider.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>

                <Input
                  type="password"
                  placeholder="API Key"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                />

                <Button
                  size="sm"
                  onClick={handleFetchModels}
                  disabled={!selectedProvider || !apiKey || isFetchingModels}
                  className="w-full"
                >
                  {isFetchingModels ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Fetching Models...
                    </>
                  ) : (
                    "Fetch Available Models"
                  )}
                </Button>

                {availableModels.length > 0 && (
                  <Select
                    value={selectedModelName}
                    onValueChange={setSelectedModelName}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select Model" />
                    </SelectTrigger>
                    <SelectContent>
                      {availableModels.map((model) => (
                        <SelectItem key={model.id} value={model.id}>
                          {model.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}

                <div className="flex gap-2">
                  <Button
                    size="sm"
                    onClick={handleSaveProfile}
                    disabled={!profileName || !selectedProvider || !apiKey}
                  >
                    <Save className="w-4 h-4 mr-2" />
                    Save
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={resetForm}
                  >
                    Cancel
                  </Button>
                </div>
              </div>
            )}

            {/* Existing Profiles */}
            {profiles.map((profile) => (
              <div
                key={profile.id}
                className="p-4 border border-border rounded-lg space-y-2"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium">{profile.name}</h4>
                    {profile.is_active ? (
                      <span className="text-xs text-primary flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3" /> Active
                      </span>
                    ) : (
                      <Button
                        variant="link"
                        size="sm"
                        className="h-auto p-0 text-xs text-muted-foreground hover:text-primary"
                        onClick={() => handleActivateProfile(profile.id)}
                      >
                        Set Active
                      </Button>
                    )}
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => handleEditProfile(profile)}
                    >
                      <Settings className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => handleDeleteProfile(profile.id)}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>

                <div className="text-sm text-muted-foreground space-y-1">
                  <div>Provider: {profile.api_provider}</div>
                  <div>API Key: {profile.api_key_masked}</div>
                  <div>Model: {profile.selected_model_name || "Not selected"}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
