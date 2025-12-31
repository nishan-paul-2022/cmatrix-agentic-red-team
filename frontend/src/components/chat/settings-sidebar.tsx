import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  X,
  Upload,
  Download,
  Plus,
  Trash2,
  Save,
  Loader2,
  Edit2,
  Key,
  Sparkles,
  Filter,
} from "lucide-react";
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

export function SettingsSidebar({ isOpen, onClose, onProfilesChange }: SettingsSidebarProps) {
  const [profiles, setProfiles] = useState<ConfigurationProfile[]>([]);
  const [providers, setProviders] = useState<Provider[]>([]);
  const [isCreating, setIsCreating] = useState(false);
  const [editingProfileId, setEditingProfileId] = useState<number | null>(null);
  const [selectedProviderFilter, setSelectedProviderFilter] = useState<string>("all");

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

  useEffect(() => {
    const fetchModels = async () => {
      if (!selectedProvider) return;

      // Case 1: User provided a new API key
      if (apiKey) {
        setIsFetchingModels(true);
        try {
          const response = await llmService.fetchModels(selectedProvider, apiKey);
          setAvailableModels(response.models);
        } catch (error) {
          console.error("Failed to fetch models", error);
          setAvailableModels([]);
        } finally {
          setIsFetchingModels(false);
        }
      }
      // Case 2: Editing existing profile (using stored key)
      else if (editingProfileId) {
        const profile = profiles.find((p) => p.id === editingProfileId);
        // Only fetch if the selected provider matches the profile's provider
        if (profile && profile.api_provider === selectedProvider) {
          setIsFetchingModels(true);
          try {
            const response = await llmService.fetchProfileModels(editingProfileId);
            setAvailableModels(response.models);
          } catch (error) {
            console.error("Failed to fetch stored models", error);
          } finally {
            setIsFetchingModels(false);
          }
        }
      }
    };

    // Debounce only if typing API key
    if (apiKey) {
      const timer = setTimeout(fetchModels, 800);
      return () => clearTimeout(timer);
    } else {
      fetchModels();
    }
  }, [selectedProvider, apiKey, editingProfileId, profiles]);

  const handleSaveProfile = async () => {
    // Validation logic
    const isEditing = !!editingProfileId;
    const profile = profiles.find((p) => p.id === editingProfileId);
    const isProviderChanged = isEditing && profile?.api_provider !== selectedProvider;

    // Require API key if:
    // 1. Creating a new profile
    // 2. Editing and provider changed
    // 3. Editing and user explicitly cleared/changed key (handled by apiKey state being non-empty if typed, but here we check if it's required)
    // Actually, if apiKey is empty string, it means user didn't type anything.

    const isApiKeyRequired = !isEditing || isProviderChanged;

    if (!profileName || !selectedProvider || (isApiKeyRequired && !apiKey)) {
      alert("Please fill all required fields");
      return;
    }

    try {
      if (editingProfileId) {
        const updateData: any = {
          name: profileName,
          api_provider: selectedProvider,
          selected_model_name: selectedModelName,
        };

        // Only include API key if user entered one
        if (apiKey) {
          updateData.api_key = apiKey;
        }

        await llmService.updateProfile(editingProfileId, updateData);
      } else {
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

  // Filter profiles by provider
  const filteredProfiles =
    selectedProviderFilter === "all"
      ? profiles
      : profiles.filter((p) => p.api_provider === selectedProviderFilter);

  // Group profiles by provider for display
  const profilesByProvider = profiles.reduce(
    (acc, profile) => {
      if (!acc[profile.api_provider]) {
        acc[profile.api_provider] = [];
      }
      acc[profile.api_provider].push(profile);
      return acc;
    },
    {} as Record<string, ConfigurationProfile[]>
  );

  // Get provider name from ID
  const getProviderName = (providerId: string) => {
    return providers.find((p) => p.id === providerId)?.name || providerId;
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm transition-opacity duration-300"
      onClick={onClose}
    >
      <div
        className="fixed right-0 top-0 h-full w-full max-w-xl bg-gradient-to-br from-card via-card to-card/95 border-l border-border/50 shadow-2xl overflow-hidden flex flex-col animate-in slide-in-from-right duration-300"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex-shrink-0 px-5 py-4 border-b border-border/50 bg-muted/20">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="p-1.5 rounded-lg bg-secondary">
                <Sparkles className="w-4 h-4 text-primary/80" />
              </div>
              <div>
                <h2 className="text-xl font-bold tracking-tight">LLM Configuration</h2>
                <p className="text-xs text-muted-foreground mt-0.5">Provider Configurations</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={onClose}
              className="hover:bg-destructive/10 hover:text-destructive transition-colors cursor-pointer"
            >
              <X className="w-5 h-5" />
            </Button>
          </div>
        </div>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto px-5 py-5">
          {/* Import/Export Section */}
          <div className="mb-6">
            <div className="flex items-center gap-2 p-3 rounded-lg bg-secondary/30 border border-border/50">
              <div className="flex gap-2 flex-1">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleExport}
                  className="hover:bg-primary/10 hover:text-primary hover:border-primary/50 transition-all cursor-pointer"
                >
                  <Download className="w-4 h-4 mr-2" />
                  Export
                </Button>
                <label>
                  <Button
                    variant="outline"
                    size="sm"
                    asChild
                    className="hover:bg-primary/10 hover:text-primary hover:border-primary/50 transition-all cursor-pointer"
                  >
                    <span>
                      <Upload className="w-4 h-4 mr-2" />
                      Import
                    </span>
                  </Button>
                  <input type="file" accept=".json" className="hidden" onChange={handleImport} />
                </label>
              </div>
              <div className="text-xs font-medium text-foreground/80">
                Backup & restore configurations
              </div>
            </div>
          </div>

          {/* Profiles Section */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-base font-semibold">Saved Configurations</h3>
              </div>
              <Button
                onClick={() => {
                  resetForm();
                  setIsCreating(true);
                }}
                size="sm"
                className="h-7 rounded-full px-3 text-xs font-medium bg-primary/10 text-primary hover:bg-primary hover:text-primary-foreground border border-primary/10 hover:border-primary transition-all duration-300 shadow-sm hover:shadow-primary/25 active:scale-95 cursor-pointer"
              >
                <Plus className="w-3.5 h-3.5" />
                New
              </Button>
            </div>

            {/* Provider Filter */}
            {profiles.length > 0 && (
              <div className="flex items-center gap-2 p-2.5 rounded-lg bg-secondary/20 border border-border/30">
                <Filter className="w-3.5 h-3.5 text-muted-foreground" />
                <Select value={selectedProviderFilter} onValueChange={setSelectedProviderFilter}>
                  <SelectTrigger className="h-7 w-[160px] bg-background/50 border-border/50 text-xs cursor-pointer">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all" className="cursor-pointer">
                      All Providers ({profiles.length})
                    </SelectItem>
                    {Object.keys(profilesByProvider).map((providerId) => (
                      <SelectItem key={providerId} value={providerId} className="cursor-pointer">
                        {getProviderName(providerId)} ({profilesByProvider[providerId].length})
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}

            {/* New Profile Form (Inline) */}
            {isCreating && !editingProfileId && (
              <div className="p-4 border border-border rounded-lg bg-muted/30 shadow-sm space-y-3 animate-in fade-in slide-in-from-top-4 duration-200">
                <div className="flex items-center justify-between mb-1">
                  <h4 className="text-sm font-semibold flex items-center gap-1.5">
                    <Plus className="w-3.5 h-3.5 text-primary" />
                    New Configuration
                  </h4>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={resetForm}
                    className="h-7 text-xs text-muted-foreground hover:text-foreground cursor-pointer"
                  >
                    Cancel
                  </Button>
                </div>

                <div className="space-y-2.5">
                  <div className="grid grid-cols-2 gap-3">
                    <Input
                      placeholder="Profile name *"
                      value={profileName}
                      onChange={(e) => setProfileName(e.target.value)}
                      className="bg-background/50 h-9 text-sm"
                      autoComplete="off"
                    />

                    <Select value={selectedProvider} onValueChange={setSelectedProvider}>
                      <SelectTrigger className="bg-background/50 h-9 text-sm cursor-pointer">
                        <SelectValue placeholder="Provider *" />
                      </SelectTrigger>
                      <SelectContent>
                        {providers.map((provider) => (
                          <SelectItem
                            key={provider.id}
                            value={provider.id}
                            className="cursor-pointer"
                          >
                            {provider.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <Input
                    type="password"
                    placeholder="API Key *"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    className="bg-background/50 font-mono text-xs h-9"
                    autoComplete="off"
                  />

                  <Select
                    value={selectedModelName}
                    onValueChange={setSelectedModelName}
                    disabled={isFetchingModels}
                  >
                    <SelectTrigger className="bg-background/50 h-9 text-sm cursor-pointer">
                      {isFetchingModels ? (
                        <div className="flex items-center text-muted-foreground">
                          <Loader2 className="w-3.5 h-3.5 mr-2 animate-spin" />
                          Loading models...
                        </div>
                      ) : (
                        <SelectValue placeholder="Select model (optional)" />
                      )}
                    </SelectTrigger>
                    <SelectContent>
                      {!selectedProvider && !apiKey ? (
                        <div className="flex flex-col items-center justify-center py-3 px-2 text-center">
                          <span className="text-xs text-muted-foreground">
                            Please select a provider and enter an API key
                          </span>
                        </div>
                      ) : !selectedProvider ? (
                        <div className="flex flex-col items-center justify-center py-3 px-2 text-center">
                          <span className="text-xs text-muted-foreground">
                            Please select a provider first
                          </span>
                        </div>
                      ) : !apiKey ? (
                        <div className="flex flex-col items-center justify-center py-3 px-2 text-center">
                          <span className="text-xs text-muted-foreground">
                            Please enter an API key first
                          </span>
                        </div>
                      ) : availableModels.length === 0 ? (
                        <div className="flex flex-col items-center justify-center py-3 px-2 text-center">
                          <span className="text-xs text-muted-foreground">
                            {isFetchingModels ? "Loading models..." : "No models available"}
                          </span>
                        </div>
                      ) : (
                        availableModels.map((model) => (
                          <SelectItem key={model.id} value={model.id} className="cursor-pointer">
                            {model.name}
                          </SelectItem>
                        ))
                      )}
                    </SelectContent>
                  </Select>
                </div>

                <Button
                  onClick={handleSaveProfile}
                  disabled={!profileName || !selectedProvider || !apiKey}
                  className="w-full h-9 cursor-pointer"
                  size="sm"
                >
                  <Save className="w-3.5 h-3.5 mr-2" />
                  Create Configuration
                </Button>
              </div>
            )}

            {/* Profiles List */}
            {filteredProfiles.length === 0 && !isCreating ? (
              <div className="text-center py-12 px-4">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-secondary/50 mb-4">
                  <Sparkles className="w-8 h-8 text-muted-foreground" />
                </div>
                <h4 className="text-lg font-medium mb-2">No configurations found</h4>
                <p className="text-sm text-muted-foreground mb-6">
                  Initialize a new provider setup to enable inference
                </p>
                <Button onClick={() => setIsCreating(true)} className="cursor-pointer">
                  <Plus className="w-4 h-4 mr-2" />
                  New Configuration
                </Button>
              </div>
            ) : (
              <div className="space-y-2.5">
                {filteredProfiles.map((profile) => {
                  const isEditing = editingProfileId === profile.id;

                  return (
                    <div
                      key={profile.id}
                      className={`group relative rounded-xl border transition-all duration-200 ${
                        isEditing
                          ? "border-primary/30 bg-muted/30 shadow-md"
                          : profile.is_active
                            ? "border-primary/30 bg-primary/5 shadow-sm hover:shadow-md"
                            : "border-border/40 bg-card hover:border-border/60 hover:bg-secondary/20 hover:shadow-sm"
                      }`}
                    >
                      {isEditing ? (
                        // Inline Edit Form
                        <div className="p-4 space-y-3 animate-in fade-in duration-200">
                          <div className="flex items-center justify-between mb-1">
                            <h4 className="text-sm font-semibold flex items-center gap-1.5">
                              <Edit2 className="w-3.5 h-3.5 text-primary" />
                              Edit Configuration
                            </h4>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={resetForm}
                              className="h-7 text-xs text-muted-foreground hover:text-foreground cursor-pointer"
                            >
                              Cancel
                            </Button>
                          </div>

                          <div className="space-y-2.5">
                            <div className="grid grid-cols-2 gap-3">
                              <Input
                                placeholder="Profile name *"
                                value={profileName}
                                onChange={(e) => setProfileName(e.target.value)}
                                className="bg-background/50 h-9 text-sm"
                                autoComplete="off"
                              />

                              <Select value={selectedProvider} onValueChange={setSelectedProvider}>
                                <SelectTrigger className="bg-background/50 h-9 text-sm cursor-pointer">
                                  <SelectValue placeholder="Provider *" />
                                </SelectTrigger>
                                <SelectContent>
                                  {providers.map((provider) => (
                                    <SelectItem
                                      key={provider.id}
                                      value={provider.id}
                                      className="cursor-pointer"
                                    >
                                      {provider.name}
                                    </SelectItem>
                                  ))}
                                </SelectContent>
                              </Select>
                            </div>

                            <Input
                              type="password"
                              placeholder="API Key * (leave empty to keep current)"
                              value={apiKey}
                              onChange={(e) => setApiKey(e.target.value)}
                              className="bg-background/50 font-mono text-xs h-9"
                              autoComplete="off"
                            />

                            <Select
                              value={selectedModelName}
                              onValueChange={setSelectedModelName}
                              disabled={isFetchingModels}
                            >
                              <SelectTrigger className="bg-background/50 h-9 text-sm cursor-pointer">
                                {isFetchingModels ? (
                                  <div className="flex items-center text-muted-foreground">
                                    <Loader2 className="w-3.5 h-3.5 mr-2 animate-spin" />
                                    Loading models...
                                  </div>
                                ) : (
                                  <SelectValue placeholder="Select model (optional)" />
                                )}
                              </SelectTrigger>
                              <SelectContent>
                                {!selectedProvider && !apiKey ? (
                                  <div className="flex flex-col items-center justify-center py-3 px-2 text-center">
                                    <span className="text-xs text-muted-foreground">
                                      Please select a provider and enter an API key
                                    </span>
                                  </div>
                                ) : !selectedProvider ? (
                                  <div className="flex flex-col items-center justify-center py-3 px-2 text-center">
                                    <span className="text-xs text-muted-foreground">
                                      Please select a provider first
                                    </span>
                                  </div>
                                ) : !apiKey &&
                                  profiles.find((p) => p.id === editingProfileId)?.api_provider !==
                                    selectedProvider ? (
                                  <div className="flex flex-col items-center justify-center py-3 px-2 text-center">
                                    <span className="text-xs text-muted-foreground">
                                      Please enter an API key first
                                    </span>
                                  </div>
                                ) : availableModels.length === 0 ? (
                                  <div className="flex flex-col items-center justify-center py-3 px-2 text-center">
                                    <span className="text-xs text-muted-foreground">
                                      {isFetchingModels
                                        ? "Loading models..."
                                        : "No models available"}
                                    </span>
                                  </div>
                                ) : (
                                  availableModels.map((model) => (
                                    <SelectItem
                                      key={model.id}
                                      value={model.id}
                                      className="cursor-pointer"
                                    >
                                      {model.name}
                                    </SelectItem>
                                  ))
                                )}
                              </SelectContent>
                            </Select>
                          </div>

                          <Button
                            onClick={handleSaveProfile}
                            disabled={!profileName || !selectedProvider}
                            className="w-full h-9 cursor-pointer"
                            size="sm"
                          >
                            <Save className="w-3.5 h-3.5 mr-2" />
                            Update Configuration
                          </Button>
                        </div>
                      ) : (
                        // Profile Display
                        <div className="px-3.5 py-3">
                          <div className="flex items-center gap-3">
                            {/* Status Indicator & Icon */}
                            <div className="relative flex-shrink-0">
                              <div
                                className={`p-2 rounded-lg transition-colors ${
                                  profile.is_active ? "bg-primary/10" : "bg-secondary"
                                }`}
                              >
                                <Key
                                  className={`w-4 h-4 ${
                                    profile.is_active ? "text-primary" : "text-muted-foreground"
                                  }`}
                                />
                              </div>
                              {profile.is_active && (
                                <div className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-primary rounded-full border-2 border-card" />
                              )}
                            </div>

                            {/* Profile Info */}
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 mb-1">
                                <h4 className="font-semibold text-sm truncate">{profile.name}</h4>
                              </div>
                              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                                <span className="font-medium text-foreground/70">
                                  {getProviderName(profile.api_provider)}
                                </span>
                                {profile.selected_model_name && (
                                  <>
                                    <span className="text-border">•</span>
                                    <span className="truncate">{profile.selected_model_name}</span>
                                  </>
                                )}
                              </div>
                            </div>

                            {/* Actions */}
                            <div className="flex items-center gap-2 flex-shrink-0">
                              {profile.is_active ? (
                                <div className="h-7 px-3 flex items-center justify-center text-xs font-medium bg-primary/10 text-primary rounded-md border border-primary/20 select-none">
                                  Active
                                </div>
                              ) : (
                                <Button
                                  size="sm"
                                  variant="outline"
                                  onClick={() => handleActivateProfile(profile.id)}
                                  className="h-7 px-3 text-xs border-primary/30 hover:bg-primary/10 hover:text-primary hover:border-primary/50 transition-all cursor-pointer"
                                >
                                  Active
                                </Button>
                              )}
                              <div className="flex items-center gap-0.5">
                                <Button
                                  variant="ghost"
                                  size="icon"
                                  onClick={() => handleEditProfile(profile)}
                                  className="h-8 w-8 text-muted-foreground hover:text-primary hover:bg-primary/10 transition-colors cursor-pointer"
                                >
                                  <Edit2 className="w-3.5 h-3.5" />
                                </Button>
                                <Button
                                  variant="ghost"
                                  size="icon"
                                  onClick={() => handleDeleteProfile(profile.id)}
                                  className="h-8 w-8 text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-colors cursor-pointer"
                                >
                                  <Trash2 className="w-3.5 h-3.5" />
                                </Button>
                              </div>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
