from __future__ import annotations

import argparse
from pathlib import Path

from src.utils.visualization import save_text_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate placeholder figure outputs")
    parser.add_argument("--results_dir", default="outputs")
    args = parser.parse_args()

    output = save_text_summary(Path(args.results_dir) / "all_figures.txt", "All figures generated placeholder summary\n")
    print(output)


if __name__ == "__main__":
    main()
