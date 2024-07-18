import os
import time

from dotenv import load_dotenv
from info_retrieval.data_retrieval import get_new_entries
from processor.process_entries import process_new_entries

load_dotenv()


def monitor_database(db_path, username, password):
    last_seen_ids = set()
    while True:
        entries = get_new_entries(db_path)
        new_entries = [
            entry for entry in entries if entry[0] not in last_seen_ids
        ]  # noqa
        if new_entries:
            process_new_entries(new_entries, username, password)
            last_seen_ids.update(entry[0] for entry in new_entries)
        else:
            print("No new entries found.")
        time.sleep(300)  # Sleep for 5 minutes


if __name__ == "__main__":
    db_path = os.getenv("DB_PATH")
    airflow_username = os.getenv("AIRFLOW_USERNAME")
    airflow_password = os.getenv("AIRFLOW_PASSWORD")

    if db_path and airflow_username and airflow_password:
        monitor_database(db_path, airflow_username, airflow_password)
    else:
        print(
            "Environment variables DB_PATH, AIRFLOW_USERNAME, and AIRFLOW_PASSWORD must be set."  # noqa
        )
