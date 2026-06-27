from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class BaseExperiment:
    """A lightweight experiment skeleton."""

    output_dir: Path | str = field(default_factory=lambda: Path("outputs/experiment"))
    steps: int = 10

    def __post_init__(self) -> None:
        self.output_dir = Path(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self) -> dict[str, Any]:
        return {"steps": self.steps, "output_dir": str(self.output_dir)}
