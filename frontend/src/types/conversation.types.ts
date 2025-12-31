/**
 * Conversation-related type definitions
 */

export interface Conversation {
  id: number;
  name: string;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface ConversationHistory {
  id: number;
  conversation_id: number;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export interface ConversationWithHistory extends Conversation {
  history: ConversationHistory[];
}

export interface ConversationCreateRequest {
  name?: string;
}

export interface ConversationUpdateRequest {
  name: string;
}

export interface ConversationListResponse {
  conversations: Conversation[];
  total: number;
}
