from __future__ import annotations

import argparse
from pathlib import Path

from src.experiments.es_chain import ESChainExperiment
from src.utils.logging import configure_logging


def main() -> None:
    parser = argparse.ArgumentParser(description="Run an early-stopping chain")
    parser.add_argument("--model", default="qwen-2.5-7b")
    parser.add_argument("--campaigns", type=int, default=10)
    parser.add_argument("--steps_per_campaign", type=int, default=20)
    parser.add_argument("--method", default="es")
    parser.add_argument("--output_dir", default="outputs/es_chain")
    args = parser.parse_args()

    experiment = ESChainExperiment(output_dir=Path(args.output_dir), steps=args.steps_per_campaign)
    logger = configure_logging(args.output_dir)
    result = experiment.run()
    logger.info("ES chain result: %s", result)


if __name__ == "__main__":
    main()
