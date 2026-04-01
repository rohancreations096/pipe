import sqlite3
from utils.logger import log

def store_data(df):
    log("Storing data in SQLite")

    conn = sqlite3.connect("data.db")
    df.to_sql("pipeline_data", conn, if_exists="replace", index=False)
    conn.close()