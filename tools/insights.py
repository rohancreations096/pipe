def generate_insights(df):
    insights = []

    insights.append(f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns.")

    missing = df.isnull().sum().sum()
    insights.append(f"Total missing values: {missing}")

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

    if len(numeric_cols) > 0:
        for col in numeric_cols[:3]:
            insights.append(f"{col}: mean={df[col].mean():.2f}, max={df[col].max()}")

    return insights