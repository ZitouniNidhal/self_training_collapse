from src.care.memory import CapabilityEffectMemory
from src.care.gate import TransferGate
from src.care.revision import BeliefRevision


def test_memory_record_and_retrieve() -> None:
    memory = CapabilityEffectMemory()
    memory.record("strategy_a", {"x": 1}, {"pass@1": 0.1}, "boundary", 0.8)
    assert memory.get_relevant("strategy_a")


def test_transfer_gate_defaults_to_pilot_when_no_memory() -> None:
    gate = TransferGate()
    decision = gate.evaluate("strategy_a", {"x": 1}, CapabilityEffectMemory())
    assert decision == "pilot"


def test_belief_revision_returns_delta() -> None:
    revision = BeliefRevision()
    delta = revision.update(None, None, {"pass@1": 0.2}, {"pass@1": 0.1})
    assert delta["pass@1"] == 0.1
