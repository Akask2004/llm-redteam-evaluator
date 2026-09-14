from typing import List, Optional

from .models import Probe
from .jailbreak import JAILBREAK_PROBES
from .injection import INJECTION_PROBES
from .leakage import LEAKAGE_PROBES


class ProbeManager:

    def __init__(self):
        self.probes = (
            JAILBREAK_PROBES
            + INJECTION_PROBES
            + LEAKAGE_PROBES
        )

    def get_all_probes(self) -> List[Probe]:
        return self.probes

    def get_by_category(self, category: str) -> List[Probe]:
        return [
            probe
            for probe in self.probes
            if probe.category == category
        ]

    def get_by_id(self, probe_id: str) -> Optional[Probe]:
        for probe in self.probes:
            if probe.id == probe_id:
                return probe

        return None

    def get_categories(self) -> List[str]:
        return sorted(
            set(probe.category for probe in self.probes)
        )