from tools.llm import ask_llm

def clean_data(df, log):

    before = df.shape[0]
    df = df.drop_duplicates()
    log(f"Removed {before - df.shape[0]} duplicates")

    missing = df.isnull().sum().sum()

    if missing > 0:

        prompt = f"""
        Columns: {list(df.columns)}
        Missing values: {missing}

        Suggest cleaning strategy.
        """

        decision = ask_llm(prompt)
        log(f"[LLM DECISION] {decision}")

        df = df.ffill().bfill().fillna("unknown")

    return df