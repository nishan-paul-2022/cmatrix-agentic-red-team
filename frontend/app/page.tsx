"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"

function TypewriterText({ text, speed = 100 }: { text: string; speed?: number }) {
  const [displayText, setDisplayText] = useState("")
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isComplete, setIsComplete] = useState(false)

  useEffect(() => {
    if (currentIndex < text.length) {
      const timer = setTimeout(() => {
        setDisplayText((prev) => prev + text[currentIndex])
        setCurrentIndex((prev) => prev + 1)
      }, speed)
      return () => clearTimeout(timer)
    } else {
      setIsComplete(true)
    }
  }, [currentIndex, text, speed])

  return <span>{displayText}{!isComplete && <span className="animate-pulse">|</span>}</span>
}
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Send, Loader2, Shield, Zap } from "lucide-react"
import { ChatMessage } from "@/components/chat-message"

export default function ChatPage() {
  const [messages, setMessages] = useState<Array<{ role: "user" | "assistant"; content: string }>>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [animationSteps, setAnimationSteps] = useState<Array<any>>([])
  const [currentAnimationStep, setCurrentAnimationStep] = useState(0)
  const [isAnimating, setIsAnimating] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = input.trim()
    setInput("")
    setMessages((prev) => [...prev, { role: "user", content: userMessage }])
    setIsLoading(true)
    setAnimationSteps([])
    setCurrentAnimationStep(0)
    setIsAnimating(false)

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMessage,
          history: messages.slice(-10), // Send last 10 messages for context
        }),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Unknown error" }))
        throw new Error(errorData.error || "Failed to fetch")
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()
      let assistantMessage = ""
      let receivedAnimationSteps: any[] = []

      // Add empty assistant message
      setMessages((prev) => [...prev, { role: "assistant", content: "" }])

      if (!reader) {
        throw new Error("No response body")
      }

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value, { stream: true })
        const lines = chunk.split("\n").filter(line => line.trim() !== "")

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6).trim()
            if (data === "[DONE]") continue

            try {
              const parsed = JSON.parse(data)
              if (parsed.animation_step) {
                // Handle animation step
                receivedAnimationSteps.push(parsed.animation_step)
                setAnimationSteps([...receivedAnimationSteps])
                setIsAnimating(true)

                // Auto-advance through animation steps
                setTimeout(() => {
                  setCurrentAnimationStep(prev => Math.min(prev + 1, receivedAnimationSteps.length))
                }, parsed.animation_step.duration)

              } else if (parsed.token) {
                // Handle regular token streaming
                assistantMessage += parsed.token
                // Keep animation visible and update the last message with accumulated content
                setMessages((prev) => {
                  const updated = [...prev]
                  updated[updated.length - 1] = {
                    role: "assistant",
                    content: assistantMessage
                  }
                  return updated
                })
              } else if (parsed.error) {
                console.error("[v0] Stream error:", parsed.error)
                throw new Error(parsed.error)
              }
            } catch (e) {
              if (e instanceof Error && e.message !== "Unexpected end of JSON input") {
                console.error("[v0] Parse error:", e)
              }
            }
          }
        }
      }
    } catch (error) {
      console.error("[v0] Error:", error)
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : "Unknown error"}. Please try again.`,
        },
      ])
    } finally {
      setIsLoading(false)
      setIsAnimating(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-background">
      <div className="matrix-rain"></div>
      {/* Header */}
      <header className="border-b border-border bg-card cyber-border scan-line">
        <div className="container flex items-center justify-between h-14 px-4 mx-auto">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-secondary cyber-border">
              <Shield className="w-5 h-5 text-secondary-foreground" />
            </div>
            <div>
              <h1 className="text-lg font-semibold terminal-text">CMatrix</h1>
              <div className="text-xs text-muted-foreground">Neural Interface Active</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-chart-1 rounded-full animate-pulse"></div>
            <div className="text-xs text-muted-foreground terminal-text">AGENT ONLINE</div>
          </div>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto">
        <div className="container max-w-4xl px-4 py-8 mx-auto">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full gap-8 py-12">
              <div className="flex items-center justify-center gap-6">
                <div className="flex items-center justify-center w-20 h-20 rounded-2xl bg-secondary cyber-border">
                  <Zap className="w-10 h-10 text-secondary-foreground" />
                </div>
                <div className="text-left">
                  <h2 className="text-4xl font-bold text-balance terminal-text glow-primary">
                    <TypewriterText text="CMatrix" speed={150} />
                  </h2>
                  <div className="text-sm text-muted-foreground terminal-text mt-2">
                    Neural Interface
                  </div>
                </div>
              </div>
              <div className="text-center space-y-4">
                <p className="text-muted-foreground text-pretty max-w-md terminal-text">
                  Agent capabilities: security scanning, system monitoring, log analysis, configuration deployment.
                </p>
                <div className="text-xs text-muted-foreground terminal-text">
                  [SYSTEM STATUS: OPERATIONAL] [AGENT: DEEPHAT-V1-7B]
                </div>
              </div>
              <div className="grid gap-3 mt-4 sm:grid-cols-2">
                <button
                  onClick={() => setInput("Scan my web application for vulnerabilities")}
                  className="px-4 py-3 text-sm text-left transition-colors border rounded-lg border-border hover:bg-accent hover:text-accent-foreground cyber-border"
                >
                  <div className="font-medium terminal-text">Security Scan</div>
                  <div className="text-xs text-muted-foreground">Analyze system vulnerabilities</div>
                </button>
                <button
                  onClick={() => setInput("Check the status of critical services")}
                  className="px-4 py-3 text-sm text-left transition-colors border rounded-lg border-border hover:bg-accent hover:text-accent-foreground cyber-border"
                >
                  <div className="font-medium terminal-text">System Status</div>
                  <div className="text-xs text-muted-foreground">Monitor infrastructure health</div>
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((message, index) => (
                <ChatMessage
                  key={index}
                  role={message.role}
                  content={message.content}
                  animationSteps={message.role === "assistant" ? animationSteps : []}
                  currentAnimationStep={currentAnimationStep}
                  isAnimating={isAnimating && index === messages.length - 1 && message.role === "assistant"}
                />
              ))}
              {isLoading && messages[messages.length - 1]?.role === "user" && (
                <ChatMessage role="assistant" content="" isLoading />
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </div>

      {/* Input */}
      <div className="border-t border-border bg-card cyber-border">
        <div className="container max-w-4xl px-4 py-4 mx-auto">
          <form onSubmit={handleSubmit} className="relative">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Enter command or query..."
              className="pr-12 resize-none min-h-[60px] max-h-[200px] cyber-border bg-black text-white placeholder:text-gray-400"
              disabled={isLoading}
            />
            <Button
              type="submit"
              size="icon"
              disabled={!input.trim() || isLoading}
              className="absolute bottom-2 right-2 rounded-lg bg-black text-white hover:bg-gray-800"
            >
              {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
            </Button>
          </form>
          <p className="mt-2 text-xs text-center text-muted-foreground terminal-text">
            [SECURITY NOTICE] Neural responses may contain classified information. Handle with care.
          </p>
        </div>
      </div>
    </div>
  )
}
