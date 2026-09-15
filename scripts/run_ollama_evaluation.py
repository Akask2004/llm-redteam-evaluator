from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adapters.ollama_adapter import OllamaAdapter
from evaluator.engine import EvaluationEngine
from probes.manager import ProbeManager
from reports.exporter import export_csv, export_report_json


def main():
    adapter_name = "ollama"
    model_name = "qwen2.5:3b"
    adapter = OllamaAdapter(model_name=model_name)

    probe_manager = ProbeManager()
    engine = EvaluationEngine(adapter)
    results = engine.evaluate(probe_manager.get_all_probes())

    output_dir = Path("reports/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "ollama_evaluation_report.json"
    csv_path = output_dir / "ollama_evaluation_results.csv"

    json_path.write_text(
        export_report_json(
            results,
            adapter=adapter_name,
            model_name=model_name,
        ),
        encoding="utf-8",
    )
    csv_path.write_text(
        export_csv(results),
        encoding="utf-8",
        newline="",
    )

    print("\nReports generated:")
    print(json_path)
    print(csv_path)


if __name__ == "__main__":
    main()
