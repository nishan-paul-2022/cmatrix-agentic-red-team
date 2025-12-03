"use client";

import { cn } from "@/lib/utils";
import { User, Loader2, Activity, CheckCircle, VenetianMask } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { AnimatedDiagram } from "../diagram/animated-diagram";
import { MESSAGES } from "@/constants/messages";
import type { ChatMessage as ChatMessageType } from "@/types/chat.types";
import { ApprovalMessage } from "./approval-message";

interface ChatMessageProps {
  message: ChatMessageType;
  isLoading?: boolean;
  currentAnimationStep?: number;
  isAnimating?: boolean;
  onRefresh?: () => void;
}

/**
 * Chat message component
 * Displays user or assistant messages with optional animations and diagrams
 */
export function ChatMessage({
  message,
  isLoading = false,
  currentAnimationStep = 0,
  isAnimating = false,
  onRefresh,
}: ChatMessageProps) {
  const isUser = message.role === "user";
  const { content, animationSteps = [], diagram, pending_approval, thread_id } = message;

  return (
    <div className={cn("flex gap-4 group", isUser ? "justify-end" : "justify-start")}>
      {!isUser && (
        <div className="flex items-start flex-shrink-0">
          <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-secondary cyber-border">
            <VenetianMask className="w-5 h-5 text-secondary-foreground" />
          </div>
        </div>
      )}

      <div className={cn("flex flex-col gap-2 max-w-[80%] sm:max-w-[70%]", isUser && "items-end")}>
        {/* Render Approval Card if pending approval exists */}
        {pending_approval && thread_id && (
          <div className="mb-4 w-full">
            <ApprovalMessage
              threadId={thread_id}
              pendingApproval={pending_approval}
              onActionComplete={onRefresh}
            />
          </div>
        )}

        <div
          className={cn(
            "rounded-lg px-4 py-3 text-sm leading-relaxed cyber-border",
            isUser ? "bg-black text-white" : "bg-muted text-foreground terminal-text",
            !isUser && (isLoading || isAnimating) && "scan-line"
          )}
        >
          {/* ... existing content rendering ... */}
          {animationSteps.length > 0 ? (
            <div className="space-y-4">
              {/* ... existing animation steps ... */}
              {/* Animated Diagram */}
              {diagram && (
                <div className="mb-4">
                  <AnimatedDiagram
                    nodes={diagram.nodes}
                    edges={diagram.edges}
                    currentStep={currentAnimationStep}
                    isAnimating={isAnimating}
                    className="w-full"
                  />
                </div>
              )}

              {/* Animation Steps */}
              <div className="space-y-2">
                {animationSteps.map((step, index) => {
                  const isActive = index === currentAnimationStep - 1 && isAnimating;
                  const isCompleted = index < currentAnimationStep - 1 || (!isAnimating && content);

                  return (
                    <div
                      key={step.step}
                      className={cn(
                        "flex items-start gap-3 p-2 rounded transition-all duration-300",
                        isActive && "bg-blue-500/10 border border-blue-500/20",
                        isCompleted && "bg-sky-500/10 border border-sky-500/20"
                      )}
                      style={{ backgroundColor: step.bgColor + "30" }}
                    >
                      <div className="flex-shrink-0 mt-0.5">
                        {isCompleted ? (
                          <CheckCircle className="w-4 h-4 text-sky-400" />
                        ) : isActive ? (
                          <Activity className="w-4 h-4 animate-spin text-blue-400" />
                        ) : (
                          <div className="w-4 h-4 rounded-full border-2 border-muted-foreground/30" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-xs font-medium terminal-text">
                            {step.icon} {step.title}
                          </span>
                          {isActive && (
                            <div className="flex gap-1">
                              <div
                                className="w-1 h-1 bg-blue-400 rounded-full animate-bounce"
                                style={{ animationDelay: "0ms" }}
                              />
                              <div
                                className="w-1 h-1 bg-blue-400 rounded-full animate-bounce"
                                style={{ animationDelay: "150ms" }}
                              />
                              <div
                                className="w-1 h-1 bg-blue-400 rounded-full animate-bounce"
                                style={{ animationDelay: "300ms" }}
                              />
                            </div>
                          )}
                        </div>
                        <p className="text-xs text-muted-foreground terminal-text">
                          {step.description}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>

              {content && (
                <div className="mt-4 pt-4 border-t border-border">
                  <div className="prose prose-sm dark:prose-invert max-w-none">
                    <ReactMarkdown>{content}</ReactMarkdown>
                  </div>
                </div>
              )}
            </div>
          ) : isLoading ? (
            <div className="flex items-center gap-2 terminal-text">
              <Loader2 className="w-4 h-4 animate-spin text-sky-400" />
              <span className="text-muted-foreground">{MESSAGES.SYSTEM.PROCESSING}</span>
            </div>
          ) : (
            <div className="prose prose-sm dark:prose-invert max-w-none">
              {isUser ? (
                <span>{content}</span>
              ) : (
                <ReactMarkdown>{content || "\u00A0"}</ReactMarkdown>
              )}
            </div>
          )}
        </div>
      </div>

      {isUser && (
        <div className="flex items-start flex-shrink-0">
          <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-secondary cyber-border">
            <User className="w-5 h-5 text-secondary-foreground" />
          </div>
        </div>
      )}
    </div>
  );
}
