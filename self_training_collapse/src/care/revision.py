from __future__ import annotations

from typing import Any


class BeliefRevision:
    """Update beliefs when observed effects differ from predicted ones."""

    def update(self, memory: Any, gate: Any, observed_delta: dict[str, float], predicted_delta: dict[str, float]) -> dict[str, float]:
        delta = {k: observed_delta.get(k, 0.0) - predicted_delta.get(k, 0.0) for k in set(observed_delta) | set(predicted_delta)}
        if memory is None or not hasattr(memory, "entries") or not memory.entries:
            return delta
        return delta
