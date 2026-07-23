"""
GENESIS SELF IMPROVEMENT SYSTEM

Unified access layer for:
- Improvement Brain
- Performance Analysis
- Upgrade Generation
- Deployment
- Knowledge Graph
"""

from core.genesis.self_improvement.improvement_brain import (
    improvement_brain
)

# Backwards compatibility alias
self_improvement = improvement_brain

__all__ = [
    "self_improvement",
    "improvement_brain",
]
