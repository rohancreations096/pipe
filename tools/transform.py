from utils.logger import log

def transform_data(df):
    log("Transforming data")

    if 'salary' in df.columns:
        df['salary'] = df['salary'] * 1.1  # simple feature engineering

    return df