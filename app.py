import streamlit as st
import pandas as pd

from adapters.mock_adapter import MockLLMAdapter
from evaluator.engine import EvaluationEngine
from probes.manager import ProbeManager
from reports.metrics import calculate_metrics


st.set_page_config(
    page_title="LLM Red-Team Evaluator",
    page_icon="🛡️",
    layout="wide",
)


st.title("🛡️ LLM Evaluation & Red-Teaming Dashboard")
st.write(
    "Evaluate model responses against jailbreak, prompt-injection, "
    "and system-prompt leakage probes."
)


# Sidebar
st.sidebar.header("Evaluation Settings")

adapter_type = st.sidebar.selectbox(
    "Select Model Adapter",
    ["Mock LLM"],
)

run_evaluation = st.sidebar.button("Run Evaluation")


if run_evaluation:
    with st.spinner("Running evaluation..."):
        adapter = MockLLMAdapter()
        engine = EvaluationEngine(adapter)
        probe_manager = ProbeManager()

        probes = probe_manager.get_all_probes()
        results = engine.evaluate(probes)

        metrics = calculate_metrics(results)

        st.session_state["results"] = results
        st.session_state["metrics"] = metrics


if "results" in st.session_state:
    results = st.session_state["results"]
    metrics = st.session_state["metrics"]

    st.subheader("Evaluation Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Probes", metrics["total_probes"])
    col2.metric("Passed", metrics["passed"])
    col3.metric("Failed", metrics["failed"])
    col4.metric("Uncertain", metrics["uncertain"])

    st.subheader("Performance Metrics")

    metric_col1, metric_col2 = st.columns(2)

    metric_col1.metric(
        "Pass Rate",
        f"{metrics['pass_rate']}%",
    )

    metric_col2.metric(
        "Failure Rate",
        f"{metrics['failure_rate']}%",
    )

    st.subheader("Risk Distribution")

    risk_distribution = metrics["risk_distribution"]

    if risk_distribution:
        risk_df = pd.DataFrame(
            list(risk_distribution.items()),
            columns=["Risk Level", "Count"],
        )

        st.bar_chart(
            risk_df.set_index("Risk Level")
        )

    st.subheader("Detailed Results")

    result_rows = []

    for result in results:
        result_rows.append(
            {
                "Probe ID": result.probe_id,
                "Category": result.category,
                "Status": result.status,
                "Severity": result.severity,
                "Risk Score": result.risk_score,
                "Risk Level": result.risk_level,
                "Confidence": result.confidence,
                "Review Required": result.review_required,
                "Reason": result.reason,
                "Response": result.response,
            }
        )

    results_df = pd.DataFrame(result_rows)

    st.dataframe(
        results_df,
        use_container_width=True,
    )

else:
    st.info("Click 'Run Evaluation' to start testing.")