import sqlite3
import pandas as pd

DB_NAME = "sales.db"


def create_table():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales(
        order_id INTEGER PRIMARY KEY,
        order_date TEXT,
        product TEXT,
        category TEXT,
        region TEXT,
        quantity INTEGER,
        unit_price REAL,
        revenue REAL
    )
    """)

    conn.commit()
    conn.close()


def insert_data(df):

    conn = sqlite3.connect(DB_NAME)

    df.to_sql("sales", conn, if_exists="replace", index=False)

    conn.close()


def fetch_data():

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql("SELECT * FROM sales", conn)

    conn.close()

    return df
