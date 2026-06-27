from __future__ import annotations

from typing import Any


class ModelLoader:
    """A minimal placeholder for loading a model."""

    def __init__(self, model_name: str = "qwen-2.5-3b") -> None:
        self.model_name = model_name

    def load(self) -> dict[str, Any]:
        return {"model_name": self.model_name, "status": "placeholder"}
