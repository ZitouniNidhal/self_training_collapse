from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML configuration file from `path`.

    Returns an empty dict on empty file. Raises FileNotFoundError on missing
    file and ValueError on invalid YAML.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {p}")
    try:
        # allow YAML or JSON-style files
        text = p.read_text(encoding="utf-8")
        if not text.strip():
            return {}
        # Try YAML first (handles both YAML and JSON)
        return yaml.safe_load(text) or {}
    except yaml.YAMLError as exc:
        # Provide a clearer error for callers
        raise ValueError(f"Failed to parse YAML config {p}: {exc}") from exc
    except Exception:
        # Re-raise unexpected errors
        raise
