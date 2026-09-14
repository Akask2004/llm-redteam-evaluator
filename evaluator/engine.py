from typing import List
from evaluator.risk_scorer import RiskScorer
from adapters.base import BaseLLMAdapter
from probes.models import Probe
from evaluator.models import EvaluationResult
from evaluator.response_checker import ResponseChecker


class EvaluationEngine:

    def __init__(self, adapter: BaseLLMAdapter):
        self.adapter = adapter
        self.checker = ResponseChecker()
        self.risk_scorer = RiskScorer()

    def evaluate_probe(self, probe: Probe) -> EvaluationResult:
        response = self.adapter.generate(
                prompt=probe.prompt,
                probe_id=probe.id,
            )
        print("\n" + "-" * 60)
        print(f"PROBE ID: {probe.id}")
        print(f"CATEGORY: {probe.category}")
        print("MODEL RESPONSE:")
        print(response)
        print("-" * 60)

        check_result = self.checker.check(
        response=response,
        category=probe.category,
    )

        result = EvaluationResult(
            probe_id=probe.id,
            category=probe.category,
            prompt=probe.prompt,
            response=response,
            status=check_result.status,
            severity=probe.severity,
            reason=check_result.reason,
            confidence=check_result.confidence,
            review_required=check_result.review_required,
        )

        return self.risk_scorer.score_result(result)
    def evaluate(
        self,
        probes: List[Probe]
    ) -> List[EvaluationResult]:

        results = []

        for probe in probes:

            print(f"Running probe: {probe.id}")

            result = self.evaluate_probe(probe)

            results.append(result)

        return results