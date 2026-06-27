from __future__ import annotations

import logging
from pathlib import Path


def configure_logging(output_dir: str | Path | None = None) -> logging.Logger:
    logger = logging.getLogger("self_training_collapse")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
        logger.addHandler(handler)
    if output_dir is not None:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    return logger
