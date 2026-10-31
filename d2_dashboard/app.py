import streamlit as st
import pandas as pd
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs.jsonl"
RESULTS = ROOT / "results.csv"

st.set_page_config(
    page_title="SDN Log Monitoring Dashboard",
    page_icon="📡",
    layout="wide"
)

st.title("📡 SDN Log Monitoring Dashboard")
st.caption("Distributed Log Aggregation System | UDP + Mininet + SDN")


def read_logs():
    records = []

    if LOGS.exists():
        with open(LOGS, "r", encoding="utf-8", errors="replace") as file:
            for line in file:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    return pd.DataFrame(records)


def read_results():
    if RESULTS.exists():
        try:
            return pd.read_csv(RESULTS)
        except Exception:
            pass

    return pd.DataFrame()


logs = read_logs()
results = read_results()

if not logs.empty and "severity" in logs.columns:
    critical_count = int(
        (logs["severity"].astype(str).str.upper() == "CRITICAL").sum()
    )
else:
    critical_count = 0

normal_count = len(logs) - critical_count

col1, col2, col3 = st.columns(3)
col1.metric("Logs collected", len(logs))
col2.metric("Critical logs", critical_count)
col3.metric("Other logs", normal_count)

st.subheader("🚨 Critical alerts")

if not logs.empty and "severity" in logs.columns:
    critical_logs = logs[
        logs["severity"].astype(str).str.upper() == "CRITICAL"
    ]

    if not critical_logs.empty:
        st.dataframe(critical_logs, use_container_width=True)
    else:
        st.success("No critical logs found.")
else:
    st.info("Waiting for log data from the UDP server.")

st.subheader("📋 Recent logs")

if not logs.empty:
    st.dataframe(logs.tail(100).iloc[::-1], use_container_width=True)
else:
    st.info("No logs recorded yet. Start the UDP server and send logs.")

st.subheader("📈 Congestion experiment results")

if not results.empty:
    results = results.copy()
    results["test"] = (
        results["traffic_class"].astype(str)
        + " - "
        + results["mode"].astype(str)
    )

    st.dataframe(results, use_container_width=True)

    if "delivery_rate_pct" in results.columns:
        st.markdown("**Delivery rate (%)**")
        st.bar_chart(
            results.set_index("test")[["delivery_rate_pct"]]
        )

    if "packet_loss_pct" in results.columns:
        st.markdown("**Packet loss (%)**")
        st.bar_chart(
            results.set_index("test")[["packet_loss_pct"]]
        )
else:
    st.info("No experiment results are available yet.")

st.caption("Refresh the page to view newly collected logs and results.")
