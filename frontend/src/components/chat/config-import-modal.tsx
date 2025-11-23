import { useState, useRef } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Upload, FileText, CheckCircle2, AlertCircle, Key } from "lucide-react";
import { llmService } from "@/lib/api/llm";

interface ConfigImportModalProps {
  isOpen: boolean;
  onClose: () => void;
  onImportSuccess: () => void;
}

interface ImportResult {
  message: string;
  imported_configs: Array<{
    provider: string;
    model: string;
    has_api_key: boolean;
    activated: boolean;
  }>;
  default_provider_set: boolean;
}

export function ConfigImportModal({ isOpen, onClose, onImportSuccess }: ConfigImportModalProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isImporting, setIsImporting] = useState(false);
  const [importResult, setImportResult] = useState<ImportResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.type !== "application/json" && !file.name.endsWith(".json")) {
        setError("Please select a valid JSON file");
        return;
      }
      setSelectedFile(file);
      setError(null);
      setImportResult(null);
    }
  };

  const handleImport = async () => {
    if (!selectedFile) return;

    setIsImporting(true);
    setError(null);

    try {
      const result = await llmService.importConfig(selectedFile);
      setImportResult(result);
      onImportSuccess();
    } catch (err: any) {
      console.error("Import error:", err);
      setError(err.message || "Failed to import configuration");
    } finally {
      setIsImporting(false);
    }
  };

  const handleClose = () => {
    setSelectedFile(null);
    setImportResult(null);
    setError(null);
    onClose();
  };

  const handleDragOver = (event: React.DragEvent) => {
    event.preventDefault();
  };

  const handleDrop = (event: React.DragEvent) => {
    event.preventDefault();
    const file = event.dataTransfer.files?.[0];
    if (file) {
      if (file.type !== "application/json" && !file.name.endsWith(".json")) {
        setError("Please select a valid JSON file");
        return;
      }
      setSelectedFile(file);
      setError(null);
      setImportResult(null);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="max-w-2xl bg-card cyber-border">
        <DialogHeader>
          <DialogTitle className="terminal-text text-xl">Import LLM Configuration</DialogTitle>
        </DialogHeader>

        <div className="space-y-6">
          {/* File Upload Section */}
          {!importResult && (
            <div
              className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary/50 transition-colors cursor-pointer"
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".json,application/json"
                onChange={handleFileSelect}
                className="hidden"
              />

              <div className="flex flex-col items-center gap-4">
                <Upload className="w-12 h-12 text-muted-foreground" />
                <div>
                  <p className="text-lg font-medium">
                    {selectedFile ? selectedFile.name : "Drop your JSON config file here"}
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">
                    or click to browse files
                  </p>
                </div>
                {selectedFile && (
                  <div className="flex items-center gap-2 text-sm text-green-500">
                    <FileText className="w-4 h-4" />
                    <span>{selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)</span>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="flex items-center gap-2 p-3 bg-destructive/10 border border-destructive/20 rounded-lg text-destructive">
              <AlertCircle className="w-4 h-4" />
              <span className="text-sm">{error}</span>
            </div>
          )}

          {/* Import Result */}
          {importResult && (
            <div className="space-y-4">
              <div className="flex items-center gap-2 p-3 bg-green-500/10 border border-green-500/20 rounded-lg text-green-700 dark:text-green-400">
                <CheckCircle2 className="w-4 h-4" />
                <span className="text-sm font-medium">{importResult.message}</span>
              </div>

              {importResult.default_provider_set && (
                <div className="text-sm text-muted-foreground">
                  ✓ Default provider has been activated
                </div>
              )}

              <div className="space-y-2">
                <h4 className="font-medium">Imported Configurations:</h4>
                <div className="max-h-40 overflow-y-auto space-y-1">
                  {importResult.imported_configs.map((config, index) => (
                    <div key={index} className="flex items-center justify-between p-2 bg-secondary/50 rounded text-sm">
                      <div className="flex items-center gap-2">
                        <span className="font-medium">{config.provider}</span>
                        <span className="text-muted-foreground">({config.model})</span>
                      </div>
                      <div className="flex items-center gap-2">
                        {config.has_api_key && <Key className="w-3 h-3 text-green-500" />}
                        {config.activated && <CheckCircle2 className="w-3 h-3 text-green-500" />}
                        <span className="text-xs text-muted-foreground">
                          {config.has_api_key ? "Key set" : "No key"}
                          {config.activated ? " • Active" : ""}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex justify-end gap-3">
            {!importResult ? (
              <>
                <Button variant="outline" onClick={handleClose}>
                  Cancel
                </Button>
                <Button
                  onClick={handleImport}
                  disabled={!selectedFile || isImporting}
                >
                  {isImporting ? "Importing..." : "Import Configuration"}
                </Button>
              </>
            ) : (
              <Button onClick={handleClose}>
                Close
              </Button>
            )}
          </div>

          {/* Instructions */}
          <div className="text-sm text-muted-foreground border-t pt-4">
            <p className="font-medium mb-2">Expected JSON format:</p>
            <pre className="bg-secondary/50 p-3 rounded text-xs overflow-x-auto">
{`{
  "default_provider": "gemini",
  "providers": {
    "gemini": {
      "enabled": true,
      "model": "gemini-2.5-pro",
      "api_keys": ["key1", "key2", "key3"]
    },
    "openrouter": {
      "enabled": false,
      "model": "x-ai/grok-4-fast:free",
      "api_key": "sk-or-v1-..."
    }
  }
}`}
            </pre>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}