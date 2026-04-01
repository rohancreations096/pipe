from tools.llm import ask_llm

def answer_question(df, question):

    q = question.lower()

    if "rows" in q:
        return f"Rows: {df.shape[0]}"

    if "columns" in q:
        return f"Columns: {df.shape[1]}"

    if "missing" in q:
        return f"Missing values: {df.isnull().sum().sum()}"

    if "mean" in q or "average" in q:
        return df.select_dtypes(include=['int64','float64']).mean().to_string()

    # LLM fallback
    sample = df.sample(min(20, len(df))).to_string()

    prompt = f"""
    Dataset sample:
    {sample}

    Question:
    {question}

    Answer clearly.
    """

    return ask_llm(prompt)