import streamlit as st
import pandas as pd
import plotly.express as px
import os

from main import run_pipeline
from tools.chat_agent import answer_question
from tools.insights import generate_insights

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="AI Data Platform", layout="wide")

# Fix imports (IMPORTANT for deployment)
import sys
sys.path.append(os.getcwd())

# -------------------------------
# TITLE
# -------------------------------
st.title("🚀 Autonomous AI Data Platform")

# -------------------------------
# SESSION STATE
# -------------------------------
if "data" not in st.session_state:
    st.session_state.data = None

if "logs" not in st.session_state:
    st.session_state.logs = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("Controls")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Data Preview", "AI Assistant"]
)

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

auto_mode = st.sidebar.checkbox("🤖 Autonomous Mode")

# -------------------------------
# FILE HANDLING
# -------------------------------
if uploaded_file:
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", "uploaded.csv")

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.sidebar.success("File uploaded")

    if st.sidebar.button("⚙️ Run Pipeline"):

        with st.spinner("Running agent..."):

            if auto_mode:
                attempts = 0
                while attempts < 3:
                    df, logs = run_pipeline(file_path)

                    if df.isnull().sum().sum() == 0:
                        break

                    attempts += 1
            else:
                df, logs = run_pipeline(file_path)

            st.session_state.data = df
            st.session_state.logs = logs

        st.sidebar.success("Pipeline complete")

# -------------------------------
# DASHBOARD
# -------------------------------
if page == "Dashboard":

    st.header("📊 Dashboard")

    if st.session_state.data is not None:
        df = st.session_state.data

        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing", int(df.isnull().sum().sum()))

        st.divider()

        # Visualization
        st.subheader("📈 Visualization")

        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

        if len(numeric_cols) > 0:
            x = st.selectbox("X-axis", numeric_cols)
            y = st.selectbox("Y-axis", numeric_cols)

            fig = px.scatter(df, x=x, y=y)
            st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # Agent Thinking
        st.subheader("🧠 Agent Thinking")

        if st.session_state.logs:
            for log in st.session_state.logs:
                st.write(f"➡️ {log}")

        st.divider()

        # AI Insights
        st.subheader("🧠 AI Insights")

        if st.button("Generate Insights"):
            with st.spinner("Analyzing..."):
                insights = generate_insights(df)
                st.success("Insights Generated")
                st.write(insights)

        # Explain pipeline
        if st.button("Explain Pipeline"):
            explanation = answer_question(
                df,
                "Explain what processing was done on this dataset"
            )
            st.write(explanation)

    else:
        st.info("Upload and run pipeline first")

# -------------------------------
# DATA PREVIEW
# -------------------------------
elif page == "Data Preview":

    st.header("📄 Data Preview")

    if st.session_state.data is not None:
        st.dataframe(st.session_state.data)

# -------------------------------
# AI ASSISTANT (WITH MEMORY)
# -------------------------------
elif page == "AI Assistant":

    st.header("🤖 AI Chat Assistant")

    if st.session_state.data is not None:

        user_input = st.text_input("Ask something about your data")

        if st.button("Ask"):

            with st.spinner("Thinking..."):

                history = "\n".join(st.session_state.chat_history)

                full_prompt = f"""
                Previous conversation:
                {history}

                New question:
                {user_input}
                """

                answer = answer_question(st.session_state.data, full_prompt)

                st.session_state.chat_history.append(f"User: {user_input}")
                st.session_state.chat_history.append(f"AI: {answer}")

                st.success(answer)

        st.subheader("💬 Chat History")

        for msg in st.session_state.chat_history[-6:]:
            st.write(msg)

    else:
        st.info("Upload dataset first")