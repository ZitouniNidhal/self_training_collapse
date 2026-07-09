from __future__ import annotations

import argparse
from pathlib import Path

from src.experiments.grpo_chain import GRPOChainExperiment
from src.utils.logging import configure_logging


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a GRPO chain")
    parser.add_argument("--model", default="qwen-2.5-7b")
    parser.add_argument("--campaigns", type=int, default=10)
    parser.add_argument("--steps_per_campaign", type=int, default=20)
    parser.add_argument("--method", default="grpo")
    parser.add_argument("--output_dir", default="outputs/grpo_chain")
    args = parser.parse_args()

    experiment = GRPOChainExperiment(output_dir=Path(args.output_dir), steps=args.steps_per_campaign)
    logger = configure_logging(args.output_dir)
    result = experiment.run()
    logger.info("GRPO chain result: %s", result)


if __name__ == "__main__":
    main()
