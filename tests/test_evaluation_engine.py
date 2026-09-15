from adapters.base import BaseLLMAdapter
from evaluator.engine import EvaluationEngine
from probes.models import Probe


class FailingAdapter(BaseLLMAdapter):
    def generate(self, prompt: str, probe_id: str | None = None) -> str:
        raise RuntimeError("adapter unavailable")


def test_engine_records_probe_error_and_continues():
    probe = Probe(
        id="ERR001",
        category="jailbreak",
        prompt="Test prompt",
        expected_behavior="The model should refuse unsafe requests.",
        severity="high",
    )

    result = EvaluationEngine(FailingAdapter()).evaluate_probe(probe)

    assert result.status == "UNCERTAIN"
    assert result.review_required is True
    assert result.error == "adapter unavailable"
    assert result.latency_ms >= 0
    assert result.expected_behavior == probe.expected_behavior
