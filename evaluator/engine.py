import logging
import time
from typing import List

from evaluator.risk_scorer import RiskScorer
from adapters.base import BaseLLMAdapter
from probes.models import Probe
from evaluator.models import EvaluationResult
from evaluator.response_checker import ResponseChecker


logger = logging.getLogger(__name__)


class EvaluationEngine:

    def __init__(self, adapter: BaseLLMAdapter):
        self.adapter = adapter
        self.checker = ResponseChecker()
        self.risk_scorer = RiskScorer()

    def evaluate_probe(self, probe: Probe) -> EvaluationResult:
        started_at = time.perf_counter()

        try:
            response = self.adapter.generate(
                prompt=probe.prompt,
                probe_id=probe.id,
            )
        except Exception as error:
            latency_ms = round(
                (time.perf_counter() - started_at) * 1000,
                2,
            )

            logger.exception(
                "Probe %s failed during model generation.",
                probe.id,
            )

            result = EvaluationResult(
                probe_id=probe.id,
                category=probe.category,
                prompt=probe.prompt,
                response="",
                status="UNCERTAIN",
                severity=probe.severity,
                reason="Model generation failed before response checking.",
                expected_behavior=probe.expected_behavior,
                confidence=0.0,
                review_required=True,
                latency_ms=latency_ms,
                error=str(error),
            )

            return self.risk_scorer.score_result(result)

        latency_ms = round(
            (time.perf_counter() - started_at) * 1000,
            2,
        )

        logger.info(
            "Probe %s completed in %sms.",
            probe.id,
            latency_ms,
        )

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
            expected_behavior=probe.expected_behavior,
            confidence=check_result.confidence,
            review_required=check_result.review_required,
            latency_ms=latency_ms,
        )

        return self.risk_scorer.score_result(result)

    def evaluate(
        self,
        probes: List[Probe]
    ) -> List[EvaluationResult]:

        results = []

        for probe in probes:
            logger.info("Running probe: %s", probe.id)
            result = self.evaluate_probe(probe)
            results.append(result)

        return results
