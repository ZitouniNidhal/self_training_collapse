from __future__ import annotations

from pathlib import Path


def save_text_summary(path: str | Path, content: str) -> Path:
    output = Path(path)
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
    except Exception as exc:
        raise IOError(f"Failed to write summary to {output}: {exc}") from exc
    return output
