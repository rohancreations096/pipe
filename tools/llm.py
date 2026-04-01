import requests
import streamlit as st

def ask_llm(prompt):

    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        return "⚠️ API key missing in Streamlit secrets."

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        # 🔥 DEBUG (important)
        if response.status_code != 200:
            return f"⚠️ LLM error {response.status_code}: {response.text}"

        result = response.json()
        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"LLM Exception: {str(e)}"