import time

from activate.activate_dag import activate_dag
from status.check_status import check_dag_status
from trigger.trigger_dag import trigger_dag

from src.pipeline_trigger.static_data.countries_iso import COUNTRIES


def process_new_entries(entries, username, password):
    for entry in entries:
        country_iso = entry[3]
        country_name = None
        for name, details in COUNTRIES.items():
            if details["code"] == country_iso:
                country_name = name
                break
        if country_name:
            dag_id = f"dynamic_generated_dag_{country_name}"
            if activate_dag(dag_id, username, password) and trigger_dag(
                dag_id, username, password
            ):
                while True:
                    status = check_dag_status(dag_id, username, password)
                    if status == "success":
                        print(f"DAG {dag_id} completed successfully.")
                        break
                    elif status == "failed":
                        print(f"DAG {dag_id} failed.")
                        break
                    elif status in ["queued", "running"]:
                        print(f"DAG {dag_id} is still {status}. Waiting...")
                        time.sleep(600)  # Wait for 10 min
                    else:
                        print(f"Unexpected status {status} for DAG {dag_id}.")
                        break
        else:
            print(
                f"Country ISO code {country_iso} not found in COUNTRIES dictionary."  # noqa
            )  # noqa
