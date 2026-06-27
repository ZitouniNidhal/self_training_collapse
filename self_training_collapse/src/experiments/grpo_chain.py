from __future__ import annotations

from src.experiments.base_experiment import BaseExperiment


class GRPOChainExperiment(BaseExperiment):
    """Run a GRPO baseline chain."""

    def run(self) -> dict[str, object]:
        result = super().run()
        result["kind"] = "grpo_chain"
        return result
