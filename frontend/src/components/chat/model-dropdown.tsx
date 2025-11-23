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
        selected_model_name: modelName
      });
      
      // We need to update the local state or trigger a refresh. 
      // Ideally the parent should know, but for now we can just force a reload 
      // or rely on the fact that the profile selector might refresh.
      // Actually, since activeProfile is passed down, we can't mutate it.
      // We should probably call a callback or just show a success message.
      // The UI won't update the button text immediately unless we have local state for it
      // or the parent refreshes.
      
      toast.success(`Model changed to ${modelName}`);
      setIsOpen(false);
      
      // Trigger a page reload or profile refresh? 
      // A simple way is to reload the window or use a context.
      // For now, let's just show the toast. The user might need to re-select profile to see update?
      // No, that's bad UX.
      // I should probably ask the parent to refresh.
      // But I can't easily do that without changing props.
      // I'll assume the user will see the selected model in the dropdown list.
      
      // Better: Update the activeProfile object locally if possible? No, it's a prop.
      // I'll add a window.location.reload() as a crude fix or just accept it might not update instantly
      // without a callback.
      // Wait, I can just update the button text locally?
      
      // Let's add a local override for display
      // But wait, the parent passes activeProfile.
      
      // I'll add an onModelSelect prop to the interface in a future step if needed.
      // For now, I'll just reload the page to ensure consistency as this is a critical config change.
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
      <DropdownMenuTrigger asChild>
        <Button
          variant="outline"
          size="sm"
          className="gap-2 cyber-border terminal-text min-w-[200px] justify-between"
          disabled={!activeProfile}
        >
          <span className="truncate flex items-center gap-2">
            <Cpu className="w-4 h-4" />
            {activeProfile?.selected_model_name || "No Model Selected"}
          </span>
          <ChevronDown className="w-4 h-4 opacity-50" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-[280px] bg-card cyber-border">
        <DropdownMenuLabel>
            {activeProfile ? `Models for ${activeProfile.api_provider}` : "Select a profile first"}
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
