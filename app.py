import streamlit as st
from main import run_pipeline

st.title("🤖 Autonomous Data Pipeline Agent")

st.write("Upload CSV or enter file path")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    with open("data/uploaded.csv", "wb") as f:
        f.write(uploaded_file.read())

    if st.button("Run Pipeline"):
        df = run_pipeline("data/uploaded.csv")
        st.success("Pipeline Completed!")
        st.dataframe(df)

file_path = st.text_input("Or enter file path")

if st.button("Run Pipeline from Path"):
    df = run_pipeline(file_path)
    st.success("Pipeline Completed!")
    st.dataframe(df)