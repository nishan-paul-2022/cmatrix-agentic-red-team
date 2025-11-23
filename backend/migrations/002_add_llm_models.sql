-- Migration: Add LLM model management tables
-- Description: Creates master_llm_models and user_model_mappings tables for database-based LLM configuration

-- Create master_llm_models table
CREATE TABLE IF NOT EXISTS master_llm_models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    provider VARCHAR(100) NOT NULL,
    default_model_name VARCHAR(255),
    status VARCHAR(50) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index on provider for faster queries
CREATE INDEX IF NOT EXISTS idx_master_llm_models_provider ON master_llm_models(provider);
CREATE INDEX IF NOT EXISTS idx_master_llm_models_status ON master_llm_models(status);

-- Create user_model_mappings table
CREATE TABLE IF NOT EXISTS user_model_mappings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    llm_model_id INTEGER NOT NULL REFERENCES master_llm_models(id) ON DELETE CASCADE,
    api_key TEXT,
    is_active BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_mapping FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_llm_model FOREIGN KEY (llm_model_id) REFERENCES master_llm_models(id) ON DELETE CASCADE,
    CONSTRAINT unique_user_model UNIQUE (user_id, llm_model_id)
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_user_model_mappings_user_id ON user_model_mappings(user_id);
CREATE INDEX IF NOT EXISTS idx_user_model_mappings_llm_model_id ON user_model_mappings(llm_model_id);
CREATE INDEX IF NOT EXISTS idx_user_model_mappings_is_active ON user_model_mappings(user_id, is_active);

-- Create trigger to update updated_at timestamp on master_llm_models
CREATE OR REPLACE FUNCTION update_master_llm_models_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_master_llm_models_updated_at
    BEFORE UPDATE ON master_llm_models
    FOR EACH ROW
    EXECUTE FUNCTION update_master_llm_models_updated_at();

-- Create trigger to update updated_at timestamp on user_model_mappings
CREATE OR REPLACE FUNCTION update_user_model_mappings_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_user_model_mappings_updated_at
    BEFORE UPDATE ON user_model_mappings
    FOR EACH ROW
    EXECUTE FUNCTION update_user_model_mappings_updated_at();

-- Ensure only one active model per user
CREATE OR REPLACE FUNCTION ensure_single_active_model()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_active = true THEN
        UPDATE user_model_mappings
        SET is_active = false
        WHERE user_id = NEW.user_id AND id != NEW.id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_ensure_single_active_model
    BEFORE INSERT OR UPDATE ON user_model_mappings
    FOR EACH ROW
    WHEN (NEW.is_active = true)
    EXECUTE FUNCTION ensure_single_active_model();

-- Seed master LLM models
INSERT INTO master_llm_models (name, description, provider, default_model_name, status) VALUES
    ('Gemini 2.5 Pro', 'Google Gemini 2.5 Pro - Advanced reasoning and long context', 'gemini', 'gemini-2.5-pro', 'active'),
    ('Gemini 2.0 Flash', 'Google Gemini 2.0 Flash - Fast and efficient', 'gemini', 'gemini-2.0-flash', 'active'),
    ('Gemini 1.5 Pro', 'Google Gemini 1.5 Pro - Production ready', 'gemini', 'gemini-1.5-pro', 'active'),
    ('OpenRouter - Grok Fast', 'X.AI Grok Fast via OpenRouter', 'openrouter', 'x-ai/grok-4-fast:free', 'active'),
    ('OpenRouter - GPT-4', 'OpenAI GPT-4 via OpenRouter', 'openrouter', 'openai/gpt-4', 'active'),
    ('OpenRouter - Claude 3.5', 'Anthropic Claude 3.5 via OpenRouter', 'openrouter', 'anthropic/claude-3.5-sonnet', 'active'),
    ('Cerebras - Llama 3.3 70B', 'Meta Llama 3.3 70B via Cerebras', 'cerebras', 'llama3.3-70b', 'active'),
    ('Cerebras - GPT OSS 120B', 'GPT OSS 120B via Cerebras', 'cerebras', 'gpt-oss-120b', 'active'),
    ('Ollama - Llama 3.2', 'Local Llama 3.2 via Ollama', 'ollama', 'llama3.2', 'active'),
    ('Ollama - Gemma 3 4B', 'Local Gemma 3 4B via Ollama', 'ollama', 'gemma3:4b', 'active'),
    ('Ollama - Qwen 2.5', 'Local Qwen 2.5 via Ollama', 'ollama', 'qwen2.5', 'active'),
    ('KiloCode - Grok Fast', 'X.AI Grok Code Fast via KiloCode', 'kilocode', 'x-ai/grok-code-fast-1', 'active'),
    ('HuggingFace - DeepHat V1', 'DeepHat V1 7B via HuggingFace', 'huggingface', 'DeepHat/DeepHat-V1-7B', 'active')
ON CONFLICT (name) DO NOTHING;
