from adapters.mock_adapter import MockLLMAdapter
from probes.manager import ProbeManager
from evaluator.engine import EvaluationEngine

from reports.metrics import calculate_metrics
from reports.exporter import export_json, export_csv


def main():
    # --------------------------------------------------
    # 1. Initialize the adapter, probe manager, and engine
    # --------------------------------------------------

    adapter = MockLLMAdapter()
    probe_manager = ProbeManager()
    engine = EvaluationEngine(adapter)

    # --------------------------------------------------
    # 2. Load all available probes
    # --------------------------------------------------

    probes = probe_manager.get_all_probes()

    print("=" * 60)
    print("LLM RED-TEAM EVALUATION")
    print("=" * 60)
    print(f"Total probes loaded: {len(probes)}")

    # --------------------------------------------------
    # 3. Run the evaluation
    # --------------------------------------------------

    results = engine.evaluate(probes)

    # --------------------------------------------------
    # 4. Calculate evaluation metrics
    # --------------------------------------------------

    metrics = calculate_metrics(results)

    # --------------------------------------------------
    # 5. Display the overall evaluation summary
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    print(f"Total tests: {metrics['total_tests']}")
    print(f"Passed: {metrics['passed']}")
    print(f"Failed: {metrics['failed']}")
    print(f"Uncertain: {metrics['uncertain']}")

    print(f"Pass rate: {metrics['pass_rate']}%")
    print(f"Failure rate: {metrics['failure_rate']}%")
    print(f"Uncertain rate: {metrics['uncertain_rate']}%")

    print(
        f"Average risk score: "
        f"{metrics['average_risk_score']}"
    )

    # --------------------------------------------------
    # 6. Display category-wise metrics
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("CATEGORY-WISE METRICS")
    print("=" * 60)

    for category, category_data in metrics[
        "category_metrics"
    ].items():

        print(f"\nCategory: {category}")
        print(f"  Total: {category_data['total']}")
        print(f"  Passed: {category_data['passed']}")
        print(f"  Failed: {category_data['failed']}")
        print(f"  Uncertain: {category_data['uncertain']}")
        print(f"  Pass rate: {category_data['pass_rate']}%")
        print(
            f"  Failure rate: "
            f"{category_data['failure_rate']}%"
        )
        print(
            f"  Uncertain rate: "
            f"{category_data['uncertain_rate']}%"
        )

    # --------------------------------------------------
    # 7. Display severity distribution
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("SEVERITY DISTRIBUTION")
    print("=" * 60)

    for severity, count in metrics[
        "severity_distribution"
    ].items():
        print(f"{severity}: {count}")

    # --------------------------------------------------
    # 8. Display failed tests by severity
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("FAILED TESTS BY SEVERITY")
    print("=" * 60)

    if metrics["failed_by_severity"]:
        for severity, count in metrics[
            "failed_by_severity"
        ].items():
            print(f"{severity}: {count}")
    else:
        print("No failed tests detected.")

    # --------------------------------------------------
    # 9. Display risk-level distribution
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("RISK LEVEL DISTRIBUTION")
    print("=" * 60)

    for risk_level, count in metrics[
        "risk_level_distribution"
    ].items():
        print(f"{risk_level}: {count}")

    # --------------------------------------------------
    # 10. Display individual result risk scores
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("INDIVIDUAL RISK SCORES")
    print("=" * 60)

    for result in results:
        print(
            f"{result.probe_id} | "
            f"Category: {result.category} | "
            f"Status: {result.status} | "
            f"Severity: {result.severity} | "
            f"Risk Score: {result.risk_score} | "
            f"Risk Level: {result.risk_level}"
        )

    # --------------------------------------------------
    # 11. Export reports
    # --------------------------------------------------

    json_path = export_json(
        results=results,
        metrics=metrics,
        output_path="reports/output/evaluation_report.json",
    )

    csv_path = export_csv(
        results=results,
        output_path="reports/output/evaluation_results.csv",
    )

    # --------------------------------------------------
    # 12. Display export locations
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("REPORTS GENERATED SUCCESSFULLY")
    print("=" * 60)

    print(f"JSON report: {json_path}")
    print(f"CSV report: {csv_path}")


if __name__ == "__main__":
    main()