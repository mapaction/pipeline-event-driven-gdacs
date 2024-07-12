# util/data_exploration.py

import os
import sqlite3

import pandas as pd

db_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../data/gdacs_events.db")
)


def check_database(db_path):
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
        return False
    else:
        print(f"Database file found at {db_path}")
        return True


def fetch_data_from_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM events", conn)
        conn.close()
        return df
    except sqlite3.OperationalError as e:
        print(f"OperationalError: {e}")
        return None


def fetch_exposed_countries(db_path):
    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM exposed_countries"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except sqlite3.OperationalError as e:
        print(f"OperationalError: {e}")
        return None
