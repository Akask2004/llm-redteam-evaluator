import json

import app as app_module


def test_dashboard_loads_without_report(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "REPORT_PATH", tmp_path / "missing.json")
    monkeypatch.setattr(app_module, "CSV_REPORT_PATH", tmp_path / "missing.csv")
    monkeypatch.setattr(app_module, "RUNS_DIR", tmp_path / "runs")

    client = app_module.app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"No Results Yet" in response.data


def test_mock_evaluation_generates_reports(tmp_path, monkeypatch):
    report_path = tmp_path / "report.json"
    csv_path = tmp_path / "report.csv"

    monkeypatch.setattr(app_module, "REPORT_PATH", report_path)
    monkeypatch.setattr(app_module, "CSV_REPORT_PATH", csv_path)
    monkeypatch.setattr(app_module, "RUNS_DIR", tmp_path / "runs")

    client = app_module.app.test_client()
    response = client.post(
        "/run-evaluation",
        data={"adapter": "mock"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert report_path.exists()
    assert csv_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["metadata"]["adapter"] == "mock"
    assert report["metrics"]["total_probes"] > 0
    assert report["results"]

    refresh_response = client.get("/")
    assert b"No Results Yet" in refresh_response.data


def test_clear_results_removes_latest_reports(tmp_path, monkeypatch):
    report_path = tmp_path / "report.json"
    csv_path = tmp_path / "report.csv"
    report_path.write_text("{}", encoding="utf-8")
    csv_path.write_text("probe_id\n", encoding="utf-8")

    monkeypatch.setattr(app_module, "REPORT_PATH", report_path)
    monkeypatch.setattr(app_module, "CSV_REPORT_PATH", csv_path)
    monkeypatch.setattr(app_module, "RUNS_DIR", tmp_path / "runs")

    client = app_module.app.test_client()
    response = client.post("/clear-results", follow_redirects=True)

    assert response.status_code == 200
    assert not report_path.exists()
    assert not csv_path.exists()
