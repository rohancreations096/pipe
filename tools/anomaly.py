import numpy as np

def detect_anomalies(df, log):
    issues = []

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = df[(df[col] < lower) | (df[col] > upper)]

        if not outliers.empty:
            issues.append(f"Outliers detected in {col}")

            # Cap values
            df[col] = np.clip(df[col], lower, upper)

    if issues:
        log(f"[ANOMALY] {issues}")

    return df