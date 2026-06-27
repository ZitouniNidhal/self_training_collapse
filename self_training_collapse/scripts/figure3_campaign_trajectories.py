from __future__ import annotations

import argparse
from pathlib import Path

from src.utils.visualization import save_text_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a placeholder campaign trajectory summary")
    parser.add_argument("--chain_dir", default="outputs/care_chain")
    args = parser.parse_args()

    summary = f"Campaign trajectory summary for {args.chain_dir}\n"
    output = save_text_summary(Path(args.chain_dir) / "figure3_summary.txt", summary)
    print(output)


if __name__ == "__main__":
    main()
