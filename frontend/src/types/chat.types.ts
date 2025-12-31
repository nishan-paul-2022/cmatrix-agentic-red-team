/**
 * Chat-related type definitions
 */

export type MessageRole = "user" | "assistant";

export interface AnimationStep {
  step: number;
  title: string;
  description: string;
  icon: string;
  bgColor: string;
  duration: number;
}

export interface NetworkDiagram {
  nodes: NetworkNode[];
  edges: NetworkEdge[];
}

export interface NetworkNode {
  id: string;
  label: string;
  group?: string;
  color?: string;
  shape?: string;
  [key: string]: any;
}

export interface NetworkEdge {
  from: string;
  to: string;
  label?: string;
  color?: string;
  [key: string]: any;
}

export interface ChatMessage {
  role: MessageRole;
  content: string;
  animationSteps?: AnimationStep[];
  diagram?: NetworkDiagram;
  timestamp?: Date;
  id?: string;
  pending_approval?: any; // Using any for now to avoid circular deps, or import PendingApproval type
  thread_id?: string;
}

export interface StreamChunk {
  token?: string;
  animation_step?: AnimationStep;
  diagram?: NetworkDiagram;
  error?: string;
}

export interface ChatRequest {
  message: string;
  history?: ChatMessage[];
}

export interface ChatResponse {
  message: string;
  animationSteps?: AnimationStep[];
  diagram?: NetworkDiagram;
}
