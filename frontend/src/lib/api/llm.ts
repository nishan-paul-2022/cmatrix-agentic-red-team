import { apiConfig } from "@/config/api.config";

export interface ConfigurationProfile {
  id: number;
  user_id: number;
  name: string;
  api_provider: string;
  api_key_masked: string;
  selected_model_name?: string;
  is_active: boolean;
}

export interface CreateProfileRequest {
  name: string;
  api_provider: string;
  api_key: string;
  selected_model_name?: string;
}

export interface UpdateProfileRequest {
  name?: string;
  api_provider?: string;
  api_key?: string;
  selected_model_name?: string;
}

export interface FetchModelsRequest {
  api_provider: string;
  api_key: string;
}

export interface AvailableModel {
  id: string;
  name: string;
  description?: string;
  context_length?: number;
}

export interface FetchModelsResponse {
  provider: string;
  models: AvailableModel[];
}

export interface Provider {
  id: string;
  name: string;
}

export const llmService = {
  // Profile management
  getProfiles: async (): Promise<ConfigurationProfile[]> => {
    const response = await fetch(`${apiConfig.baseUrl}/llm/profiles`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
      },
    });
    if (!response.ok) throw new Error("Failed to fetch profiles");
    return response.json();
  },

  createProfile: async (data: CreateProfileRequest): Promise<ConfigurationProfile> => {
    const response = await fetch(`${apiConfig.baseUrl}/llm/profiles`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to create profile");
    return response.json();
  },

  updateProfile: async (
    id: number,
    data: UpdateProfileRequest
  ): Promise<ConfigurationProfile> => {
    const response = await fetch(`${apiConfig.baseUrl}/llm/profiles/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to update profile");
    return response.json();
  },

  deleteProfile: async (id: number): Promise<void> => {
    const response = await fetch(`${apiConfig.baseUrl}/llm/profiles/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
      },
    });
    if (!response.ok) throw new Error("Failed to delete profile");
  },

  activateProfile: async (id: number): Promise<void> => {
    const response = await fetch(
      `${apiConfig.baseUrl}/llm/profiles/${id}/activate`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
        },
      }
    );
    if (!response.ok) throw new Error("Failed to activate profile");
  },

  // Provider management
  getProviders: async (): Promise<{ providers: Provider[] }> => {
    const response = await fetch(`${apiConfig.baseUrl}/llm/providers`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
      },
    });
    if (!response.ok) throw new Error("Failed to fetch providers");
    return response.json();
  },

  fetchModels: async (
    provider: string,
    apiKey: string
  ): Promise<FetchModelsResponse> => {
    const response = await fetch(
      `${apiConfig.baseUrl}/llm/providers/fetch-models`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
        },
        body: JSON.stringify({ api_provider: provider, api_key: apiKey }),
      }
    );
    if (!response.ok) throw new Error("Failed to fetch models");
    return response.json();
  },

  fetchProfileModels: async (profileId: number): Promise<FetchModelsResponse> => {
    const response = await fetch(
      `${apiConfig.baseUrl}/llm/profiles/${profileId}/models`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
        },
      }
    );
    if (!response.ok) throw new Error("Failed to fetch profile models");
    return response.json();
  },

  // Import/Export
  importConfig: async (file: File): Promise<any> => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${apiConfig.baseUrl}/llm/config/import`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
      },
      body: formData,
    });
    if (!response.ok) throw new Error("Failed to import config");
    return response.json();
  },

  exportConfig: async (): Promise<any> => {
    const response = await fetch(`${apiConfig.baseUrl}/llm/config/export`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
      },
    });
    if (!response.ok) throw new Error("Failed to export config");
    return response.json();
  },
};
