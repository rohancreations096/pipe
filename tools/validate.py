from utils.logger import log

def validate_data(df):
    log("Validating data")

    if df.empty:
        raise ValueError("Data is empty!")

    return True