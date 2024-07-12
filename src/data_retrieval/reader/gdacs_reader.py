import requests


class CustomGDACSAPIError(Exception):
    pass


class CustomGDACSAPIReader:
    def fetch_event_details(self, event_type, event_id):
        url = f"https://www.gdacs.org/gdacsapi/api/events/geteventdata?eventtype={event_type}&eventid={event_id}"  # noqa E501
        response = requests.get(url)
        if response.status_code != 200:
            raise CustomGDACSAPIError(
                f"API Error: Failed to fetch details for event ID {event_id}."
            )
        return response.json()
