from sklearn.ensemble import IsolationForest
from utils.logger import log

def detect_anomalies(df):

    log("Running anomaly detection")

    numeric_df = df.select_dtypes(include=['int64', 'float64'])

    if numeric_df.empty:
        return df, None

    model = IsolationForest(contamination=0.05, random_state=42)

    df['anomaly'] = model.fit_predict(numeric_df)

    return df, df[df['anomaly'] == -1]