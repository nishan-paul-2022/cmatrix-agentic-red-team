# Configuration Import/Export JSON Format (Simplified)

## Export Format

When you export your configuration, you'll get a JSON file in this format:

```json
{
  "profiles": [
    {
      "name": "Work Profile",
      "api_provider": "Gemini",
      "api_key": "AIzaSyD...your-key-here",
      "selected_model_name": "gemini-2.0-flash-exp",
      "is_active": true
    },
    {
      "name": "Personal Profile",
      "api_provider": "Cerebras",
      "api_key": "csk-...your-key-here",
      "selected_model_name": "llama3.3-70b",
      "is_active": false
    }
  ]
}
```

## Import Format

You can import a configuration using the same format. The system will:
1. Create all profiles listed
2. Activate the profile marked with `"is_active": true`

### Minimal Example

```json
{
  "profiles": [
    {
      "name": "My Profile",
      "api_provider": "Gemini",
      "api_key": "YOUR_GEMINI_API_KEY",
      "selected_model_name": "gemini-2.0-flash-exp",
      "is_active": true
    }
  ]
}
```

## Field Descriptions

### Profile Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Name of the configuration profile |
| `api_provider` | string | Yes | Must be one of: "Cerebras", "Gemini", "Hugging Face", "Kilo Code", "Openrouter" |
| `api_key` | string | Yes | Your API key for the provider |
| `selected_model_name` | string | No | The model name (e.g., "gemini-2.0-flash-exp") |
| `is_active` | boolean | No | Whether this profile should be active (default: false) |

## How It Works

**One Profile = One Provider + One Key + One Model**

Each configuration profile contains:
- **ONE** API provider (e.g., Gemini, Cerebras)
- **ONE** API key for that provider
- **ONE** selected model from that provider's free models

The system automatically fetches available free models from the provider when you enter your API key.

## Supported API Providers

### 1. Cerebras
- **Provider ID**: `"Cerebras"`
- **Example models**: `"llama3.3-70b"`, `"llama3.1-8b"`
- **API Key format**: `csk-...`

### 2. Gemini
- **Provider ID**: `"Gemini"`
- **Example models**: `"gemini-2.0-flash-exp"`, `"gemini-1.5-pro"`
- **API Key format**: `AIzaSy...`

### 3. Hugging Face
- **Provider ID**: `"Hugging Face"`
- **Example models**: `"meta-llama/Llama-3.2-3B-Instruct"`, `"mistralai/Mistral-7B-Instruct-v0.3"`
- **API Key format**: `hf_...`

### 4. Kilo Code
- **Provider ID**: `"Kilo Code"`
- **Example models**: `"x-ai/grok-code-fast-1"`
- **API Key format**: Varies

### 5. Openrouter
- **Provider ID**: `"Openrouter"`
- **Example models**: `"x-ai/grok-beta"`, `"anthropic/claude-3.5-sonnet"`
- **API Key format**: `sk-or-v1-...`

## Usage

### Creating a Profile

1. Click **"Select Profile"** button → **"Settings"**
2. Click **"Add Profile"**
3. Enter:
   - Profile name
   - Select API provider
   - Enter API key
   - Click **"Fetch Available Models"** (dynamic fetch)
   - Select your desired model
4. Click **"Save"**

### Export Configuration

1. Click **"Export Config"** button in settings sidebar
2. File `llm-config.json` will download automatically
3. Save it securely (contains your API keys!)

### Import Configuration

1. Click **"Import Config"** button in settings sidebar
2. Select your JSON file
3. System will create all profiles
4. Active profile will be set automatically

## Notes

> [!WARNING]
> **Security**: Exported JSON files contain your API keys in plain text. Store them securely and never commit them to version control.

> [!TIP]
> **Sharing**: You can share configurations with others by replacing the `api_key` values with placeholders like `"YOUR_API_KEY_HERE"` before sharing.

> [!IMPORTANT]
> **Provider Names**: The `api_provider` field is case-sensitive and must exactly match one of the 5 supported providers.

> [!NOTE]
> **Dynamic Model Fetching**: The system fetches available free models in real-time from each provider's API. No hardcoded model lists!
