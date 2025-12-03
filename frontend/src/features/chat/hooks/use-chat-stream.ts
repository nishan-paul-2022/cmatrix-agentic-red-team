"use client";

import { useState, useCallback, useEffect } from "react";
import type { ChatMessage, StreamChunk, AnimationStep, NetworkDiagram } from "@/types/chat.types";
import type { ConversationWithHistory } from "@/types/conversation.types";
import { apiConfig } from "@/config/api.config";
import { MESSAGES } from "@/constants/messages";
import { useConversations } from "@/contexts/conversation-context";
import { useAuth } from "@/contexts/auth-context";

interface UseChatStreamReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  isAnimating: boolean;
  currentAnimationStep: number;
  sendMessage: (message: string) => Promise<void>;
  setInput: (input: string) => void;
  input: string;
  refreshMessages: () => Promise<void>;
}

/**
 * Hook for handling chat streaming functionality
 */
export function useChatStream(): UseChatStreamReturn {
  const { activeConversation, loadConversationHistory, createConversation, loadConversations } =
    useConversations();
  const { user } = useAuth();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false);
  const [currentAnimationStep, setCurrentAnimationStep] = useState(0);

  // Load conversation history when active conversation changes
  useEffect(() => {
    const loadMessages = async () => {
      if (activeConversation) {
        // Retry logic for newly created conversations (race condition handling)
        let retries = 3;
        let delay = 100; // Start with 100ms delay

        while (retries > 0) {
          try {
            const conversationData = await loadConversationHistory(activeConversation.id);
            const chatMessages: ChatMessage[] = conversationData.history.map((h) => ({
              role: h.role as "user" | "assistant",
              content: h.content,
            }));
            setMessages(chatMessages);
            break; // Success, exit retry loop
          } catch (error) {
            retries--;

            // If it's a 404 and we have retries left, wait and retry
            if (error instanceof Error && error.message.includes("not found") && retries > 0) {
              console.warn(
                `Conversation ${activeConversation.id} not found, retrying in ${delay}ms... (${retries} retries left)`
              );
              await new Promise((resolve) => setTimeout(resolve, delay));
              delay *= 2; // Exponential backoff
            } else {
              // For other errors or no retries left, log and clear messages
              console.error("Failed to load conversation history:", error);
              setMessages([]);
              break;
            }
          }
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
          console.error("Failed to create conversation:", error);
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
        const token = localStorage.getItem("auth_token");
        if (!token) {
          throw new Error("Not authenticated. Please log in.");
        }

        // 1. Create Background Job
        const createResponse = await fetch(
          `${apiConfig.baseUrl}${apiConfig.endpoints.jobs.create}`,
          {
            method: "POST",
            headers: {
              ...apiConfig.headers,
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              message: userMessage,
              conversation_id: conversationId,
              history: messages.slice(-10), // Last 10 messages for context
            }),
          }
        );

        if (!createResponse.ok) {
          const errorData = await createResponse.json().catch(() => ({}));
          let errorMessage: string = MESSAGES.ERRORS.FETCH_FAILED;

          if (errorData.detail) {
            if (typeof errorData.detail === "string") {
              errorMessage = errorData.detail;
            } else if (Array.isArray(errorData.detail)) {
              // Handle FastAPI validation errors
              errorMessage = errorData.detail
                .map((err: any) => `${err.loc?.join(".")} ${err.msg}`)
                .join(", ");
            } else if (typeof errorData.detail === "object") {
              errorMessage = JSON.stringify(errorData.detail);
            }
          }

          throw new Error(errorMessage);
        }

        const { job_id } = await createResponse.json();

        // Add empty assistant message with loading state
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: "Processing request...", animationSteps: [] },
        ]);

        // 2. Poll for Completion
        let jobResult: any = null;
        let pollCount = 0;
        const MAX_POLLS = 600; // 20 minutes max (2s interval)

        while (pollCount < MAX_POLLS) {
          await new Promise((resolve) => setTimeout(resolve, 2000)); // Poll every 2s
          pollCount++;

          const statusResponse = await fetch(
            `${apiConfig.baseUrl}${apiConfig.endpoints.jobs.get(job_id)}`,
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );

          // Handle 410 - job expired/cleared from Redis (graceful degradation)
          if (statusResponse.status === 410) {
            console.warn(`Job ${job_id} has expired or was cleared from cache`);
            // Break polling and show a friendly message
            setMessages((prev) => {
              const updated = [...prev];
              updated[updated.length - 1] = {
                role: "assistant",
                content:
                  "Your request took too long and the result has expired. Please try sending your message again.",
              };
              return updated;
            });
            return; // Exit gracefully without throwing
          }

          // Handle 404 - job not found (should rarely happen with new logic)
          if (statusResponse.status === 404) {
            console.warn(`Job ${job_id} not found`);
            setMessages((prev) => {
              const updated = [...prev];
              updated[updated.length - 1] = {
                role: "assistant",
                content: "Unable to find your request. Please try sending your message again.",
              };
              return updated;
            });
            return; // Exit gracefully without throwing
          }

          // Retry on other errors (network issues, temporary 500s, etc.)
          if (!statusResponse.ok) continue;

          const statusData = await statusResponse.json();

          if (statusData.status === "success") {
            jobResult = statusData.result;
            break;
          } else if (statusData.status === "failed") {
            throw new Error(statusData.error || "Job failed during execution");
          } else if (statusData.status === "cancelled") {
            throw new Error("Job was cancelled");
          }

          // Optional: Update loading message with duration
          if (pollCount % 5 === 0) {
            // Every 10s
            setMessages((prev) => {
              const updated = [...prev];
              const lastMsg = updated[updated.length - 1];
              if (lastMsg.role === "assistant" && lastMsg.content.startsWith("Processing")) {
                updated[updated.length - 1] = {
                  ...lastMsg,
                  content: `Processing request... (${Math.floor(pollCount * 2)}s)`,
                };
              }
              return updated;
            });
          }
        }

        if (!jobResult) {
          throw new Error("Job timed out or returned no result");
        }

        // 3. Playback Result (Simulate Streaming)

        // Clear the "Processing..." message
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = { role: "assistant", content: "", animationSteps: [] };
          return updated;
        });

        let assistantMessage = "";
        let receivedAnimationSteps: AnimationStep[] = [];
        let receivedDiagram: NetworkDiagram | null = null;

        // Check for Pending Approval
        if (typeof jobResult === "object" && jobResult.pending_approval) {
          const threadId = `user_${user?.id}_conv_${conversationId}`;
          // Extract content from messages list if available
          let content = "Approval Required";
          if (
            jobResult.messages &&
            Array.isArray(jobResult.messages) &&
            jobResult.messages.length > 0
          ) {
            content = jobResult.messages[0].content || content;
          }

          setMessages((prev) => {
            const updated = [...prev];
            updated[updated.length - 1] = {
              role: "assistant",
              content: content,
              pending_approval: jobResult.pending_approval,
              thread_id: threadId,
              animationSteps: [],
            };
            return updated;
          });
          setIsLoading(false);
          return;
        }

        // Check if result is complex object or string
        if (typeof jobResult === "object" && jobResult.animation_steps) {
          // Complex result with animations
          const { animation_steps, diagram, final_answer } = jobResult;

          // Handle Diagram
          if (diagram) {
            receivedDiagram = diagram;
            setMessages((prev) => {
              const updated = [...prev];
              const lastMsg = updated[updated.length - 1];
              if (lastMsg.role === "assistant") {
                lastMsg.diagram = receivedDiagram!;
              }
              return updated;
            });
          }

          // Handle Animations
          if (animation_steps && animation_steps.length > 0) {
            setIsAnimating(true);
            setIsLoading(false); // Stop loading spinner, start animation

            for (const step of animation_steps) {
              receivedAnimationSteps.push(step);

              // Update message with new step
              setMessages((prev) => {
                const updated = [...prev];
                const lastMsg = updated[updated.length - 1];
                if (lastMsg.role === "assistant") {
                  lastMsg.animationSteps = [...receivedAnimationSteps];
                }
                return updated;
              });

              // Advance step counter
              setCurrentAnimationStep(receivedAnimationSteps.length);

              // Wait for duration
              await new Promise((resolve) => setTimeout(resolve, step.duration || 1500));
            }
          }

          // Handle Final Text
          const words = (final_answer || "").split(" ");
          for (let i = 0; i < words.length; i++) {
            assistantMessage += words[i] + " ";
            setMessages((prev) => {
              const updated = [...prev];
              updated[updated.length - 1] = {
                ...updated[updated.length - 1],
                content: assistantMessage,
              };
              return updated;
            });
            await new Promise((resolve) => setTimeout(resolve, 30)); // Fast typing
          }
        } else {
          // Simple string result
          const text = typeof jobResult === "string" ? jobResult : JSON.stringify(jobResult);
          const words = text.split(" ");

          for (let i = 0; i < words.length; i++) {
            assistantMessage += words[i] + " ";
            setMessages((prev) => {
              const updated = [...prev];
              updated[updated.length - 1] = {
                ...updated[updated.length - 1],
                content: assistantMessage,
              };
              return updated;
            });
            await new Promise((resolve) => setTimeout(resolve, 30));
          }
        }

        // Refresh conversations list to update title if generated
        loadConversations();
      } catch (error) {
        console.error("[Chat Job] Error:", error);
        setMessages((prev) => {
          const updated = [...prev];
          const lastMsg = updated[updated.length - 1];
          const errorMessage = error instanceof Error ? error.message : MESSAGES.ERRORS.GENERIC;

          if (lastMsg && lastMsg.role === "assistant") {
            updated[updated.length - 1] = {
              ...lastMsg,
              content:
                lastMsg.content && !lastMsg.content.startsWith("Processing")
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

  const refreshMessages = useCallback(async () => {
    if (activeConversation) {
      try {
        const conversationData = await loadConversationHistory(activeConversation.id);
        const chatMessages: ChatMessage[] = conversationData.history.map((h) => ({
          role: h.role as "user" | "assistant",
          content: h.content,
        }));
        setMessages(chatMessages);
      } catch (error) {
        console.error("Failed to refresh conversation history:", error);
      }
    }
  }, [activeConversation, loadConversationHistory]);

  const startPolling = useCallback(async () => {
    // Optimistic update: Remove pending_approval immediately
    setMessages((prev) => {
      const updated = [...prev];
      const lastMsgIndex = updated.findIndex((m) => m.pending_approval);
      if (lastMsgIndex !== -1) {
        updated[lastMsgIndex] = {
          ...updated[lastMsgIndex],
          pending_approval: undefined,
          content: "Processing approval...",
        };
      }
      return updated;
    });

    const POLL_DURATION = 30000; // 30 seconds
    const POLL_INTERVAL = 2000; // 2 seconds
    const startTime = Date.now();

    const poll = async () => {
      if (Date.now() - startTime > POLL_DURATION) return;
      await refreshMessages();
      setTimeout(poll, POLL_INTERVAL);
    };

    poll();
  }, [refreshMessages]);

  return {
    messages,
    isLoading,
    isAnimating,
    currentAnimationStep,
    sendMessage,
    setInput,
    input,
    refreshMessages: startPolling, // Expose startPolling as refreshMessages
  };
}
