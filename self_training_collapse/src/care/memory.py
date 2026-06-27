from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CapabilityEffectMemory:
    """Store and retrieve capability-effect observations for self-training campaigns."""

    entries: list[dict[str, Any]] = field(default_factory=list)

    def record(self, strategy: str, context: dict[str, Any], capability_delta: dict[str, float], boundary: str, confidence: float) -> None:
        self.entries.append(
            {
                "strategy": strategy,
                "context": context,
                "capability_delta": capability_delta,
                "boundary": boundary,
                "confidence": confidence,
            }
        )

    def get_relevant(self, strategy: str) -> list[dict[str, Any]]:
        return [entry for entry in self.entries if entry["strategy"] == strategy]
