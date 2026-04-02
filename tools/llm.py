from groq import Groq
import streamlit as st


def ask_llm(prompt, df=None):
    """
    Sends a prompt to Groq LLM with optional dataset context
    """

    try:
        # 🔐 Get API key securely
        api_key = st.secrets.get("GROQ_API_KEY")

        if not api_key:
            return "⚠️ GROQ_API_KEY not found in Streamlit secrets."

        client = Groq(api_key=api_key)

        # 📊 Add dataset context (VERY IMPORTANT FOR SMART AI)
        data_context = ""

        if df is not None:
            try:
                data_context = f"""
Dataset Info:
- Rows: {df.shape[0]}
- Columns: {df.shape[1]}
- Column Names: {list(df.columns)}

Sample Data:
{df.head(5).to_string()}
"""
            except Exception:
                data_context = ""

        # 🧠 Final prompt (context + user question)
        final_prompt = f"""
You are a data analyst AI.

{data_context}

User Question:
{prompt}

Instructions:
- Be clear and concise
- Use data context if available
- If question is general, explain dataset
"""

        # 🚀 LLM CALL (FIXED MODEL)
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": final_prompt}
            ],
            model="llama3-70b-8192",  # ✅ UPDATED MODEL
            temperature=0.7,
            max_tokens=1024
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ LLM error: {str(e)}"