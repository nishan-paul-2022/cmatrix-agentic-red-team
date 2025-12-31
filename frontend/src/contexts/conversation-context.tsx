"use client";

import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import type { Conversation, ConversationWithHistory } from "@/types/conversation.types";
import * as conversationApi from "@/lib/api/conversations";

interface ConversationContextType {
  conversations: Conversation[];
  activeConversation: Conversation | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  createConversation: (name?: string) => Promise<Conversation>;
  selectConversation: (conversation: Conversation | null) => void;
  updateConversation: (id: number, name: string) => Promise<void>;
  deleteConversation: (id: number) => Promise<void>;
  loadConversations: () => Promise<void>;
  loadConversationHistory: (id: number) => Promise<ConversationWithHistory>;
}

const ConversationContext = createContext<ConversationContextType | undefined>(undefined);

export function ConversationProvider({ children }: { children: React.ReactNode }) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversation, setActiveConversation] = useState<Conversation | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Track initialization
  const initializedRef = React.useRef(false);

  // Load conversations on mount
  const loadConversations = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await conversationApi.getConversations();
      setConversations(response.conversations);

      // If not initialized and we have conversations, select the first one
      // We use a functional update to check if there's already an active conversation
      // to avoid adding activeConversation to the dependency array
      if (!initializedRef.current && response.conversations.length > 0) {
        setActiveConversation((current) => {
          if (!current) {
            return response.conversations[0];
          }
          return current;
        });
        initializedRef.current = true;
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to load conversations";
      setError(errorMessage);
      console.error("Failed to load conversations:", err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Create new conversation
  const createConversation = useCallback(async (name?: string): Promise<Conversation> => {
    try {
      setError(null);
      const newConversation = await conversationApi.createConversation({ name });

      // Add to conversations list
      setConversations((prev) => [newConversation, ...prev]);

      // Set as active
      setActiveConversation(newConversation);

      return newConversation;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to create conversation";
      setError(errorMessage);
      throw err;
    }
  }, []);

  // Select conversation
  const selectConversation = useCallback((conversation: Conversation | null) => {
    setActiveConversation(conversation);
  }, []);

  // Update conversation
  const updateConversation = useCallback(
    async (id: number, name: string) => {
      try {
        setError(null);
        const updatedConversation = await conversationApi.updateConversation(id, { name });

        // Update in conversations list
        setConversations((prev) =>
          prev.map((conv) => (conv.id === id ? updatedConversation : conv))
        );

        // Update active conversation if it's the one being updated
        if (activeConversation?.id === id) {
          setActiveConversation(updatedConversation);
        }
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : "Failed to update conversation";
        setError(errorMessage);
        throw err;
      }
    },
    [activeConversation]
  );

  // Delete conversation
  const deleteConversation = useCallback(
    async (id: number) => {
      try {
        setError(null);
        await conversationApi.deleteConversation(id);

        // Remove from conversations list
        setConversations((prev) => prev.filter((conv) => conv.id !== id));

        // If deleted conversation was active, select another one
        if (activeConversation?.id === id) {
          const remainingConversations = conversations.filter((conv) => conv.id !== id);
          setActiveConversation(
            remainingConversations.length > 0 ? remainingConversations[0] : null
          );
        }
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : "Failed to delete conversation";
        setError(errorMessage);
        throw err;
      }
    },
    [activeConversation, conversations]
  );

  // Load conversation with history
  const loadConversationHistory = useCallback(
    async (id: number): Promise<ConversationWithHistory> => {
      try {
        setError(null);
        return await conversationApi.getConversation(id);
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Failed to load conversation history";
        setError(errorMessage);
        throw err;
      }
    },
    []
  );

  // Load conversations on mount
  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  const value: ConversationContextType = {
    conversations,
    activeConversation,
    isLoading,
    error,
    createConversation,
    selectConversation,
    updateConversation,
    deleteConversation,
    loadConversations,
    loadConversationHistory,
  };

  return <ConversationContext.Provider value={value}>{children}</ConversationContext.Provider>;
}

export function useConversations() {
  const context = useContext(ConversationContext);
  if (context === undefined) {
    throw new Error("useConversations must be used within a ConversationProvider");
  }
  return context;
}
