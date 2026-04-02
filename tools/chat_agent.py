from tools.llm import ask_llm


def answer_question(df, question):
    """
    Smart AI-powered Q&A using LLM
    """

    if df is None:
        return "⚠️ Please upload data first."

    # 🚀 Use LLM instead of rules
    response = ask_llm(question, df)

    return response