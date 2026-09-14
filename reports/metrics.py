from collections import Counter, defaultdict
from typing import Any, Dict, List

from evaluator.models import EvaluationResult


def calculate_rate(count: int, total: int) -> float:
    if total == 0:
        return 0.0

    return round((count / total) * 100, 2)


def calculate_metrics(
    results: List[EvaluationResult],
) -> Dict[str, Any]:

    total_tests = len(results)

    status_counts = Counter(result.status for result in results)
    category_counts = defaultdict(Counter)
    severity_counts = Counter()
    failed_by_severity = Counter()
    risk_level_counts = Counter()

    total_risk_score = 0.0

    for result in results:
        category_counts[result.category][result.status] += 1
        severity_counts[result.severity] += 1
        risk_level_counts[result.risk_level] += 1

        total_risk_score += result.risk_score

        if result.status == "FAIL":
            failed_by_severity[result.severity] += 1

    passed = status_counts.get("PASS", 0)
    failed = status_counts.get("FAIL", 0)
    uncertain = status_counts.get("UNCERTAIN", 0)

    category_metrics = {}

    for category, counts in category_counts.items():
        category_total = sum(counts.values())

        category_passed = counts.get("PASS", 0)
        category_failed = counts.get("FAIL", 0)
        category_uncertain = counts.get("UNCERTAIN", 0)

        category_metrics[category] = {
            "total": category_total,
            "passed": category_passed,
            "failed": category_failed,
            "uncertain": category_uncertain,
            "pass_rate": calculate_rate(
                category_passed,
                category_total,
            ),
            "failure_rate": calculate_rate(
                category_failed,
                category_total,
            ),
            "uncertain_rate": calculate_rate(
                category_uncertain,
                category_total,
            ),
        }

    average_risk_score = (
        round(total_risk_score / total_tests, 2)
        if total_tests
        else 0.0
    )

    return {
        "total_tests": total_tests,
        "passed": passed,
        "failed": failed,
        "uncertain": uncertain,
        "pass_rate": calculate_rate(passed, total_tests),
        "failure_rate": calculate_rate(failed, total_tests),
        "uncertain_rate": calculate_rate(uncertain, total_tests),
        "average_risk_score": average_risk_score,
        "category_metrics": dict(category_metrics),
        "severity_distribution": dict(severity_counts),
        "failed_by_severity": dict(failed_by_severity),
        "risk_level_distribution": dict(risk_level_counts),
    }