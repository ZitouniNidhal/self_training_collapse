from __future__ import annotations

from src.experiments.base_experiment import BaseExperiment


class CAREChainExperiment(BaseExperiment):
    """Run a multi-campaign CARE chain."""

    def run(self) -> dict[str, object]:
        result = super().run()
        result["kind"] = "care_chain"
        return result
