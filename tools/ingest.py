import pandas as pd
from utils.logger import log

def ingest_data(source):
    log(f"Ingesting data from {source}")
    try:
        df = pd.read_csv(source)
        return df
    except Exception as e:
        log(f"Ingestion failed: {e}")
        return None