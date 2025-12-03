"""
Advanced Reasoning Patterns for CMatrix Agentic System.

This module provides state-of-the-art reasoning capabilities:
- ReWOO: Reasoning Without Observation for upfront planning
- Self-Reflection: Post-execution analysis and improvement
- Tree of Thoughts: Multi-strategy evaluation and selection

Design Principles:
- Modularity: Each pattern is independently usable
- Performance: Optimized for production workloads
- Observability: Comprehensive logging and metrics
- Reliability: Graceful degradation and error handling
"""

from .reflection import ReflectionResult, SelfReflection, get_self_reflection
from .rewoo import Plan, PlanStep, ReWOOPlanner, get_rewoo_planner
from .tree_of_thoughts import Strategy, StrategyEvaluation, TreeOfThoughts, get_tree_of_thoughts

__all__ = [
    # ReWOO
    "ReWOOPlanner",
    "Plan",
    "PlanStep",
    "get_rewoo_planner",
    # Self-Reflection
    "SelfReflection",
    "ReflectionResult",
    "get_self_reflection",
    # Tree of Thoughts
    "TreeOfThoughts",
    "Strategy",
    "StrategyEvaluation",
    "get_tree_of_thoughts",
]
