import requests
import streamlit as st

def ask_llm(prompt):

    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        return "No API key configured."

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=data)
        return res.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"LLM Error: {str(e)}"