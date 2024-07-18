import requests
from requests.auth import HTTPBasicAuth


def check_dag_status(dag_id, username, password):
    url = f"http://192.168.104.21:8080/api/v1/dags/{dag_id}/dagRuns?limit=1&order_by=-execution_date"  # noqa
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            dag_runs = response.json()
            if dag_runs["dag_runs"]:
                last_run = dag_runs["dag_runs"][0]
                print(f"Last run of DAG {dag_id} status: {last_run['state']}")
                return last_run[
                    "state"
                ]  # e.g., 'success', 'failed', 'queued', 'running'
            else:
                print(f"No runs found for DAG {dag_id}.")
                return "no_runs"
        else:
            print(
                f"Failed to get status for DAG {dag_id}. Status code: {response.status_code}, Response: {response.text}"  # noqa
            )  # noqa
            return "error"
    except requests.exceptions.RequestException as e:
        print(f"Failed to get status for DAG {dag_id}. Error: {e}")
        return "error"
