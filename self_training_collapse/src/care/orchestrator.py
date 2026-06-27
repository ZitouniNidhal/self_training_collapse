from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.care.gate import TransferGate
from src.care.memory import CapabilityEffectMemory
from src.care.revision import BeliefRevision


@dataclass
class CAREOrchestrator:
    """Coordinate a simple CARE workflow over multiple campaigns."""

    memory: CapabilityEffectMemory = None
    gate: TransferGate = None
    revision: BeliefRevision = None

    def __post_init__(self) -> None:
        if self.memory is None:
            self.memory = CapabilityEffectMemory()
        if self.gate is None:
            self.gate = TransferGate()
        if self.revision is None:
            self.revision = BeliefRevision()

    def run_campaign(self, strategy: str, current_context: dict[str, Any], observed_delta: dict[str, float], predicted_delta: dict[str, float]) -> dict[str, Any]:
        decision = self.gate.evaluate(strategy, current_context, self.memory)
        self.memory.record(strategy, current_context, observed_delta, "default boundary", 0.5)
        revision = self.revision.update(self.memory, self.gate, observed_delta, predicted_delta)
        return {"decision": decision, "revision": revision}
