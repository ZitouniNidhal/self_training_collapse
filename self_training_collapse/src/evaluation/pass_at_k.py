from __future__ import annotations

from typing import Sequence


def pass_at_k(scores: Sequence[float], k: int = 1) -> float:
    """Return the fraction of samples that pass at the requested k."""
    if not scores:
        return 0.0
    count = sum(1 for score in scores if score >= 1.0)
    return count / len(scores)
