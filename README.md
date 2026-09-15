# LLM Red-Team Evaluator

A small Flask-based dashboard and evaluation engine for testing model responses
against authorized jailbreak, prompt-injection, and system-prompt-leakage probes.

The project is intentionally simple: probes are plain Python objects, adapters
call a target model, the evaluator classifies responses with deterministic
rules, and reports are exported as JSON and CSV.

## Features

- Jailbreak, prompt-injection, and system-prompt-leakage probes
- Mock adapter for instant local demos and tests
- Ollama adapter for local model evaluation
- PASS, FAIL, and UNCERTAIN response classification
- Severity-based risk scoring
- Per-probe latency and error recording
- JSON and CSV report export
- Flask dashboard with downloadable reports

## Project Layout

```text
.
|-- adapters/          # Model adapters: mock and Ollama
|-- evaluator/         # Evaluation engine, checker, risk scoring, result models
|-- probes/            # Probe definitions and probe manager
|-- reports/           # Metrics and report exporters
|-- scripts/           # Manual CLI helpers and demo runs
|-- static/            # Flask CSS
|-- templates/         # Flask HTML templates
|-- tests/             # Automated pytest suite
|-- app.py             # Flask dashboard entry point
`-- requirements.txt   # Runtime and test dependencies
```

Generated reports are written to `reports/output/`, which is ignored by Git.

## Setup

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS or Linux, activate the environment with:

```bash
source .venv/bin/activate
```

## Run the Dashboard

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

The dashboard supports two run modes:

- `Mock demo`: deterministic local responses, useful for testing the UI.
- `Ollama`: sends probes to a locally running Ollama server.

By design, dashboard results are shown once after a run. Refreshing the page
returns the dashboard to an empty state. Use the JSON/CSV buttons immediately
after a run if you want to download the latest report.

## Run with Ollama

Start Ollama locally and make sure the model exists:

```bash
ollama pull qwen2.5:3b
ollama serve
```

Then choose `Ollama` in the dashboard and run the evaluation.

You can also run the CLI helper:

```bash
python scripts/run_ollama_evaluation.py
```

## Useful Scripts

```bash
python scripts/inspect_probes.py
python scripts/run_mock_adapter.py
python scripts/run_mock_evaluation.py
python scripts/run_ollama_evaluation.py
```

## Run Tests

```bash
python -m pytest -v
```

## Configuration

The Flask secret key can be set with:

```bash
set FLASK_SECRET_KEY=your-secret-value
```

PowerShell users can set it for the current session with:

```powershell
$env:FLASK_SECRET_KEY = "your-secret-value"
```

If unset, the app uses a local development fallback.

## Ethical Use

Use this tool only for authorized safety testing of models and systems you own
or have permission to evaluate.
