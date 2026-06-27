from __future__ import annotations

import argparse
from pathlib import Path

from src.experiments.diagnostic import DiagnosticExperiment


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a single diagnostic campaign")
    parser.add_argument("--model", default="qwen-2.5-3b")
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--output_dir", default="outputs/diagnostic")
    args = parser.parse_args()

    experiment = DiagnosticExperiment(output_dir=Path(args.output_dir), steps=args.steps)
    result = experiment.run()
    print(result)


if __name__ == "__main__":
    main()
