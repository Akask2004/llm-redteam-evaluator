from adapters.mock_adapter import MockLLMAdapter
from probes.manager import ProbeManager
from evaluator.engine import EvaluationEngine


def main():

    # Initialize the target model
    adapter = MockLLMAdapter()

    # Load probes
    probe_manager = ProbeManager()

    probes = probe_manager.get_all_probes()

    # Create evaluation engine
    engine = EvaluationEngine(adapter)

    # Run evaluation
    results = engine.evaluate(probes)

    print("\n" + "=" * 50)
    print("EVALUATION RESULTS")
    print("=" * 50)

    for result in results:

        print(f"\nProbe ID: {result.probe_id}")
        print(f"Category: {result.category}")
        print(f"Status: {result.status}")
        print(f"Reason: {result.reason}")
        print(f"Response: {result.response}")


if __name__ == "__main__":
    main()