from __future__ import annotations

from typing import Any


class CapabilityTracker:
    """Track high-level capability metrics over time."""

    def __init__(self) -> None:
        self.metrics: dict[str, list[float]] = {}

    def update(self, values: dict[str, float]) -> None:
        for key, value in values.items():
            self.metrics.setdefault(key, []).append(float(value))

    def snapshot(self) -> dict[str, Any]:
        return {key: values[-1] if values else 0.0 for key, values in self.metrics.items()}
