from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth


def trigger_dag(dag_id, username, password):
    url = f"http://192.168.104.21:8080/api/v1/dags/{dag_id}/dagRuns"
    data = {
        "conf": {},
        "execution_date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    try:
        response = requests.post(
            url, json=data, auth=HTTPBasicAuth(username, password)
        )  # noqa
        if response.status_code == 200:
            print(f"DAG {dag_id} triggered successfully.")
            return True
        else:
            print(
                f"Failed to trigger DAG {dag_id}. Status code: {response.status_code}, Response: {response.text}"  # noqa
            )  # noqa
            return False
    except requests.exceptions.RequestException as e:
        print(f"Failed to trigger DAG {dag_id}. Error: {e}")
        return False
