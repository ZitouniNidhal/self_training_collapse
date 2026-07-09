from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.experiments.base_experiment import BaseExperiment
from src.models.trainer import ReinforceTrainer
from src.utils.logging import configure_logging




class DiagnosticExperiment(BaseExperiment):
    """
    Run a diagnostic campaign to simulate the rise-and-collapse
    phenomenon during self-training.
    """

    def run(self) -> dict[str, Any]:
        """
        Executes a simulated training run, logs metrics per step,
        and saves the trajectory to a file.
        """
        super().run()  # Ensures output_dir is created
        logger = configure_logging(self.output_dir)

        trainer = ReinforceTrainer(max_steps=self.steps)
        trajectory: list[dict[str, Any]] = []

        try:
            for _ in range(self.steps):
                metrics = trainer.train_step()
                trajectory.append(metrics)
        except Exception as exc:  # catch trainer errors
            logger.exception("Training failed during diagnostic run: %s", exc)
            raise

        # Save trajectory
        output_file = self.output_dir / "trajectory.jsonl"
        try:
            with output_file.open("w", encoding="utf-8") as f:
                for step_data in trajectory:
                    f.write(json.dumps(step_data) + "\n")
        except Exception as exc:
            logger.exception("Failed saving trajectory to %s: %s", output_file, exc)
            raise

        logger.info("Diagnostic run complete. Steps=%d, output=%s", len(trajectory), output_file)

        return {
            "kind": "diagnostic",
            "steps_completed": len(trajectory),
            "output_file": str(output_file),
            "final_pass_at_1": trajectory[-1]["pass_at_1"] if trajectory else 0.0,
        }
