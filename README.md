Self-Training Collapse: Rise-and-Collapse in LLM Self-Improvement

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-2606.21090-red.svg)](https://arxiv.org/abs/2606.21090)

> **Self-Improvement Can Self-Regress: The Rise-and-Collapse Failure Mode of LLM Self-Training**
>
> This repository contains a reproducible implementation of the CARE (Capability-Aware Research Experience) framework and the experimental infrastructure used to study rise-and-collapse dynamics in LLM self-training with verifiable rewards.

## Overview

This project implements and studies the "rise-and-collapse" phenomenon in LLM self-training:
- **Within-campaign collapse**: REINFORCE training on code rewards rises to a peak in ~50 steps, then collapses to near-zero
- **Between-campaign carryover**: Sequential training campaigns either compound gains or drift downward
- **Three intervention levels**: Campaign-level memory (CARE), within-campaign stopping (ES), and algorithm-level variance reduction (GRPO)

### Key Results

| Model | Method | End pass@1 | Notes |
|-------|--------|-----------|-------|
| Qwen-2.5-3B | Naive REINFORCE | 4.9% | Fragile regime |
| Qwen-2.5-3B | **CARE v2** | **9.5%** | ✅ Best at 3B |
| Qwen-2.5-7B | Naive REINFORCE | 11.8% | Rich signal |
| Qwen-2.5-7B | CARE v2 | 13.8% | Parity with naive |
| Qwen-2.5-7B | **ES (Early Stop)** | **22.2%** | ✅ Best at 7B |
| Qwen-2.5-7B | GRPO | 20.7% | Algorithm-level fix |

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/self-training-collapse.git
cd self-training-collapse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Running a Minimal Experiment

```bash
# Run a single diagnostic campaign (200 steps, no chaining)
python scripts/run_diagnostic.py --model qwen-2.5-3b --steps 200 --output_dir outputs/diagnostic

# Run a 10-campaign CARE chain
python scripts/run_care_chain.py --model qwen-2.5-3b --campaigns 10 --steps_per_campaign 20 --method care

# Run with early stopping (ES)
python scripts/run_care_chain.py --model qwen-2.5-7b --campaigns 10 --steps_per_campaign 20 --method es
```

### Reproducing Paper Figures

```bash
# Generate Figure 1: Rise-then-collapse trajectory
python scripts/figure1_diagnostic.py --checkpoint_path outputs/diagnostic

# Generate Figure 3: Campaign-aligned trajectories
python scripts/figure3_campaign_trajectories.py --chain_dir outputs/care_chain

# Generate all figures
python scripts/generate_all_figures.py --results_dir outputs/
```

## Project Structure

```
self-training-collapse/
├── src/
│   ├── care/              # CARE framework implementation
│   │   ├── memory.py      # Capability-Effect Memory (Module 1)
│   │   ├── gate.py        # Self-Improvement Transfer Gate (Module 2)
│   │   ├── revision.py    # Regression-Aware Belief Revision (Module 3)
│   │   └── orchestrator.py # Full CARE orchestrator
│   ├── experiments/       # Experiment runners
│   │   ├── base_experiment.py
│   │   ├── diagnostic.py  # Single-campaign diagnostics
│   │   ├── care_chain.py  # Multi-campaign CARE chains
│   │   ├── es_chain.py    # Early stopping chains
│   │   └── grpo_chain.py  # GRPO baseline chains
│   ├── models/            # Model loading and training
│   │   ├── model_loader.py
│   │   ├── trainer.py     # REINFORCE / GRPO trainer
│   │   └── checkpoint.py
│   ├── evaluation/        # Evaluation infrastructure
│   │   ├── codegrader.py  # Binary code reward
│   │   ├── pass_at_k.py   # pass@k metrics
│   │   └── capability_tracker.py  # Multi-dim capability tracking
│   └── utils/             # Utilities
│       ├── config.py
│       ├── logging.py
│       └── visualization.py
├── configs/               # YAML configuration files
│   ├── care_default.yaml
│   ├── es_default.yaml
│   └── grpo_default.yaml
├── scripts/               # Executable scripts
│   ├── run_diagnostic.py
│   ├── run_care_chain.py
│   ├── run_es_chain.py
│   ├── run_grpo_chain.py
│   ├── figure1_diagnostic.py
│   ├── figure3_campaign_trajectories.py
│   └── generate_all_figures.py
├── tests/                 # Test suite
├── notebooks/             # Jupyter notebooks for analysis
├── examples/              # Minimal examples
├── docs/                  # Documentation
│   ├── THEORY.md          # Theoretical background
│   ├── CITATIONS.bib      # BibTeX references
│   └── API.md             # API documentation
├── data/                  # Data directory (not versioned)
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md
```

## The CARE Framework

CARE (Capability-Aware Research Experience) is a meta-scientific memory system with three modules:

### Module 1: Capability-Effect Memory
Records structured entries: `{strategy, context, capability_delta, boundary, confidence}`

```python
from src.care.memory import CapabilityEffectMemory

memory = CapabilityEffectMemory()
memory.record(
    strategy="increase_rejection_sampling",
    context={"positive_rate": 0.2, "model_size": "3B"},
    capability_delta={"pass@1": +0.06, "diversity": -0.04, "hard_case_acc": -0.01},
    boundary="harmful when positive_rate > 0.4",
    confidence=0.85
)
```

### Module 2: Self-Improvement Transfer Gate
Decides whether to reuse, adapt, pilot, or reject a strategy:

```python
from src.care.gate import TransferGate

gate = TransferGate(protected_capabilities=["diversity", "hard_case_acc"])
decision = gate.evaluate(strategy, current_context, memory)
# Returns: "reuse" | "adapt" | "pilot" | "reject"
```

### Module 3: Regression-Aware Belief Revision
Updates beliefs when observed effects deviate from predictions:

```python
from src.care.revision import BeliefRevision

revision = BeliefRevision()
revision.update(memory, gate, observed_delta, predicted_delta)
```

## Core Concepts

### Rise-and-Collapse Dynamics

The paper documents a robust failure mode where REINFORCE self-training on code rewards exhibits:

1. **Rise phase**: pass@1 climbs rapidly (25% → 81% in ~50 steps for Qwen-2.5-7B)
2. **Collapse phase**: pass@1 degrades to near-zero by step 200
3. **Structural properties**:
   - Phase-transition score ≈ 0.78 (78% of drop happens in single step)
   - Collapse onset ≈ step 16.7/20 (late in campaign)
   - Zero usable post-onset latency for end-of-campaign gates

### Three Intervention Levels

| Level | Method | Timescale | Signal | When It Helps |
|-------|--------|-----------|--------|---------------|
| Between-campaign | CARE | After each campaign | Memory + end/peak ratio | Fragile regime (3B) |
| Within-campaign | ES | During campaign | Per-step trajectory | Rich signal (7B) |
| Algorithm-level | GRPO | Inside each update | Group-relative reward | Improves carryover |

## Reproducibility

All experiments use:
- **Base models**: Qwen-2.5-3B-Instruct, Qwen-2.5-7B-Instruct
- **Training**: REINFORCE with binary CodeGrader reward (or GRPO variant)
- **Hardware**: 1× 8×GB200 GPUs per job
- **Hyperparameters**: lr=1e-6, temperature=0.7, 16 samples/prompt
- **Campaign lengths**: 20 steps (headline), 50 steps (ablation), 200 steps (diagnostic)

### Data

Competitive programming problems from:
- HumanEval
- MBPP  
- APPS (medium-easy difficulty)

Problems include function signature, docstring, and unit test assertions for CodeGrader execution.

## Citation

If you use this code or build on this work, please cite:

```bibtex
@article{lin2026self,
  title={Self-Improvement Can Self-Regress: The Rise-and-Collapse Failure Mode of LLM Self-Training},
  author={Lin, Jianzhe},
  journal={arXiv preprint arXiv:2606.21090},
  year={2026}
}
```

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

This work was done at Meta AI. We thank the open-source community for:
- [Qwen](https://github.com/QwenLM/Qwen) model family
- [vLLM](https://github.com/vllm-project/vllm) for efficient inference
- [Transformers](https://github.com/huggingface/transformers) library
- [DeepSpeed](https://github.com/microsoft/DeepSpeed) / FSDP for distributed training

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.


