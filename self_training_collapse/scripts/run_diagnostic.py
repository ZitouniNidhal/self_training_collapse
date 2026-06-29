from __future__ import annotations

import argparse
import logging
from pathlib import Path

from src.experiments.diagnostic import DiagnosticExperiment
from src.models.model_loader import ModelLoader


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def main() -> None:
    setup_logging()
    
    parser = argparse.ArgumentParser(description="Run a single diagnostic campaign")
    parser.add_argument("--model", default="qwen-2.5-3b", help="Model name to simulate.")
    parser.add_argument("--steps", type=int, default=200, help="Number of steps in the campaign.")
    parser.add_argument("--output_dir", default="outputs/diagnostic", help="Output directory.")
    args = parser.parse_args()

    logging.info(f"Starting diagnostic experiment with model: {args.model}")
    logging.info(f"Configured for {args.steps} steps. Output dir: {args.output_dir}")

    # Simulate loading model
    loader = ModelLoader(model_name=args.model)
    config = loader.load()
    logging.info(f"Loaded simulated model: {config.name} ({config.parameters / 1e9:.1f}B params)")

    experiment = DiagnosticExperiment(output_dir=Path(args.output_dir), steps=args.steps)
    result = experiment.run()
    
    logging.info(f"Experiment completed. Final pass@1: {result['final_pass_at_1']:.4f}")
    logging.info(f"Trajectory saved to {result['output_file']}")


if __name__ == "__main__":
    main()
