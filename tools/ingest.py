import pandas as pd

def ingest_data(source):

    if source.startswith("http"):
        return pd.read_json(source)

    else:
        return pd.read_csv(source)