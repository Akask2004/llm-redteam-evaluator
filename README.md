# 🛡️ LLM Red-Team Evaluator

A small Flask-based dashboard and evaluation engine for testing model responses against authorized **jailbreak, prompt-injection, and system-prompt-leakage probes**.

The project is intentionally simple: probes are plain Python objects, adapters call a target model, the evaluator classifies responses using deterministic rules, and reports are exported as **JSON and CSV**.

## 🚀 Live Demo

👉 **https://llm-redteam-evaluator.onrender.com/**

> The live demo uses the **Mock Adapter** for instant evaluation without requiring a locally running LLM.

## ✨ Features

* Jailbreak, prompt-injection, and system-prompt-leakage probes
* Mock adapter for instant demos and tests
* Ollama adapter for local LLM evaluation
* `PASS`, `FAIL`, and `UNCERTAIN` response classification
* Severity-based risk scoring
* Per-probe latency and error recording
* JSON and CSV report export
* Flask dashboard with downloadable reports
* Automated testing with Pytest

## 🏗️ Project Layout

```text
.
|-- adapters/          # Model adapters: Mock and Ollama
|-- evaluator/         # Evaluation engine, checker, risk scoring, result models
|-- probes/            # Probe definitions and probe manager
|-- reports/           # Metrics and report exporters
|-- scripts/           # CLI helpers and demo runs
|-- static/            # Flask CSS
|-- templates/         # Flask HTML templates
|-- tests/             # Automated pytest suite
|-- app.py             # Flask dashboard entry point
|-- render.yaml        # Render deployment configuration
|-- requirements.txt   # Runtime dependencies
`-- requirements-dev.txt # Development and test dependencies
```

Generated reports are written to `reports/output/`, which is ignored by Git.

## ⚙️ Setup

Clone the repository:

```bash
git clone https://github.com/Akask2004/llm-redteam-evaluator.git
cd llm-redteam-evaluator
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows

```powershell
.\.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements-dev.txt
```

## 🖥️ Run the Dashboard

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

The dashboard supports two run modes:

### Mock Demo

Uses deterministic local responses and is useful for:

* Testing the dashboard
* Demonstrating the evaluation workflow
* Running tests without an external LLM

### Ollama

Sends probes to a locally running Ollama model for actual model evaluation.

## 🤖 Run with Ollama

Install and start Ollama, then pull a model:

```bash
ollama pull qwen2.5:3b
ollama serve
```

Select **Ollama** in the dashboard and run the evaluation.

You can also use:

```bash
python scripts/run_ollama_evaluation.py
```

> **Note:** Ollama mode is intended for local use. The public Render deployment uses Mock mode because a deployed application cannot directly access Ollama running on your personal computer.

## 🧪 Run Tests

```bash
python -m pytest -v
```

## 📊 Evaluation Workflow

```text
Security Probe
      ↓
LLM Adapter
      ↓
Model Response
      ↓
Response Checker
      ↓
PASS / FAIL / UNCERTAIN
      ↓
Risk Scoring
      ↓
JSON / CSV Report
      ↓
Flask Dashboard
```

## 🔐 Configuration

Set the Flask secret key using an environment variable.

### PowerShell

```powershell
$env:FLASK_SECRET_KEY = "your-secret-value"
```

### Windows CMD

```cmd
set FLASK_SECRET_KEY=your-secret-value
```

For local development, the application has a fallback value if the variable is not set.

## 🛠️ Tech Stack

* **Python**
* **Flask**
* **Ollama**
* **Pytest**
* **HTML / CSS / JavaScript**
* **JSON / CSV**
* **Gunicorn**
* **Render**

## 🔐 Ethical Use

Use this tool only for **authorized safety testing** of models and systems that you own or have explicit permission to evaluate.

This project is intended for educational purposes, AI safety research, and authorized LLM red-team testing.

## 👨‍💻 Author

**Akash Dutta**

Interested in **LLM Security, Red Teaming, Jailbreak Testing, Prompt Injection, AI Safety, and LLM Evaluation**.

### 🔗 Links

**Live Demo:**
https://llm-redteam-evaluator.onrender.com/

**GitHub:**
https://github.com/Akask2004/llm-redteam-evaluator
