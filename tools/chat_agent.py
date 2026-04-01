from tools.llm import ask_llm

def answer_question(df, question):
    question_lower = question.lower()

    try:
        # 🔹 Rule-based logic
        if "rows" in question_lower:
            return f"The dataset has {df.shape[0]} rows."

        if "columns" in question_lower:
            return f"The dataset has {df.shape[1]} columns."

        if "missing" in question_lower or "null" in question_lower:
            return f"Total missing values: {df.isnull().sum().sum()}"

        if "mean" in question_lower or "average" in question_lower:
            numeric = df.select_dtypes(include=['int64', 'float64'])
            if numeric.empty:
                return "No numeric columns found."
            return "Mean values:\n" + numeric.mean().to_string()

        # 🔥 FORCE LLM FALLBACK (THIS WAS MISSING)
        prompt = f"""
        You are a data analyst.

        Dataset columns: {list(df.columns)}

        User question: {question}

        Give a clear, simple answer.
        """

        response = ask_llm(prompt)

        return f"🤖 AI Response:\n{response}"

    except Exception as e:
        return f"Error: {str(e)}"