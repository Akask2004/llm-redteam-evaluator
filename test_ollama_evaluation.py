from adapters.ollama_adapter import OllamaAdapter
from probes.manager import ProbeManager
from evaluator.engine import EvaluationEngine

from reports.metrics import calculate_metrics
from reports.exporter import export_json, export_csv


def main():
    # Initialize local Ollama model
    adapter = OllamaAdapter(
        model="qwen2.5:3b"
    )

    # Load probes
    probe_manager = ProbeManager()
    probes = probe_manager.get_all_probes()

    # Initialize evaluation engine
    engine = EvaluationEngine(adapter)

    # Run evaluation
    results = engine.evaluate(probes)

    # Calculate metrics
    metrics = calculate_metrics(results)

    # Display summary
    print("\n" + "=" * 60)
    print("OLLAMA LLM EVALUATION SUMMARY")
    print("=" * 60)

    print(f"Total tests: {metrics['total_tests']}")
    print(f"Passed: {metrics['passed']}")
    print(f"Failed: {metrics['failed']}")
    print(f"Uncertain: {metrics['uncertain']}")
    print(f"Pass rate: {metrics['pass_rate']}%")
    print(f"Failure rate: {metrics['failure_rate']}%")
    print(
        f"Average risk score: "
        f"{metrics['average_risk_score']}"
    )

    # Export reports
    json_path = export_json(
        results,
        metrics,
        "reports/output/ollama_evaluation_report.json",
    )

    csv_path = export_csv(
        results,
        "reports/output/ollama_evaluation_results.csv",
    )

    print("\nReports generated:")
    print(json_path)
    print(csv_path)


if __name__ == "__main__":
    main()