from dataclasses import dataclass
from typing import Literal


@dataclass
class EvaluationResult:
    probe_id: str
    category: str
    prompt: str
    response: str
    status: Literal["PASS", "FAIL", "UNCERTAIN"]
    severity: str
    reason: str
    risk_score: float = 0.0
    risk_level: str = "LOW"