import streamlit as st

from adapters.mock_adapter import MockLLMAdapter
from evaluator.engine import EvaluationEngine
from probes.manager import ProbeManager
from reports.metrics import calculate_metrics


st.set_page_config(
    page_title="LLM Red-Team Tester",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ LLM Red-Team & Jailbreak Vulnerability Tester")

st.write(
    """
    An authorized testing platform for evaluating LLM behavior against
    jailbreak, prompt-injection, and system-prompt-leakage probes.
    """
)

st.warning(
    "Use this demo only for models and applications that you are authorized to test."
)

adapter_type = st.selectbox(
    "Select evaluation mode",
    ["Mock LLM Demo"],
)

if st.button("Run Red-Team Evaluation"):
    with st.spinner("Running security probes..."):
        adapter = MockLLMAdapter()
        probe_manager = ProbeManager()
        probes = probe_manager.get_all_probes()

        engine = EvaluationEngine(adapter)
        results = engine.evaluate(probes)
        metrics = calculate_metrics(results)

    st.success("Evaluation completed successfully.")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Tests", metrics["total_tests"])
    col2.metric("Passed", metrics["passed"])
    col3.metric("Failed", metrics["failed"])
    col4.metric("Uncertain", metrics["uncertain"])

    st.subheader("Evaluation Summary")

    st.write({
        "Pass Rate": f'{metrics["pass_rate"]}%',
        "Failure Rate": f'{metrics["failure_rate"]}%',
        "Average Risk Score": metrics["average_risk_score"],
    })

    st.subheader("Probe Results")

    table_data = []

    for result in results:
        table_data.append(
            {
                "Probe ID": result.probe_id,
                "Category": result.category,
                "Status": result.status,
                "Severity": result.severity,
                "Risk Score": result.risk_score,
                "Risk Level": result.risk_level,
                "Reason": result.reason,
            }
        )

    st.dataframe(table_data, use_container_width=True)

    st.subheader("Detailed Responses")

    for result in results:
        with st.expander(f"{result.probe_id} — {result.status}"):
            st.write("**Category:**", result.category)
            st.write("**Prompt:**", result.prompt)
            st.write("**Model Response:**", result.response)
            st.write("**Reason:**", result.reason)
            st.write("**Risk Score:**", result.risk_score)
            st.write("**Risk Level:**", result.risk_level)