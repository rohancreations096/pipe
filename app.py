import streamlit as st
import pandas as pd
from main import run_pipeline

st.set_page_config(page_title="Autonomous Data Pipeline Agent", layout="wide")

st.title("🤖 Autonomous Data Pipeline Agent")

st.write("Upload CSV or enter file path")

# -------------------------------
# 📂 File Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    file_path = "data/uploaded.csv"

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    if st.button("Run Pipeline"):
        with st.spinner("Running pipeline..."):
            df = run_pipeline(file_path)

        if df is not None:
            st.success("✅ Pipeline Completed!")

            # -------------------------------
            # 📊 Dataset Info
            # -------------------------------
            st.subheader("📊 Dataset Summary")
            st.write("Shape:", df.shape)
            st.write("Columns:", df.columns.tolist())

            # -------------------------------
            # 🔍 Preview (SAFE DISPLAY)
            # -------------------------------
            st.subheader("🔍 Data Preview (First 100 Rows)")
            st.dataframe(df.head(100))

            # -------------------------------
            # ⬇ Download Full Data
            # -------------------------------
            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="⬇ Download Processed Data",
                data=csv,
                file_name="processed_data.csv",
                mime="text/csv",
            )

        else:
            st.error("❌ Pipeline failed. Check logs.")


# -------------------------------
# 📁 File Path Input
# -------------------------------
st.subheader("Or enter file path")

file_path_input = st.text_input("Enter CSV file path")

if st.button("Run Pipeline from Path"):
    with st.spinner("Running pipeline..."):
        df = run_pipeline(file_path_input)

    if df is not None:
        st.success("✅ Pipeline Completed!")

        st.subheader("📊 Dataset Summary")
        st.write("Shape:", df.shape)
        st.write("Columns:", df.columns.tolist())

        st.subheader("🔍 Data Preview (First 100 Rows)")
        st.dataframe(df.head(100))

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇ Download Processed Data",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv",
        )

    else:
        st.error("❌ Pipeline failed.")