from utils.logger import log

def clean_data(df):
    log("Cleaning data")

    df = df.drop_duplicates()
    df = df.fillna(method='ffill')

    return df