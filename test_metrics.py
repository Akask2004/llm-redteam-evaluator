from evaluator.models import EvaluationResult
from reports.metrics import MetricsCalculator


def test_metrics_calculation():
    results = [
        EvaluationResult(
            probe_id="JB001",
            category="jailbreak",
            prompt="Test prompt",
            response="I cannot help.",
            status="PASS",
            severity="low",
            reason="Refusal detected",
            confidence=0.9,
            review_required=False,
        ),
        EvaluationResult(
            probe_id="JB002",
            category="jailbreak",
            prompt="Test prompt",
            response="Here are the steps.",
            status="FAIL",
            severity="high",
            reason="Compliance detected",
            confidence=0.8,
            review_required=True,
        ),
    ]

    metrics = MetricsCalculator().calculate(results)

    assert metrics["total_probes"] == 2
    assert metrics["passed"] == 1
    assert metrics["failed"] == 1
    assert metrics["failure_rate"] == 50.0