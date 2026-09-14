from collections import Counter
from typing import List

from evaluator.models import EvaluationResult


class MetricsCalculator:
    """
    Calculates summary metrics for evaluation results.
    """

    def calculate(self, results: List[EvaluationResult]) -> dict:
        total = len(results)

        status_counts = Counter(
            result.status for result in results
        )

        category_counts = Counter(
            result.category for result in results
        )

        severity_counts = Counter(
            result.severity for result in results
        )

        risk_counts = Counter(
            result.risk_level for result in results
        )

        passed = status_counts.get("PASS", 0)
        failed = status_counts.get("FAIL", 0)
        uncertain = status_counts.get("UNCERTAIN", 0)

        pass_rate = (
            (passed / total) * 100
            if total > 0
            else 0.0
        )

        failure_rate = (
            (failed / total) * 100
            if total > 0
            else 0.0
        )

        return {
            "total_probes": total,
            "passed": passed,
            "failed": failed,
            "uncertain": uncertain,
            "pass_rate": round(pass_rate, 2),
            "failure_rate": round(failure_rate, 2),
            "status_distribution": dict(status_counts),
            "category_distribution": dict(category_counts),
            "severity_distribution": dict(severity_counts),
            "risk_distribution": dict(risk_counts),
        }


def calculate_metrics(results: List[EvaluationResult]) -> dict:
    """
    Backward-compatible function used by older tests and scripts.
    """
    return MetricsCalculator().calculate(results)