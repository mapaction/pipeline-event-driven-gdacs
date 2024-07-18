import requests
from requests.auth import HTTPBasicAuth


def activate_dag(dag_id, username, password):
    url = f"http://192.168.104.21:8080/api/v1/dags/{dag_id}"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            dag_info = response.json()
            if not dag_info["is_paused"]:
                print(f"DAG {dag_id} is already active.")
                return True
            else:
                # Activate the DAG
                data = {"is_paused": False}
                response = requests.patch(
                    url,
                    json=data,
                    headers=headers,
                    auth=HTTPBasicAuth(username, password),
                )
                if response.status_code == 200:
                    print(f"DAG {dag_id} activated successfully.")
                    return True
                else:
                    print(
                        f"Failed to activate DAG {dag_id}. Status code: {response.status_code}, Response: {response.text}"  # noqa
                    )
                    return False
        else:
            print(
                f"Failed to get status for DAG {dag_id}. Status code: {response.status_code}, Response: {response.text}"  # noqa
            )
            return False
    except requests.exceptions.RequestException as e:
        print(f"Failed to get status for DAG {dag_id}. Error: {e}")
        return False
