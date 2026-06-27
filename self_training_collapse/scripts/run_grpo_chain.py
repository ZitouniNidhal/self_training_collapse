from __future__ import annotations

import argparse
from pathlib import Path

from src.experiments.grpo_chain import GRPOChainExperiment


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a GRPO chain")
    parser.add_argument("--model", default="qwen-2.5-7b")
    parser.add_argument("--campaigns", type=int, default=10)
    parser.add_argument("--steps_per_campaign", type=int, default=20)
    parser.add_argument("--method", default="grpo")
    parser.add_argument("--output_dir", default="outputs/grpo_chain")
    args = parser.parse_args()

    experiment = GRPOChainExperiment(output_dir=Path(args.output_dir), steps=args.steps_per_campaign)
    result = experiment.run()
    print(result)


if __name__ == "__main__":
    main()
