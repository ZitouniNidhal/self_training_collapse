from __future__ import annotations

from src.experiments.base_experiment import BaseExperiment


class ESChainExperiment(BaseExperiment):
    """Run an early-stopping chain."""

    def run(self) -> dict[str, object]:
        result = super().run()
        result["kind"] = "es_chain"
        return result
