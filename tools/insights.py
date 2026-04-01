from tools.llm import ask_llm

def generate_insights(df):

    sample = df.sample(min(20, len(df))).to_string()

    prompt = f"""
    Analyze dataset:

    {sample}

    Give 5 insights.
    """

    return ask_llm(prompt)