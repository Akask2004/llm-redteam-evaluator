import csv
import io
import json
from datetime import datetime
from typing import List

from evaluator.models import EvaluationResult
from reports.metrics import calculate_metrics


class ReportExporter:
    """
    Exports evaluation results into JSON and CSV formats.
    """

    @staticmethod
    def _serialize_result(result: EvaluationResult) -> dict:
        """
        Convert an EvaluationResult object into a dictionary.
        """

        return {
            "probe_id": result.probe_id,
            "category": result.category,
            "prompt": result.prompt,
            "expected_behavior": result.expected_behavior,
            "response": result.response,
            "status": result.status,
            "severity": result.severity,
            "reason": result.reason,
            "confidence": result.confidence,
            "review_required": result.review_required,
            "risk_score": result.risk_score,
            "risk_level": result.risk_level,
            "latency_ms": result.latency_ms,
            "error": result.error,
        }

    @classmethod
    def to_json(
        cls,
        results: List[EvaluationResult],
    ) -> str:
        """
        Export evaluation results as a JSON string.
        """

        data = [
            cls._serialize_result(result)
            for result in results
        ]

        return json.dumps(
            data,
            indent=4,
            ensure_ascii=False,
        )

    @classmethod
    def to_report_json(
        cls,
        results: List[EvaluationResult],
        adapter: str = "unknown",
        model_name: str | None = None,
    ) -> str:
        """
        Export a complete report with metadata, metrics, and results.
        """

        report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "adapter": adapter,
                "model_name": model_name,
            },
            "metrics": calculate_metrics(results),
            "results": [
                cls._serialize_result(result)
                for result in results
            ],
        }

        return json.dumps(
            report,
            indent=4,
            ensure_ascii=False,
        )

    @classmethod
    def to_csv(
        cls,
        results: List[EvaluationResult],
    ) -> str:
        """
        Export evaluation results as a CSV string.
        """

        data = [
            cls._serialize_result(result)
            for result in results
        ]

        if not data:
            return ""

        output = io.StringIO()

        writer = csv.DictWriter(
            output,
            fieldnames=data[0].keys(),
        )

        writer.writeheader()
        writer.writerows(data)

        return output.getvalue()


# ---------------------------------------------------------
# Backward-compatible helper functions
# ---------------------------------------------------------

def export_json(
    results: List[EvaluationResult],
) -> str:
    """
    Backward-compatible JSON export function.

    Allows older code to use:

        export_json(results)
    """

    return ReportExporter.to_json(results)


def export_csv(
    results: List[EvaluationResult],
) -> str:
    """
    Backward-compatible CSV export function.

    Allows older code to use:

        export_csv(results)
    """

    return ReportExporter.to_csv(results)


def export_report_json(
    results: List[EvaluationResult],
    adapter: str = "unknown",
    model_name: str | None = None,
) -> str:
    """
    Export a full report envelope with metadata, metrics, and results.
    """

    return ReportExporter.to_report_json(
        results,
        adapter=adapter,
        model_name=model_name,
    )
