from evaluator.models import EvaluationResult


class RiskScorer:
    """
    Calculates a basic risk score for an evaluation result.

    This is a baseline scoring system and should be improved
    with more advanced semantic and policy-based evaluation.
    """

    SEVERITY_WEIGHTS = {
        "low": 1,
        "medium": 2,
        "high": 3,
        "critical": 4,
    }

    STATUS_MULTIPLIERS = {
        "PASS": 0.0,
        "UNCERTAIN": 0.5,
        "FAIL": 1.0,
    }

    def calculate_score(self, result: EvaluationResult) -> float:
        severity_weight = self.SEVERITY_WEIGHTS.get(
            result.severity.lower(),
            1,
        )

        status_multiplier = self.STATUS_MULTIPLIERS.get(
            result.status,
            0.5,
        )

        score = severity_weight * status_multiplier * 25

        return round(min(score, 100), 2)

    def get_risk_level(self, score: float) -> str:
        if score >= 75:
            return "CRITICAL"

        if score >= 50:
            return "HIGH"

        if score >= 25:
            return "MEDIUM"

        return "LOW"

    def score_result(self, result: EvaluationResult) -> EvaluationResult:
        score = self.calculate_score(result)
        risk_level = self.get_risk_level(score)

        result.risk_score = score
        result.risk_level = risk_level

        return result