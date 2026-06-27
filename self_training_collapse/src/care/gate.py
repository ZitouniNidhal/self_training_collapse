from __future__ import annotations

from typing import Any


class TransferGate:
    """Decide whether to reuse, adapt, pilot, or reject a strategy."""

    def __init__(self, protected_capabilities: list[str] | None = None) -> None:
        self.protected_capabilities = protected_capabilities or []

    def evaluate(self, strategy: str, current_context: dict[str, Any], memory: Any) -> str:
        if not memory.entries:
            return "pilot"
        relevant = memory.get_relevant(strategy)
        if not relevant:
            return "pilot"
        return "reuse"
