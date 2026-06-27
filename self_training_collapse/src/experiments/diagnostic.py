from __future__ import annotations

from pathlib import Path

from src.experiments.base_experiment import BaseExperiment


class DiagnosticExperiment(BaseExperiment):
    """Run a simple diagnostic campaign."""

    def run(self) -> dict[str, object]:
        result = super().run()
        result["kind"] = "diagnostic"
        return result
