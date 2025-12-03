"use client";

import React, { useEffect, useRef } from "react";
import { DataSet, DataView } from "vis-data/peer";
import { Network } from "vis-network/peer";
import type { Node, Edge, Options } from "vis-network/peer";
import "vis-network/styles/vis-network.css";
import { cn } from "@/lib/utils";
import "./vis-styles.css";

interface DiagramNode {
  id: string;
  label: string;
  type?: "user" | "ai" | "tool" | "result";
  active?: boolean;
  completed?: boolean;
  [key: string]: any; // Allow additional properties from backend
}

interface DiagramEdge {
  from: string;
  to: string;
  active?: boolean;
  completed?: boolean;
}

interface AnimatedDiagramProps {
  nodes: DiagramNode[];
  edges: DiagramEdge[];
  currentStep?: number;
  isAnimating?: boolean;
  className?: string;
}

export function AnimatedDiagram({
  nodes: initialNodes,
  edges: initialEdges,
  currentStep = 0,
  isAnimating = false,
  className,
}: AnimatedDiagramProps) {
  const visJsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!visJsRef.current) return;

    const getIcon = (type?: string) => {
      switch (type) {
        case "user":
          return "👤";
        case "ai":
          return "🤖";
        case "tool":
          return "🔧";
        case "result":
          return "📊";
        default:
          return "●";
      }
    };

    const nodes = new DataSet<Node>(
      initialNodes.map((node, index) => {
        const isActive = index === currentStep;
        const isCompleted = index < currentStep;

        return {
          id: node.id,
          label: `${getIcon(node.type || undefined)}\n\n${node.label}`,
          shape: "box",
          font: {
            color: isCompleted ? "#94a3b8" : "#ffffff",
            size: 12,
            multi: true,
          },
          borderWidth: isActive ? 2 : 1,
          color: {
            border: isActive ? "#ffffff" : isCompleted ? "#475569" : "#334155",
            background: "#2d3748",
            hover: {
              background: "#475569",
            },
          },
          margin: {
            top: 10,
            right: 10,
            bottom: 10,
            left: 10,
          },
          shapeProperties: {
            borderRadius: 6,
          },
          shadow: isActive
            ? { enabled: true, color: "rgba(255,255,255,0.5)", size: 20 }
            : { enabled: false },
        };
      })
    );

    const edges = new DataSet<Edge>(
      initialEdges.map((edge, index) => {
        const isActive = index === currentStep - 1;
        const isCompleted = index < currentStep - 1;
        return {
          from: edge.from,
          to: edge.to,
          arrows: {
            to: {
              enabled: true,
              scaleFactor: 0.5,
            },
          },
          color: {
            color: isActive ? "#ffffff" : isCompleted ? "#475569" : "#334155",
            highlight: "#ffffff",
          },
          width: isActive ? 2 : 1,
          smooth: {
            enabled: true,
            type: "curvedCW",
            roundness: 0.2,
          },
        };
      })
    );

    const data = {
      nodes: nodes as DataSet<Node, "id"> | DataView<Node, "id">,
      edges: edges as DataSet<Edge, "id"> | DataView<Edge, "id">,
    };

    const options: Options = {
      autoResize: true,
      physics: {
        enabled: true,
        solver: "forceAtlas2Based",
        forceAtlas2Based: {
          gravitationalConstant: -50,
          centralGravity: 0.01,
          springLength: 100,
          springConstant: 0.08,
          damping: 0.4,
          avoidOverlap: 0.5,
        },
        stabilization: {
          iterations: 150,
        },
      },
      interaction: {
        dragNodes: true,
        dragView: true,
        zoomView: true,
        hover: true,
      },
      layout: {
        hierarchical: false,
      },
    };

    const network = new Network(visJsRef.current, data, options);

    // Add a background grid
    const canvas = visJsRef.current.getElementsByTagName("canvas")[0];
    const ctx = canvas.getContext("2d");

    network.on("beforeDrawing", (ctx) => {
      // Get the canvas dimensions
      const canvasWidth = canvas.width;
      const canvasHeight = canvas.height;

      // Clear the entire canvas
      ctx.clearRect(0, 0, canvasWidth, canvasHeight);

      // Save the current transformation matrix
      ctx.save();

      // Reset transformation to draw grid in canvas coordinates
      ctx.setTransform(1, 0, 0, 1, 0, 0);

      // Draw grid covering the entire canvas
      const gridSize = 20;
      ctx.strokeStyle = "rgba(255, 255, 255, 0.1)";
      ctx.lineWidth = 0.5;

      for (let x = 0; x <= canvasWidth; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvasHeight);
        ctx.stroke();
      }

      for (let y = 0; y <= canvasHeight; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvasWidth, y);
        ctx.stroke();
      }

      // Restore the transformation matrix
      ctx.restore();
    });

    network.on("stabilizationIterationsDone", () => {
      // Disable physics after stabilization to prevent circulating movement
      network.setOptions({ physics: { enabled: false } });
    });

    let animationFrameId: number;
    let timeoutId: NodeJS.Timeout;
    let isMounted = true;

    if (isAnimating) {
      // Animate data flow from start node to end node sequentially
      const animateFlow = (edgeIndex: number) => {
        if (!isMounted) return;

        if (edgeIndex >= initialEdges.length) {
          // Animation complete, reset to start if needed
          return;
        }

        const activeEdge = initialEdges[edgeIndex];
        const fromNodeId = activeEdge.from;
        const toNodeId = activeEdge.to;

        const particleId = `flow-particle-${edgeIndex}`;
        if (!nodes.get(particleId)) {
          try {
            nodes.add({
              id: particleId,
              shape: "dot",
              size: 4,
              color: "#60a5fa",
              physics: false,
            });
          } catch (e) {
            console.warn("Failed to add particle node:", e);
            return;
          }
        }

        // Check if network is still valid and has the method
        if (!network || !network.getPositions) {
          return;
        }

        try {
          const positions = network.getPositions([fromNodeId, toNodeId]);
          const fromNode = positions[fromNodeId];
          const toNode = positions[toNodeId];

          if (fromNode && toNode) {
            const distance = Math.sqrt(
              Math.pow(toNode.x - fromNode.x, 2) + Math.pow(toNode.y - fromNode.y, 2)
            );
            const duration = distance / 80; // Adjust speed for smoother flow
            const startTime = Date.now();

            const step = () => {
              if (!isMounted) return;

              const now = Date.now();
              const time = (now - startTime) / 1000;
              const progress = Math.min(time / duration, 1);

              const x = fromNode.x + (toNode.x - fromNode.x) * progress;
              const y = fromNode.y + (toNode.y - fromNode.y) * progress;

              try {
                nodes.update({ id: particleId, x, y });
              } catch (e) {
                // Ignore update errors if node is gone
              }

              if (progress < 1) {
                animationFrameId = requestAnimationFrame(step);
              } else {
                // Remove particle and move to next edge
                try {
                  if (nodes.get(particleId)) {
                    nodes.remove(particleId);
                  }
                } catch (e) {
                  // Ignore removal errors
                }
                // Continue to next edge after a brief delay
                timeoutId = setTimeout(() => animateFlow(edgeIndex + 1), 200);
              }
            };
            step();
          } else {
            // If nodes not found, continue to next edge
            timeoutId = setTimeout(() => animateFlow(edgeIndex + 1), 200);
          }
        } catch (e) {
          console.error("Error in animateFlow:", e);
        }
      };

      // Start animation from first edge
      animateFlow(0);
    }

    return () => {
      isMounted = false;
      cancelAnimationFrame(animationFrameId);
      clearTimeout(timeoutId);

      try {
        if (nodes.get("flow-particle")) {
          nodes.remove("flow-particle");
        }
      } catch (e) {
        // Ignore
      }

      if (network) {
        network.destroy();
      }
    };
  }, [initialNodes, initialEdges, currentStep, isAnimating]);

  return (
    <div
      className={cn(
        "relative w-full h-64 bg-card rounded-lg border border-border overflow-hidden",
        className
      )}
    >
      <div ref={visJsRef} className="w-full h-full" key={initialNodes.length} />
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
  );
}
