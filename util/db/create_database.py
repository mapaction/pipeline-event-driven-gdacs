import os
import sqlite3

db_dir = os.path.dirname(os.path.abspath(__file__))

database_path = os.path.join(db_dir, "..", "..", "data", "gdacs_events.db")


def create_database():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gdacs_id TEXT,
            event_title TEXT,
            summary TEXT,
            link TEXT,
            published_date DATETIME,
            name TEXT,
            from_date DATETIME,
            to_date DATETIME,
            exposed_countries TEXT,  -- Will store JSON string
            exposed_population INTEGER,
            max_wind_speed INTEGER,
            max_storm_surge REAL,
            vulnerability TEXT,
            alert_level TEXT,
            gdacs_score INTEGER,
            version INTEGER,
            last_updated DATETIME,
            datemodified DATETIME,  -- Added datemodified column
            UNIQUE(gdacs_id, version)
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS exposed_countries (
            event_id INTEGER,
            gdacs_id TEXT,
            country TEXT,
            country_iso TEXT,  -- New column for country ISO code
            FOREIGN KEY(event_id) REFERENCES events(id),
            FOREIGN KEY(gdacs_id) REFERENCES events(gdacs_id)
        )
    """
    )
    conn.commit()
    conn.close()
