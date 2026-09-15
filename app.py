from datetime import datetime
import os
from pathlib import Path
import json
from urllib.parse import urlparse

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)

from adapters.mock_adapter import MockLLMAdapter
from adapters.ollama_adapter import OllamaAdapter
from evaluator.engine import EvaluationEngine
from probes.manager import ProbeManager
from reports.exporter import export_csv, export_report_json
from reports.metrics import calculate_metrics

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "llm-redteam-evaluator-dev")

REPORT_PATH = Path("reports/output/ollama_evaluation_report.json")
CSV_REPORT_PATH = Path("reports/output/ollama_evaluation_results.csv")
RUNS_DIR = Path("reports/output/runs")


@app.route("/", methods=["GET"])
def dashboard():
    has_report = REPORT_PATH.exists()
    show_report = session.pop("show_report_once", False)
    if has_report and show_report:
        results, metrics, metadata = load_report()
    else:
        results, metrics, metadata = [], empty_metrics(), {}

    return render_template(
        "index.html",
        results=results,
        metrics=metrics,
        metadata=metadata,
        has_json_report=has_report,
        has_csv_report=CSV_REPORT_PATH.exists(),
        last_updated=get_last_updated() if has_report else None,
    )

@app.route("/run-evaluation", methods=["POST"])
def run_evaluation():
    adapter_type = request.form.get("adapter", "mock")
    model_name = request.form.get("model_name", "qwen2.5:3b").strip()
    base_url = request.form.get("base_url", "http://localhost:11434").strip()

    try:
        if adapter_type == "ollama":
            validate_local_ollama_url(base_url)
            adapter = OllamaAdapter(
                model_name=model_name or "qwen2.5:3b",
                base_url=base_url or "http://localhost:11434",
            )
        else:
            adapter = MockLLMAdapter()

        probe_manager = ProbeManager()
        engine = EvaluationEngine(adapter)
        results = engine.evaluate(probe_manager.get_all_probes())

        output_dir = REPORT_PATH.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        RUNS_DIR.mkdir(parents=True, exist_ok=True)

        report_json = export_report_json(
            results,
            adapter=adapter_type,
            model_name=model_name if adapter_type == "ollama" else None,
        )

        REPORT_PATH.write_text(
            report_json,
            encoding="utf-8",
        )

        CSV_REPORT_PATH.write_text(
            export_csv(results),
            encoding="utf-8",
            newline="",
        )

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        run_report_path = RUNS_DIR / f"evaluation-{timestamp}.json"
        run_report_path.write_text(report_json, encoding="utf-8")

        flash(
            f"Evaluation completed with {len(results)} probes using {adapter_type}.",
            "success",
        )
        session["show_report_once"] = True

    except Exception as error:
        flash(f"Evaluation failed: {error}", "error")

    return redirect(url_for("dashboard"))


@app.route("/clear-results", methods=["POST"])
def clear_results():
    session.pop("show_report_once", None)

    for path in (REPORT_PATH, CSV_REPORT_PATH):
        if path.exists():
            path.unlink()

    flash("Dashboard results cleared.", "success")
    return redirect(url_for("dashboard"))


@app.route("/download/<file_type>", methods=["GET"])
def download_report(file_type):
    if file_type == "json" and REPORT_PATH.exists():
        return send_file(REPORT_PATH, as_attachment=True)

    if file_type == "csv" and CSV_REPORT_PATH.exists():
        return send_file(CSV_REPORT_PATH, as_attachment=True)

    flash("Requested report file does not exist yet.", "error")
    return redirect(url_for("dashboard"))


def load_report():
    if not REPORT_PATH.exists():
        return [], empty_metrics(), {}

    try:
        data = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        flash("The saved JSON report could not be parsed.", "error")
        return [], empty_metrics(), {}

    if isinstance(data, dict):
        results = data.get("results", [])
        metrics = data.get("metrics") or calculate_metrics_from_dicts(results)
        metadata = data.get("metadata", {})
        return results, normalize_metrics(metrics), metadata

    if isinstance(data, list):
        return data, calculate_metrics_from_dicts(data), {}

    return [], empty_metrics(), {}


def calculate_metrics_from_dicts(results):
    class MetricResult:
        def __init__(self, result):
            self.status = result.get("status", "UNCERTAIN")
            self.category = result.get("category", "unknown")
            self.severity = result.get("severity", "low")
            self.risk_level = result.get("risk_level", "LOW")

    return calculate_metrics([MetricResult(result) for result in results])


def normalize_metrics(metrics):
    defaults = empty_metrics()
    defaults.update(metrics or {})
    return defaults


def empty_metrics():
    return {
        "total_probes": 0,
        "passed": 0,
        "failed": 0,
        "uncertain": 0,
        "pass_rate": 0,
        "failure_rate": 0,
        "status_distribution": {},
        "category_distribution": {},
        "severity_distribution": {},
        "risk_distribution": {},
    }


def get_last_updated():
    if not REPORT_PATH.exists():
        return None

    modified_at = REPORT_PATH.stat().st_mtime

    return datetime.fromtimestamp(modified_at).strftime("%Y-%m-%d %H:%M:%S")


def validate_local_ollama_url(base_url):
    parsed = urlparse(base_url or "http://localhost:11434")
    allowed_hosts = {"localhost", "127.0.0.1", "::1"}

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Ollama base URL must use http or https.")

    if parsed.hostname not in allowed_hosts:
        raise ValueError("Ollama base URL must point to localhost.")


if __name__ == "__main__":
    app.run(
        host=os.environ.get("FLASK_HOST", "127.0.0.1"),
        port=int(os.environ.get("FLASK_PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "0") == "1",
    )
