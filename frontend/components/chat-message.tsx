import { cn } from "@/lib/utils"
import { User, Shield, Loader2, Activity, CheckCircle, AlertTriangle } from "lucide-react"
import ReactMarkdown from "react-markdown"

interface ChatMessageProps {
  role: "user" | "assistant"
  content: string
  isLoading?: boolean
  animationSteps?: any[]
  currentAnimationStep?: number
  isAnimating?: boolean
}

export function ChatMessage({ role, content, isLoading, animationSteps = [], currentAnimationStep = 0, isAnimating = false }: ChatMessageProps) {
  const isUser = role === "user"

  return (
    <div className={cn("flex gap-4 group", isUser ? "justify-end" : "justify-start")}>
      {!isUser && (
        <div className="flex items-start flex-shrink-0">
          <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-secondary cyber-border">
            <Shield className="w-5 h-5 text-secondary-foreground" />
          </div>
        </div>
      )}

      <div className={cn("flex flex-col gap-2 max-w-[80%] sm:max-w-[70%]", isUser && "items-end")}>
        {!isUser && (
          <div className="text-xs text-muted-foreground terminal-text flex items-center gap-2">
            <div className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse"></div>
            DEEPHAT AGENT
          </div>
        )}
        <div
          className={cn(
            "rounded-lg px-4 py-3 text-sm leading-relaxed cyber-border",
            isUser
              ? "bg-black text-white"
              : "bg-muted text-foreground terminal-text",
            !isUser && (isLoading || isAnimating) && "scan-line"
          )}
        >
          {(isAnimating && animationSteps.length > 0) || (content && animationSteps.length > 0) ? (
            <div className="space-y-3">
              <div className="flex items-center gap-2 terminal-text mb-3">
                <Activity className="w-4 h-4 animate-pulse text-blue-400" />
                <span className="text-muted-foreground">[AGENT WORKING...]</span>
              </div>
              <div className="space-y-2">
                {animationSteps.map((step, index) => {
                  const isActive = index === currentAnimationStep - 1 && isAnimating
                  const isCompleted = index < currentAnimationStep - 1 || (!isAnimating && content)

                  return (
                    <div
                      key={step.step}
                      className={cn(
                        "flex items-start gap-3 p-2 rounded transition-all duration-300",
                        isActive && "bg-blue-500/10 border border-blue-500/20",
                        isCompleted && "bg-green-500/10 border border-green-500/20"
                      )}
                    >
                      <div className="flex-shrink-0 mt-0.5">
                        {isCompleted ? (
                          <CheckCircle className="w-4 h-4 text-green-400" />
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
                              <div className="w-1 h-1 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                              <div className="w-1 h-1 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                              <div className="w-1 h-1 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                            </div>
                          )}
                        </div>
                        <p className="text-xs text-muted-foreground terminal-text">
                          {step.description}
                        </p>
                      </div>
                    </div>
                  )
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
              <Loader2 className="w-4 h-4 animate-spin text-green-400" />
              <span className="text-muted-foreground">[PROCESSING QUERY...]</span>
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
        {isUser && (
          <div className="text-xs text-muted-foreground terminal-text flex items-center gap-2">
            <div className="w-1.5 h-1.5 bg-blue-400 rounded-full"></div>
            HUMAN OPERATOR
          </div>
        )}
      </div>

      {isUser && (
        <div className="flex items-start flex-shrink-0">
          <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-secondary cyber-border">
            <User className="w-5 h-5 text-secondary-foreground" />
          </div>
        </div>
      )}
    </div>
  )
}
