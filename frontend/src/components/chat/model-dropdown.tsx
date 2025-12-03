import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { ChevronDown, Cpu, Loader2, CheckCircle2 } from "lucide-react";
import { llmService, ConfigurationProfile, AvailableModel } from "@/lib/api/llm";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { toast } from "sonner";

interface ModelDropdownProps {
  activeProfile: ConfigurationProfile | null;
}

export function ModelDropdown({ activeProfile }: ModelDropdownProps) {
  const [models, setModels] = useState<AvailableModel[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  const fetchModels = async () => {
    if (!activeProfile) return;

    setIsLoading(true);
    try {
      const response = await llmService.fetchProfileModels(activeProfile.id);
      setModels(response.models);
    } catch (error) {
      console.error("Failed to fetch models", error);
      toast.error("Failed to fetch available models");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectModel = async (modelName: string) => {
    if (!activeProfile) return;

    try {
      await llmService.updateProfile(activeProfile.id, {
        selected_model_name: modelName,
      });

      toast.success(`Model changed to ${modelName}`);
      setIsOpen(false);

      // Force reload to update context/UI
      window.location.reload();
    } catch (error) {
      console.error("Failed to update profile model", error);
      toast.error("Failed to update model selection");
    }
  };

  useEffect(() => {
    if (isOpen && activeProfile) {
      fetchModels();
    }
  }, [isOpen, activeProfile]);

  return (
    <DropdownMenu open={isOpen} onOpenChange={setIsOpen}>
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
                  className="gap-2 cyber-border terminal-text min-w-[200px] justify-between cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                  disabled={!activeProfile}
                >
                  <span className="truncate flex items-center gap-2">
                    <Cpu className="w-4 h-4" />
                    {activeProfile?.selected_model_name || "Select Model"}
                  </span>
                  <ChevronDown className="w-4 h-4 opacity-50" />
                </Button>
              </DropdownMenuTrigger>
            </span>
          </TooltipTrigger>
          {!activeProfile && (
            <TooltipContent>
              <p>Configuration required</p>
            </TooltipContent>
          )}
        </Tooltip>
      </TooltipProvider>

      <DropdownMenuContent align="end" className="w-[280px] bg-card cyber-border">
        <DropdownMenuLabel>
          {activeProfile ? `Models for ${activeProfile.api_provider}` : "Configuration Required"}
        </DropdownMenuLabel>
        <DropdownMenuSeparator />

        {isLoading ? (
          <div className="flex items-center justify-center py-4">
            <Loader2 className="w-4 h-4 animate-spin mr-2" />
            <span className="text-xs text-muted-foreground">Fetching models...</span>
          </div>
        ) : (
          <>
            {models.map((model) => (
              <DropdownMenuItem
                key={model.id}
                onClick={() => handleSelectModel(model.id)}
                className="cursor-pointer flex-col items-start gap-1"
              >
                <div className="flex items-center justify-between w-full">
                  <span className="font-medium">{model.name}</span>
                  {activeProfile?.selected_model_name === model.id && (
                    <CheckCircle2 className="w-3 h-3 text-primary" />
                  )}
                </div>
                {model.description && (
                  <span className="text-xs text-muted-foreground line-clamp-1">
                    {model.description}
                  </span>
                )}
              </DropdownMenuItem>
            ))}

            {models.length === 0 && (
              <div className="text-center text-muted-foreground py-4 text-sm">
                No models found for this provider.
              </div>
            )}
          </>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
