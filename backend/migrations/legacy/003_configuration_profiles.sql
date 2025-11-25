-- Migration: Simplified Configuration Profile Schema
-- Description: One API provider, one API key, one model per profile

-- Drop old tables
DROP TABLE IF EXISTS language_models CASCADE;
DROP TABLE IF EXISTS configuration_profiles CASCADE;

-- Drop old triggers and functions
DROP TRIGGER IF EXISTS trigger_ensure_single_selected_model ON language_models;
DROP TRIGGER IF EXISTS trigger_update_language_models_updated_at ON language_models;
DROP TRIGGER IF EXISTS trigger_ensure_single_active_profile ON configuration_profiles;
DROP TRIGGER IF EXISTS trigger_update_configuration_profiles_updated_at ON configuration_profiles;
DROP FUNCTION IF EXISTS ensure_single_selected_model();
DROP FUNCTION IF EXISTS update_language_models_updated_at();
DROP FUNCTION IF EXISTS ensure_single_active_profile();
DROP FUNCTION IF EXISTS update_configuration_profiles_updated_at();

-- Create simplified configuration_profiles table
CREATE TABLE IF NOT EXISTS configuration_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    api_provider VARCHAR(50) NOT NULL CHECK (api_provider IN ('Cerebras', 'Gemini', 'Hugging Face', 'Kilo Code', 'Openrouter')),
    api_key TEXT NOT NULL,
    selected_model_name VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_profile FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT unique_user_profile_name UNIQUE (user_id, name)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_configuration_profiles_user_id ON configuration_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_configuration_profiles_is_active ON configuration_profiles(user_id, is_active);
CREATE INDEX IF NOT EXISTS idx_configuration_profiles_provider ON configuration_profiles(api_provider);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_configuration_profiles_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_configuration_profiles_updated_at
    BEFORE UPDATE ON configuration_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_configuration_profiles_updated_at();

-- Ensure only one active profile per user
CREATE OR REPLACE FUNCTION ensure_single_active_profile()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_active = true THEN
        UPDATE configuration_profiles
        SET is_active = false
        WHERE user_id = NEW.user_id AND id != NEW.id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_ensure_single_active_profile
    BEFORE INSERT OR UPDATE ON configuration_profiles
    FOR EACH ROW
    WHEN (NEW.is_active = true)
    EXECUTE FUNCTION ensure_single_active_profile();
