from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TypedDict

from src.care.gate import TransferGate
from src.care.memory import CapabilityEffectMemory
from src.care.revision import BeliefRevision


class CampaignResult(TypedDict):
    """Result of running a single CARE campaign."""
    decision: str
    revision: Any


@dataclass
class CAREOrchestrator:
    """
    Coordinate a simple CARE workflow over multiple campaigns.
    
    The Orchestrator ties together the Memory (Module 1), Transfer Gate (Module 2),
    and Belief Revision (Module 3) to manage the self-training lifecycle.
    """

    memory: CapabilityEffectMemory | None = None
    gate: TransferGate | None = None
    revision: BeliefRevision | None = None

    def __post_init__(self) -> None:
        """Initialize default modules if not provided."""
        if self.memory is None:
            self.memory = CapabilityEffectMemory()
        if self.gate is None:
            self.gate = TransferGate()
        if self.revision is None:
            self.revision = BeliefRevision()

    def run_campaign(
        self, 
        strategy: str, 
        current_context: dict[str, Any], 
        observed_delta: dict[str, float], 
        predicted_delta: dict[str, float]
    ) -> CampaignResult:
        """
        Run a single campaign iteration through the CARE workflow.

        Args:
            strategy (str): The intervention strategy being evaluated.
            current_context (dict[str, Any]): Context of the current campaign.
            observed_delta (dict[str, float]): The actual observed changes in capabilities.
            predicted_delta (dict[str, float]): The previously predicted changes.

        Returns:
            CampaignResult: A dictionary containing the gate's decision and revision status.
        """
        assert self.gate is not None
        assert self.memory is not None
        assert self.revision is not None
        
        decision = self.gate.evaluate(strategy, current_context, self.memory)
        self.memory.record(strategy, current_context, observed_delta, "default boundary", 0.5)
        revision_result = self.revision.update(self.memory, self.gate, observed_delta, predicted_delta)
        
        return {"decision": decision, "revision": revision_result}
