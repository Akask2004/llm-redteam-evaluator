import csv
import json

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from evaluator.models import EvaluationResult


def get_timestamp() -> str:
    """Return the current UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


def export_json(
    results: List[EvaluationResult],
    metrics: Dict[str, Any],
    output_path: str,
) -> Path:
    """Export evaluation results and metrics to JSON."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "generated_at": get_timestamp(),
        "summary": metrics,
        "results": [asdict(result) for result in results],
    }

    with path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return path


def export_csv(
    results: List[EvaluationResult],
    output_path: str,
) -> Path:
    """Export evaluation results to CSV."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "probe_id",
        "category",
        "prompt",
        "response",
        "status",
        "severity",
        "reason",
        "risk_score",
        "risk_level",
    ]

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for result in results:
            writer.writerow(asdict(result))

    return path