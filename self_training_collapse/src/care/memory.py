from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TypedDict


class MemoryEntry(TypedDict):
    """A single entry in the Capability-Effect Memory."""
    strategy: str
    context: dict[str, Any]
    capability_delta: dict[str, float]
    boundary: str
    confidence: float


@dataclass
class CapabilityEffectMemory:
    """
    Store and retrieve capability-effect observations for self-training campaigns.
    
    This module tracks how specific intervention strategies affect different
    capabilities across various contexts, establishing boundaries of
    effectiveness.
    """

    entries: list[MemoryEntry] = field(default_factory=list)

    def record(
        self, 
        strategy: str, 
        context: dict[str, Any], 
        capability_delta: dict[str, float], 
        boundary: str, 
        confidence: float
    ) -> None:
        """
        Record a new observation of a strategy's effect.

        Args:
            strategy (str): The intervention strategy used (e.g., 'increase_rejection_sampling').
            context (dict[str, Any]): Contextual parameters during the campaign.
            capability_delta (dict[str, float]): Observed changes in capabilities (e.g., {'pass@1': 0.05}).
            boundary (str): Estimated condition where the strategy is effective or harmful.
            confidence (float): Confidence score for this observation (0.0 to 1.0).
        """
        self.entries.append(
            {
                "strategy": strategy,
                "context": context,
                "capability_delta": capability_delta,
                "boundary": boundary,
                "confidence": confidence,
            }
        )

    def get_relevant(self, strategy: str) -> list[MemoryEntry]:
        """
        Retrieve all memory entries relevant to a specific strategy.

        Args:
            strategy (str): The strategy to search for.

        Returns:
            list[MemoryEntry]: A list of relevant memory entries.
        """
        return [entry for entry in self.entries if entry["strategy"] == strategy]
