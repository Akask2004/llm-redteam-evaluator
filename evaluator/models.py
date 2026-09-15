from dataclasses import dataclass
from typing import Literal


EvaluationStatus = Literal[
    "PASS",
    "FAIL",
    "UNCERTAIN",
]

SeverityLevel = Literal[
    "low",
    "medium",
    "high",
    "critical",
]

RiskLevel = Literal[
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
]


@dataclass
class EvaluationResult:
    """
    Represents the result of evaluating one adversarial probe.
    """

    probe_id: str
    category: str
    prompt: str
    response: str

    status: EvaluationStatus
    severity: SeverityLevel
    reason: str

    # New evaluation metadata
    expected_behavior: str = ""
    confidence: float = 0.0
    review_required: bool = False

    # Risk information
    risk_score: float = 0.0
    risk_level: RiskLevel = "LOW"

    # Execution metadata
    latency_ms: float = 0.0
    error: str | None = None
