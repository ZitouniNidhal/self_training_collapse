from __future__ import annotations

import argparse
from pathlib import Path

from src.utils.visualization import save_text_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a placeholder figure summary")
    parser.add_argument("--checkpoint_path", default="outputs/diagnostic")
    args = parser.parse_args()

    summary = f"Diagnostic summary for {args.checkpoint_path}\n"
    output = save_text_summary(Path(args.checkpoint_path) / "figure1_summary.txt", summary)
    print(output)


if __name__ == "__main__":
    main()
