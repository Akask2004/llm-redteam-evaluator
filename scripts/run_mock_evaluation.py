from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adapters.mock_adapter import MockLLMAdapter
from evaluator.engine import EvaluationEngine
from probes.manager import ProbeManager


def main():
    adapter = MockLLMAdapter()
    probe_manager = ProbeManager()
    engine = EvaluationEngine(adapter)
    results = engine.evaluate(probe_manager.get_all_probes())

    print("\n" + "=" * 50)
    print("EVALUATION RESULTS")
    print("=" * 50)

    for result in results:
        print(f"\nProbe ID: {result.probe_id}")
        print(f"Category: {result.category}")
        print(f"Status: {result.status}")
        print(f"Risk: {result.risk_level} ({result.risk_score})")
        print(f"Reason: {result.reason}")
        print(f"Response: {result.response}")


if __name__ == "__main__":
    main()
