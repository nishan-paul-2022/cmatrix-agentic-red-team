"use client";

import { useState, useCallback, useEffect } from "react";
import type { ChatMessage, StreamChunk, AnimationStep, NetworkDiagram } from "@/types/chat.types";
import type { ConversationWithHistory } from "@/types/conversation.types";
import { apiConfig } from "@/config/api.config";
import { MESSAGES } from "@/constants/messages";
import { useConversations } from "@/contexts/conversation-context";

interface UseChatStreamReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  isAnimating: boolean;
  currentAnimationStep: number;
  sendMessage: (message: string) => Promise<void>;
  setInput: (input: string) => void;
  input: string;
}

/**
 * Hook for handling chat streaming functionality
 */
export function useChatStream(): UseChatStreamReturn {
  const { activeConversation, loadConversationHistory, createConversation } = useConversations();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false);
  const [currentAnimationStep, setCurrentAnimationStep] = useState(0);

  // Load conversation history when active conversation changes
  useEffect(() => {
    const loadMessages = async () => {
      if (activeConversation) {
        try {
          const conversationData = await loadConversationHistory(activeConversation.id);
          const chatMessages: ChatMessage[] = conversationData.history.map(h => ({
            role: h.role as "user" | "assistant",
            content: h.content,
          }));
          setMessages(chatMessages);
        } catch (error) {
          console.error('Failed to load conversation history:', error);
          setMessages([]);
        }
      } else {
        setMessages([]);
      }
    };

    loadMessages();
  }, [activeConversation, loadConversationHistory]);

  const sendMessage = useCallback(
    async (userMessage: string) => {
      if (!userMessage.trim() || isLoading) return;

      // Ensure we have an active conversation
      let conversationId = activeConversation?.id;
      if (!conversationId) {
        try {
          const newConversation = await createConversation();
          conversationId = newConversation.id;
        } catch (error) {
          console.error('Failed to create conversation:', error);
          return;
        }
      }

      // Add user message
      setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
      setIsLoading(true);
      setIsAnimating(false);
      setCurrentAnimationStep(0);

      try {
        // Get auth token from localStorage
        const token = localStorage.getItem('auth_token');
        if (!token) {
          throw new Error('Not authenticated. Please log in.');
        }

        const response = await fetch(`${apiConfig.baseUrl}${apiConfig.endpoints.chatStream}`, {
          method: "POST",
          headers: {
            ...apiConfig.headers,
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({
            message: userMessage,
            conversation_id: conversationId,
            history: messages.slice(-10), // Last 10 messages for context
          }),
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({
            error: MESSAGES.ERRORS.GENERIC,
          }));
          throw new Error(errorData.error || MESSAGES.ERRORS.FETCH_FAILED);
        }

        const reader = response.body?.getReader();
        if (!reader) {
          throw new Error(MESSAGES.ERRORS.NO_RESPONSE);
        }

        const decoder = new TextDecoder();
        let assistantMessage = "";
        let receivedAnimationSteps: AnimationStep[] = [];
        let receivedDiagram: NetworkDiagram | null = null;

        // Add empty assistant message
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: "", animationSteps: [] },
        ]);

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split("\n").filter((line) => line.trim() !== "");

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              const data = line.slice(6).trim();
              if (data === "[DONE]") continue;

              try {
                const parsed: StreamChunk = JSON.parse(data);

                if (parsed.animation_step) {
                  // Handle animation step
                  receivedAnimationSteps.push(parsed.animation_step);
                  setIsAnimating(true);
                  setIsLoading(false);

                  // Update message with animation steps
                  setMessages((prev) => {
                    const updated = [...prev];
                    const lastMsg = updated[updated.length - 1];
                    if (lastMsg.role === "assistant") {
                      lastMsg.animationSteps = [...receivedAnimationSteps];
                      if (receivedDiagram) {
                        lastMsg.diagram = receivedDiagram;
                      }
                    }
                    return updated;
                  });

                  // Auto-advance animation
                  setTimeout(() => {
                    setCurrentAnimationStep((prev) =>
                      Math.min(prev + 1, receivedAnimationSteps.length)
                    );
                  }, parsed.animation_step.duration);
                } else if (parsed.diagram) {
                  // Handle diagram
                  receivedDiagram = parsed.diagram;
                  setMessages((prev) => {
                    const updated = [...prev];
                    const lastMsg = updated[updated.length - 1];
                    if (lastMsg.role === "assistant") {
                      lastMsg.diagram = receivedDiagram!;
                    }
                    return updated;
                  });
                } else if (parsed.token) {
                  // Handle regular token streaming
                  assistantMessage += parsed.token;
                  setMessages((prev) => {
                    const updated = [...prev];
                    updated[updated.length - 1] = {
                      ...updated[updated.length - 1],
                      content: assistantMessage,
                    };
                    return updated;
                  });
                } else if (parsed.error) {
                  throw new Error(parsed.error);
                }
              } catch (e) {
                if (e instanceof Error && e.message !== "Unexpected end of JSON input") {
                  console.error("[Chat Stream] Parse error:", e);
                }
              }
            }
          }
        }
      } catch (error) {
        console.error("[Chat Stream] Error:", error);
        setMessages((prev) => {
          const updated = [...prev];
          const lastMsg = updated[updated.length - 1];
          const errorMessage = error instanceof Error ? error.message : MESSAGES.ERRORS.GENERIC;

          if (lastMsg && lastMsg.role === "assistant") {
            updated[updated.length - 1] = {
              ...lastMsg,
              content: lastMsg.content 
                ? `${lastMsg.content}\n\n[Error: ${errorMessage}]`
                : errorMessage,
            };
            return updated;
          }

          return [
            ...prev,
            {
              role: "assistant",
              content: errorMessage,
            },
          ];
        });
      } finally {
        setIsLoading(false);
        setIsAnimating(false);
      }
    },
    [messages, isLoading, activeConversation, createConversation, loadConversationHistory]
  );

  return {
    messages,
    isLoading,
    isAnimating,
    currentAnimationStep,
    sendMessage,
    setInput,
    input,
  };
}
