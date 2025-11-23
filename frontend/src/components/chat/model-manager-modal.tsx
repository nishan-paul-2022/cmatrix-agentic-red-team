// @ts-nocheck
import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Save, Eye, EyeOff, CheckCircle2, Key, Upload } from "lucide-react";
import { llmService, LLMModel } from "@/lib/api/llm";
import { ConfigImportModal } from "./config-import-modal";

interface ModelManagerModalProps {
  isOpen: boolean;
  onClose: () => void;
  onModelChange: () => void;
}

export function ModelManagerModal({ isOpen, onClose, onModelChange }: ModelManagerModalProps) {
  const [models, setModels] = useState<LLMModel[]>([]);
  const [editingModelId, setEditingModelId] = useState<number | null>(null);
  const [apiKey, setApiKey] = useState("");
  const [showApiKey, setShowApiKey] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showImportModal, setShowImportModal] = useState(false);

  useEffect(() => {
    if (isOpen) {
      fetchModels();
    }
  }, [isOpen]);

  const fetchModels = async () => {
    try {
      const data = await llmService.getModels();
      setModels(data);
    } catch (error) {
      console.error("Failed to fetch models", error);
    }
  };

  const handleSave = async () => {
    if (!editingModelId || !apiKey) return;

    setIsLoading(true);
    try {
      await llmService.updateApiKey(editingModelId, apiKey);
      await fetchModels();
      setEditingModelId(null);
      setApiKey("");
      setShowApiKey(false);
      onModelChange();
    } catch (error) {
      console.error("Failed to save API key", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleActivate = async (modelId: number) => {
    setIsLoading(true);
    try {
      await llmService.activateModel(modelId);
      await fetchModels();
      onModelChange();
    } catch (error) {
      console.error("Failed to activate model", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = (model: LLMModel) => {
    setEditingModelId(model.id);
    setApiKey("");
    setShowApiKey(false);
  };

  return (
    <>
      <Dialog open={isOpen} onOpenChange={onClose}>
        <DialogContent className="max-w-3xl bg-card cyber-border">
          <DialogHeader>
            <div className="flex items-center justify-between">
              <DialogTitle className="terminal-text text-xl">Manage LLM API Keys</DialogTitle>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowImportModal(true)}
              >
                <Upload className="w-4 h-4 mr-2" />
                Import Config
              </Button>
            </div>
          </DialogHeader>

        <div className="space-y-4 max-h-[500px] overflow-y-auto">
          {models.map((model) => (
            <div 
              key={model.id} 
              className={`p-4 rounded border ${editingModelId === model.id ? 'bg-secondary border-primary' : 'border-border hover:bg-secondary/50'}`}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="font-semibold">{model.name}</h3>
                    {model.is_active && <CheckCircle2 className="w-4 h-4 text-green-500" />}
                    {model.has_api_key && <Key className="w-4 h-4 text-green-500" />}
                  </div>
                  <p className="text-sm text-muted-foreground mb-2">{model.description || model.provider}</p>
                  
                  {editingModelId === model.id ? (
                    <div className="space-y-3 mt-3">
                      <div className="flex gap-2">
                        <div className="relative flex-1">
                          <Input 
                            type={showApiKey ? "text" : "password"}
                            value={apiKey} 
                            onChange={(e) => setApiKey(e.target.value)}
                            placeholder="Enter API key..."
                            className="pr-10"
                          />
                          <button
                            type="button"
                            onClick={() => setShowApiKey(!showApiKey)}
                            className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                          >
                            {showApiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                          </button>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <Button 
                          size="sm" 
                          onClick={handleSave} 
                          disabled={isLoading || !apiKey}
                        >
                          <Save className="w-4 h-4 mr-2" />
                          Save API Key
                        </Button>
                        <Button 
                          size="sm" 
                          variant="outline" 
                          onClick={() => {
                            setEditingModelId(null);
                            setApiKey("");
                            setShowApiKey(false);
                          }}
                        >
                          Cancel
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <div className="flex items-center gap-2 mt-2">
                      {model.has_api_key && (
                        <span className="text-xs text-muted-foreground">
                          API Key: {model.api_key_masked}
                        </span>
                      )}
                    </div>
                  )}
                </div>

                <div className="flex flex-col gap-2">
                  {editingModelId !== model.id && (
                    <>
                      <Button 
                        size="sm" 
                        variant="outline"
                        onClick={() => handleEdit(model)}
                      >
                        {model.has_api_key ? "Update Key" : "Add Key"}
                      </Button>
                      {model.has_api_key && !model.is_active && (
                        <Button 
                          size="sm" 
                          onClick={() => handleActivate(model.id)}
                          disabled={isLoading}
                        >
                          Activate
                        </Button>
                      )}
                      {model.is_active && (
                        <span className="text-xs text-green-500 text-center">Active</span>
                      )}
                    </>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="text-sm text-muted-foreground mt-4">
          <p>• Configure API keys for the models you want to use</p>
          <p>• Only one model can be active at a time</p>
          <p>• API keys are stored securely in the database</p>
        </div>
      </DialogContent>
    </Dialog>

    <ConfigImportModal
      isOpen={showImportModal}
      onClose={() => setShowImportModal(false)}
      onImportSuccess={() => {
        setShowImportModal(false);
        fetchModels();
        onModelChange();
      }}
    />
    </>
  );
}
