import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
sys.path.append(os.getcwd())

from main import run_pipeline
from scheduler import start_scheduler, stop_scheduler, get_scheduler_status
from tools.insights import generate_insights
from tools.chat_agent import answer_question

st.set_page_config(page_title="AI Data Platform", layout="wide")

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("AI Data Platform")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Data Preview", "AI Assistant", "Scheduler"]
)

# Session
if "data" not in st.session_state:
    st.session_state.data = None
    st.session_state.anomalies = None

# Upload
st.sidebar.subheader("Upload Data")
uploaded_file = st.sidebar.file_uploader("CSV", type=["csv"])

file_path = None

if uploaded_file:
    file_path = "data/uploaded.csv"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

# Run Pipeline
if st.sidebar.button("Run Pipeline") and file_path:
    df, anomalies = run_pipeline(file_path)
    st.session_state.data = df
    st.session_state.anomalies = anomalies

df = st.session_state.data
anomalies = st.session_state.anomalies

# -------------------------------
# DASHBOARD PAGE
# -------------------------------
if page == "Dashboard":

    st.title("Dashboard")

    if df is not None:

        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing", df.isnull().sum().sum())

        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

        if len(numeric_cols) > 0:
            col = st.selectbox("Select column", numeric_cols)

            col1, col2 = st.columns(2)

            with col1:
                st.plotly_chart(px.histogram(df, x=col))

            with col2:
                st.plotly_chart(px.box(df, y=col))

        st.subheader("AI Insights")

        for ins in generate_insights(df):
            st.info(ins)

    else:
        st.warning("Upload and run pipeline")

# -------------------------------
# DATA PREVIEW PAGE
# -------------------------------
elif page == "Data Preview":

    st.title("Data Preview")

    if df is not None:
        st.dataframe(df.head(200))

        if anomalies is not None:
            st.subheader("Anomalies")
            st.dataframe(anomalies.head(50))

    else:
        st.warning("No data available")

# -------------------------------
# AI ASSISTANT PAGE
# -------------------------------
elif page == "AI Assistant":

    st.title("Ask Your Data")

    if df is not None:

        question = st.text_input("Ask a question about your dataset")

        if st.button("Ask"):
            answer = answer_question(df, question)
            st.success(answer)

    else:
        st.warning("Upload data first")

# -------------------------------
# SCHEDULER PAGE
# -------------------------------
elif page == "Scheduler":

    st.title("Scheduler")

    minutes = st.number_input("Run every (minutes)", 1, 60, 1)

    if st.button("Start"):
        if file_path:
            start_scheduler(file_path, minutes)
            st.success("Scheduler started")

    if st.button("Stop"):
        stop_scheduler()
        st.warning("Stopped")

    st.write("Running:", get_scheduler_status())