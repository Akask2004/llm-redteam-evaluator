from dataclasses import dataclass
from typing import Literal


@dataclass
class Probe:
    id: str
    category: str
    prompt: str
    expected_behavior: str
    severity: Literal["low", "medium", "high", "critical"]