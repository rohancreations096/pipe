import streamlit as st
import pandas as pd
import plotly.express as px

from main import run_pipeline
from scheduler import start_scheduler, stop_scheduler, get_scheduler_status

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Autonomous Data Pipeline Agent", layout="wide")

# -------------------------------
# Title
# -------------------------------
st.title("Autonomous Data Pipeline Agent")
st.write("Upload CSV or enter file path")

# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

file_path = None

if uploaded_file:
    file_path = "data/uploaded.csv"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

# -------------------------------
# File Path Input
# -------------------------------
st.subheader("Or enter file path")
file_path_input = st.text_input("Enter CSV file path")

if file_path_input:
    file_path = file_path_input

# -------------------------------
# Run Pipeline
# -------------------------------
if st.button("Run Pipeline") and file_path:

    with st.spinner("Running pipeline..."):
        df, anomalies = run_pipeline(file_path)

    if df is not None:

        st.success("Pipeline Completed")

        # -------------------------------
        # Dataset Summary
        # -------------------------------
        st.subheader("Dataset Summary")

        col1, col2 = st.columns(2)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])

        st.write("Columns:", df.columns.tolist())

        # -------------------------------
        # Preview
        # -------------------------------
        st.subheader("Data Preview (First 100 Rows)")
        st.dataframe(df.head(100))

        # -------------------------------
        # Visualization Dashboard
        # -------------------------------
        st.subheader("Data Visualization Dashboard")

        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

        if numeric_cols:
            selected_col = st.selectbox("Select column for analysis", numeric_cols)

            col1, col2 = st.columns(2)

            # Histogram
            with col1:
                fig = px.histogram(
                    df,
                    x=selected_col,
                    title="Distribution",
                    color_discrete_sequence=["blue"]
                )
                st.plotly_chart(fig, use_container_width=True)

            # Box Plot (Anomaly view)
            with col2:
                fig2 = px.box(
                    df,
                    y=selected_col,
                    title="Outlier Detection",
                    color_discrete_sequence=["red"]
                )
                st.plotly_chart(fig2, use_container_width=True)

        else:
            st.warning("No numeric columns available")

        # -------------------------------
        # Anomaly Detection
        # -------------------------------
        if anomalies is not None:

            st.subheader("Anomaly Detection Results")

            st.metric("Total Anomalies", len(anomalies))

            if not anomalies.empty:
                st.dataframe(anomalies.head(50))

                # Plot anomalies
                if numeric_cols:
                    fig3 = px.scatter(
                        df,
                        y=selected_col,
                        title="Anomaly Scatter Plot"
                    )
                    st.plotly_chart(fig3, use_container_width=True)

            else:
                st.success("No anomalies detected")

        # -------------------------------
        # Download
        # -------------------------------
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Processed Data",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv"
        )

    else:
        st.error("Pipeline failed. Check logs.")

# -------------------------------
# Scheduler UI
# -------------------------------
st.subheader("Schedule Pipeline")

schedule_minutes = st.number_input("Run every (minutes)", min_value=1, value=1)

if st.button("Start Scheduler") and file_path:
    start_scheduler(file_path, schedule_minutes)
    st.success(f"Pipeline scheduled every {schedule_minutes} minutes")

if st.button("Stop Scheduler"):
    stop_scheduler()
    st.warning("Scheduler stopped")

st.write("Scheduler running:", get_scheduler_status())