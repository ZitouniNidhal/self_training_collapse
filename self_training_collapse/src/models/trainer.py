from __future__ import annotations

import math
from typing import Any, TypedDict


class StepMetrics(TypedDict):
    """Metrics collected during a single training step."""
    step: int
    pass_at_1: float
    reward: float
    loss: float


class BaseTrainer:
    """Abstract base class for simulated LLM training algorithms."""

    def __init__(self, learning_rate: float = 1e-6, max_steps: int = 200) -> None:
        self.learning_rate = learning_rate
        self.max_steps = max_steps
        self.current_step = 0

    def train_step(self) -> StepMetrics:
        """Simulate a single training step and return metrics."""
        raise NotImplementedError("Subclasses must implement train_step()")


class ReinforceTrainer(BaseTrainer):
    """
    Simulates REINFORCE training, which famously exhibits the rise-and-collapse
    failure mode during code capability self-training.
    """

    def train_step(self) -> StepMetrics:
        self.current_step += 1
        # Simulate Rise and Collapse
        # Peak at ~50 steps, collapse near 200 steps
        if self.current_step <= 50:
            pass_at_1 = 0.25 + 0.56 * (self.current_step / 50)  # Rises to 81%
        else:
            # Collapse phase
            progress = (self.current_step - 50) / 150
            pass_at_1 = 0.81 * math.exp(-5 * progress)  # Exponential decay

        return {
            "step": self.current_step,
            "pass_at_1": pass_at_1,
            "reward": pass_at_1 * 10,
            "loss": max(0.0, 1.0 - pass_at_1),
        }


class GrpoTrainer(BaseTrainer):
    """
    Simulates Group Relative Policy Optimization (GRPO) training, which
    acts as an algorithm-level variance reduction technique to mitigate collapse.
    """

    def train_step(self) -> StepMetrics:
        self.current_step += 1
        # GRPO mitigates collapse, so pass_at_1 stays relatively stable
        # Rise phase is similar but less extreme, and no severe collapse.
        if self.current_step <= 50:
            pass_at_1 = 0.25 + 0.40 * (self.current_step / 50)  # Rises to ~65%
        else:
            # Stable phase with slight degradation
            progress = (self.current_step - 50) / 150
            pass_at_1 = 0.65 - 0.1 * progress

        return {
            "step": self.current_step,
            "pass_at_1": pass_at_1,
            "reward": pass_at_1 * 10,
            "loss": max(0.0, 1.0 - pass_at_1),
        }
