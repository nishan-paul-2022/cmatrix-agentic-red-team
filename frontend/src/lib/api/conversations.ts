/**
 * Conversation API client functions
 */

import { apiConfig } from "@/config/api.config";
import type {
  Conversation,
  ConversationCreateRequest,
  ConversationUpdateRequest,
  ConversationListResponse,
  ConversationWithHistory,
} from "@/types/conversation.types";

/**
 * Get authorization headers
 */
function getAuthHeaders(): Record<string, string> {
  const token = localStorage.getItem("auth_token");
  return {
    ...apiConfig.headers,
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

/**
 * Create a new conversation
 */
export async function createConversation(
  data: ConversationCreateRequest = {}
): Promise<Conversation> {
  const response = await fetch(`${apiConfig.baseUrl}${apiConfig.endpoints.conversations}`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: "Failed to create conversation" }));
    throw new Error(error.error || "Failed to create conversation");
  }

  return response.json();
}

/**
 * Get all conversations for the current user
 */
export async function getConversations(): Promise<ConversationListResponse> {
  const response = await fetch(`${apiConfig.baseUrl}${apiConfig.endpoints.conversations}`, {
    method: "GET",
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: "Failed to fetch conversations" }));
    throw new Error(error.error || "Failed to fetch conversations");
  }

  return response.json();
}

/**
 * Get a specific conversation with its history
 */
export async function getConversation(conversationId: number): Promise<ConversationWithHistory> {
  const response = await fetch(
    `${apiConfig.baseUrl}${apiConfig.endpoints.conversations}/${conversationId}`,
    {
      method: "GET",
      headers: getAuthHeaders(),
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: "Failed to fetch conversation" }));
    throw new Error(error.error || "Failed to fetch conversation");
  }

  return response.json();
}

/**
 * Update a conversation (rename)
 */
export async function updateConversation(
  conversationId: number,
  data: ConversationUpdateRequest
): Promise<Conversation> {
  const response = await fetch(
    `${apiConfig.baseUrl}${apiConfig.endpoints.conversations}/${conversationId}`,
    {
      method: "PATCH",
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: "Failed to update conversation" }));
    throw new Error(error.error || "Failed to update conversation");
  }

  return response.json();
}

/**
 * Delete a conversation
 */
export async function deleteConversation(conversationId: number): Promise<void> {
  const response = await fetch(
    `${apiConfig.baseUrl}${apiConfig.endpoints.conversations}/${conversationId}`,
    {
      method: "DELETE",
      headers: getAuthHeaders(),
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: "Failed to delete conversation" }));
    throw new Error(error.error || "Failed to delete conversation");
  }
}
