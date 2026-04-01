import requests
import streamlit as st


def ask_llm(prompt):
    """
    Sends a prompt to Groq LLM API and returns response.
    Safe for deployment with error handling.
    """

    try:
        # 🔐 Get API key securely
        api_key = st.secrets.get("GROQ_API_KEY")

        if not api_key:
            return "⚠️ LLM API key not found. Using fallback logic."

        # 🌐 API endpoint
        url = "https://api.groq.com/openai/v1/chat/completions"

        # 📡 Headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # 🧠 Request body
        data = {
            "model": "llama3-70b-8192",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful data analyst. Answer clearly and concisely."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3
        }

        # 🚀 Send request
        response = requests.post(url, headers=headers, json=data, timeout=30)

        # ❌ Handle bad response
        if response.status_code != 200:
            return f"⚠️ LLM error: {response.status_code}"

        result = response.json()

        # ✅ Extract response safely
        return result["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        return "⚠️ LLM request timed out. Try again."

    except requests.exceptions.RequestException as e:
        return f"⚠️ Network error: {str(e)}"

    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"