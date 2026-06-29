from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.care.memory import CapabilityEffectMemory


class TransferGate:
    """
    Decide whether to reuse, adapt, pilot, or reject a strategy.
    
    The Transfer Gate evaluates proposed self-improvement strategies against
    the capability-effect memory to determine if they are safe to apply in
    the current context, protecting critical capabilities from collapsing.
    """

    def __init__(self, protected_capabilities: list[str] | None = None) -> None:
        """
        Initialize the Transfer Gate.

        Args:
            protected_capabilities (list[str] | None): A list of capability names
                (e.g., ['diversity', 'hard_case_acc']) that should not degrade.
        """
        self.protected_capabilities = protected_capabilities or []

    def evaluate(self, strategy: str, current_context: dict[str, Any], memory: CapabilityEffectMemory) -> str:
        """
        Evaluate a strategy against memory to make a transfer decision.

        Args:
            strategy (str): The proposed intervention strategy.
            current_context (dict[str, Any]): Context of the current campaign.
            memory (CapabilityEffectMemory): The capability-effect memory instance.

        Returns:
            str: The decision string, one of "reuse", "adapt", "pilot", or "reject".
        """
        if not memory.entries:
            return "pilot"
        
        relevant = memory.get_relevant(strategy)
        if not relevant:
            return "pilot"
            
        # In a full implementation, this would evaluate the capability_delta 
        # and confidence against the protected_capabilities.
        return "reuse"
