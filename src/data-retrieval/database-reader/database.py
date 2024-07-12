import json
import os
import sqlite3
from datetime import datetime

script_dir = os.path.dirname(__file__)
db_path = os.path.join(script_dir, "..", "..", "..", "data", "gdacs_events.db")


def gdacs_id_exists(gdacs_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM events WHERE gdacs_id = ?", (gdacs_id,)
    )  # noqa E501
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists


def get_current_version(event_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT MAX(version) FROM events WHERE gdacs_id = ?", (event_id,)
    )  # noqa E501
    result = cursor.fetchone()
    conn.close()
    return result[0] if result[0] is not None else 0


def get_existing_countries(gdacs_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT country, country_iso FROM exposed_countries WHERE gdacs_id = ?",  # noqa E501
        (gdacs_id,),
    )
    countries = {(row[0], row[1]) for row in cursor.fetchall()}
    conn.close()
    return countries


def get_latest_modification_date(event_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT MAX(datemodified) FROM events WHERE gdacs_id = ?", (event_id,)
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result[0] is not None else None


def store_event_in_db(
    event_id, event_details, rss_event, version, modification_date
):  # noqa E501
    existing_countries = get_existing_countries(event_id)
    new_countries = {
        (country["countryname"], country["iso3"].lower())
        for country in event_details.get("affectedcountries", [])
    }
    countries_to_add = new_countries - existing_countries

    if not countries_to_add:
        print(
            f"GDACS ID {event_id} already exists with no new countries. "
            f"Skipping entry."
        )
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    exposed_countries_json = json.dumps(
        list(new_countries)
    )  # Convert list to JSON string

    cursor.execute(
        """
        INSERT INTO events (
            gdacs_id, event_title, summary, link, published_date, name,
            from_date, to_date, exposed_countries, exposed_population,
            max_wind_speed, max_storm_surge, vulnerability, alert_level,
            gdacs_score, version, last_updated, datemodified
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event_id,
            rss_event.title,
            rss_event.summary,
            rss_event.link,
            datetime.strptime(rss_event.published, "%a, %d %b %Y %H:%M:%S %Z"),
            event_details.get("name", "N/A"),
            (
                datetime.strptime(
                    event_details.get("fromdate", "N/A"), "%Y-%m-%dT%H:%M:%S"
                )
                if event_details.get("fromdate", "N/A") != "N/A"
                else None
            ),
            (
                datetime.strptime(
                    event_details.get("todate", "N/A"), "%Y-%m-%dT%H:%M:%S"
                )
                if event_details.get("todate", "N/A") != "N/A"
                else None
            ),
            exposed_countries_json,  # Store JSON string
            (
                int(event_details.get("population", 0))
                if event_details.get("population", "N/A") != "N/A"
                else None
            ),
            (
                int(event_details.get("maxwindspeed", 0))
                if event_details.get("maxwindspeed", "N/A") != "N/A"
                else None
            ),
            (
                float(event_details.get("maxstormsurge", 0.0))
                if event_details.get("maxstormsurge", "N/A") != "N/A"
                else None
            ),
            event_details.get("vulnerability", "N/A"),
            event_details.get("alertlevel", "N/A"),
            (
                int(event_details.get("alertscore", 0))
                if event_details.get("alertscore", "N/A") != "N/A"
                else None
            ),
            version,
            datetime.now(),
            modification_date,
        ),
    )
    event_row_id = cursor.lastrowid

    # Insert new exposed countries
    for country, iso in countries_to_add:
        cursor.execute(
            """
            INSERT INTO exposed_countries (event_id,
            gdacs_id, country, country_iso)
            VALUES (?, ?, ?, ?)
            """,
            (event_row_id, event_id, country, iso),
        )

    conn.commit()
    conn.close()
