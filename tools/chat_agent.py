def answer_question(df, question):
    question = question.lower()

    if "rows" in question:
        return f"The dataset has {df.shape[0]} rows."

    if "columns" in question:
        return f"The dataset has {df.shape[1]} columns."

    if "missing" in question:
        return f"Missing values: {df.isnull().sum().sum()}"

    if "average" in question or "mean" in question:
        numeric = df.select_dtypes(include=['int64', 'float64'])
        if not numeric.empty:
            return numeric.mean().to_string()

    return "I couldn't understand. Try: rows, columns, mean, missing values."