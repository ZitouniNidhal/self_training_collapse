from __future__ import annotations

import argparse
from pathlib import Path

from src.experiments.care_chain import CAREChainExperiment
from src.utils.logging import configure_logging


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a CARE chain")
    parser.add_argument("--model", default="qwen-2.5-3b")
    parser.add_argument("--campaigns", type=int, default=10)
    parser.add_argument("--steps_per_campaign", type=int, default=20)
    parser.add_argument("--method", default="care")
    parser.add_argument("--output_dir", default="outputs/care_chain")
    args = parser.parse_args()

    experiment = CAREChainExperiment(output_dir=Path(args.output_dir), steps=args.steps_per_campaign)
    logger = configure_logging(args.output_dir)
    result = experiment.run()
    logger.info("CARE chain result: %s", result)


if __name__ == "__main__":
    main()
