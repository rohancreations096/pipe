from groq import Groq
import streamlit as st


def ask_llm(prompt, df=None):
    try:
        api_key = st.secrets.get("GROQ_API_KEY")

        if not api_key:
            return "⚠️ GROQ_API_KEY not found."

        client = Groq(api_key=api_key)

        # Dataset context
        context = ""
        if df is not None:
            context = f"""
Dataset:
Rows: {df.shape[0]}
Columns: {df.shape[1]}
Columns List: {list(df.columns)}

Sample:
{df.head(5).to_string()}
"""

        final_prompt = f"""
You are an expert data analyst.

{context}

User Question:
{prompt}

Give clear, useful insights.
"""

        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": final_prompt}
            ],
            model="llama-3.1-70b-versatile",  # ✅ FINAL FIX
            temperature=0.7,
            max_tokens=1024
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ LLM error: {str(e)}"