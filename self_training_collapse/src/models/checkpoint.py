from __future__ import annotations

from pathlib import Path


class CheckpointManager:
    """Persist lightweight checkpoint metadata."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)

    def save(self, name: str, payload: dict[str, object]) -> Path:
        output = self.path / f"{name}.json"
        output.write_text(str(payload), encoding="utf-8")
        return output
