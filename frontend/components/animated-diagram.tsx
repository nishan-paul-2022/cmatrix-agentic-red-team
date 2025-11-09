"use client"

import React, { useState, useEffect } from "react"
import { cn } from "@/lib/utils"

interface DiagramNode {
  id: string
  label: string
  x: number
  y: number
  type: 'user' | 'ai' | 'tool' | 'result'
  active?: boolean
  completed?: boolean
}

interface DiagramEdge {
  from: string
  to: string
  active?: boolean
  completed?: boolean
}

interface AnimatedDiagramProps {
  nodes: DiagramNode[]
  edges: DiagramEdge[]
  currentStep?: number
  isAnimating?: boolean
  className?: string
}

export function AnimatedDiagram({ nodes, edges, currentStep = 0, isAnimating = false, className }: AnimatedDiagramProps) {
  const [animatedNodes, setAnimatedNodes] = useState(nodes)
  const [animatedEdges, setAnimatedEdges] = useState(edges)

  useEffect(() => {
    if (!isAnimating) return

    // Update node and edge states based on current step
    const updatedNodes = nodes.map((node, index) => ({
      ...node,
      active: index === currentStep,
      completed: index < currentStep
    }))

    const updatedEdges = edges.map((edge, index) => ({
      ...edge,
      active: index === currentStep - 1,
      completed: index < currentStep - 1
    }))

    setAnimatedNodes(updatedNodes)
    setAnimatedEdges(updatedEdges)
  }, [currentStep, isAnimating, nodes, edges])

  const getNodeColor = (node: DiagramNode) => {
    if (node.completed) return "bg-green-500 border-green-400"
    if (node.active) return "bg-blue-500 border-blue-400 animate-pulse"
    return "bg-muted border-muted-foreground"
  }

  const getNodeIcon = (type: string) => {
    switch (type) {
      case 'user': return '👤'
      case 'ai': return '🤖'
      case 'tool': return '🔧'
      case 'result': return '📊'
      default: return '●'
    }
  }

  const getEdgeColor = (edge: DiagramEdge) => {
    if (edge.completed) return "stroke-green-400"
    if (edge.active) return "stroke-blue-400 animate-pulse"
    return "stroke-muted-foreground"
  }

  return (
    <div className={cn("relative w-full h-64 bg-card rounded-lg border border-border p-4 overflow-hidden", className)}>
      {/* Background grid */}
      <div className="absolute inset-0 opacity-10">
        <svg width="100%" height="100%" className="text-muted-foreground">
          <defs>
            <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
              <path d="M 20 0 L 0 0 0 20" fill="none" stroke="currentColor" strokeWidth="0.5"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      {/* SVG Diagram */}
      <svg width="100%" height="100%" className="absolute inset-0">
        {/* Edges */}
        {animatedEdges.map((edge, index) => {
          const fromNode = animatedNodes.find(n => n.id === edge.from)
          const toNode = animatedNodes.find(n => n.id === edge.to)
          if (!fromNode || !toNode) return null

          const x1 = fromNode.x + 40 // center of node
          const y1 = fromNode.y + 40
          const x2 = toNode.x + 40
          const y2 = toNode.y + 40

          return (
            <g key={`edge-${index}`}>
              {/* Arrow line */}
              <line
                x1={x1}
                y1={y1}
                x2={x2}
                y2={y2}
                className={cn("stroke-2 transition-all duration-500", getEdgeColor(edge))}
                markerEnd="url(#arrowhead)"
              />
              {/* Animated flow indicator */}
              {edge.active && (
                <circle
                  r="3"
                  fill="#3b82f6"
                  className="animate-ping"
                >
                  <animateMotion
                    dur="1.5s"
                    repeatCount="indefinite"
                    path={`M${x1},${y1} L${x2},${y2}`}
                  />
                </circle>
              )}
            </g>
          )
        })}

        {/* Arrow marker definition */}
        <defs>
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="7"
            refX="9"
            refY="3.5"
            orient="auto"
          >
            <polygon
              points="0 0, 10 3.5, 0 7"
              fill="currentColor"
            />
          </marker>
        </defs>

        {/* Nodes */}
        {animatedNodes.map((node) => (
          <g key={node.id} transform={`translate(${node.x}, ${node.y})`}>
            {/* Node circle */}
            <circle
              cx="40"
              cy="40"
              r="35"
              className={cn(
                "stroke-2 fill-current transition-all duration-500",
                getNodeColor(node)
              )}
            />

            {/* Node icon */}
            <text
              x="40"
              y="45"
              textAnchor="middle"
              className="text-lg font-bold fill-white"
            >
              {getNodeIcon(node.type)}
            </text>

            {/* Node label */}
            <text
              x="40"
              y="75"
              textAnchor="middle"
              className="text-xs font-medium fill-current text-muted-foreground max-w-20"
            >
              {node.label}
            </text>

            {/* Active glow effect */}
            {node.active && (
              <circle
                cx="40"
                cy="40"
                r="45"
                className="stroke-blue-400 stroke-2 fill-none animate-ping opacity-50"
              />
            )}
          </g>
        ))}
      </svg>

      {/* Status indicator */}
      <div className="absolute bottom-2 left-2 text-xs text-muted-foreground terminal-text">
        {isAnimating ? (
          <span className="flex items-center gap-1">
            <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse"></div>
            PROCESSING STEP {currentStep + 1}
          </span>
        ) : (
          <span>WORKFLOW COMPLETE</span>
        )}
      </div>
    </div>
  )
}