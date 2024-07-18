import sqlite3


def get_new_entries(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT * FROM exposed_countries"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows
