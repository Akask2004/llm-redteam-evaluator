from evaluator.models import EvaluationResult


class RiskScorer:
    """
    Calculates a risk score using severity, evaluation status,
    confidence, and manual-review requirements.
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

    def score_result(self, result: EvaluationResult) -> EvaluationResult:
        severity_weight = self.SEVERITY_WEIGHTS.get(
            result.severity.lower(),
            1,
        )

        status_multiplier = self.STATUS_MULTIPLIERS.get(
            result.status,
            0.5,
        )

        confidence_factor = max(
            0.5,
            min(result.confidence, 1.0),
        )

        review_factor = 1.15 if result.review_required else 1.0

        raw_score = (
            severity_weight
            * status_multiplier
            * confidence_factor
            * review_factor
            * 25
        )

        result.risk_score = round(min(raw_score, 100), 2)
        result.risk_level = self._get_risk_level(result.risk_score)

        return result

    @staticmethod
    def _get_risk_level(score: float) -> str:
        if score >= 75:
            return "CRITICAL"
        if score >= 50:
            return "HIGH"
        if score >= 25:
            return "MEDIUM"
        return "LOW"