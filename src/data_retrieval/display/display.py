from datetime import datetime

from src.data_retrieval.database_reader.database import (
    get_current_version,
    get_latest_modification_date,
    store_event_in_db,
)
from src.data_retrieval.reader.gdacs_reader import (
    CustomGDACSAPIError,
    CustomGDACSAPIReader,
)


def display_event_details(rss_events):
    custom_api_reader = CustomGDACSAPIReader()

    for rss_event in rss_events:
        event_id = rss_event.link.split("eventid=")[-1]
        event_type = (
            rss_event.link.split("eventtype=")[-1].split("&")[0].upper()
        )  # noqa E501

        print("-" * 40)
        print(f"Event Title: {rss_event.title}")
        print(f"GDACS ID: {event_id}")
        print(f"Summary: {rss_event.summary}")
        print(f"Link: {rss_event.link}")
        print(f"Published Date: {rss_event.published}")

        try:
            custom_event_details = custom_api_reader.fetch_event_details(
                event_type=event_type, event_id=event_id
            )
            props = custom_event_details["properties"]

            print(f"Name: {props.get('name', 'N/A')}")
            print(
                f"From - To: {props.get('fromdate', 'N/A')[:10]} - "
                f"{props.get('todate', 'N/A')[:10]}"
            )
            affected_countries = [
                f"{country['countryname']} ({country['iso3'].lower()})"
                for country in props.get("affectedcountries", [])
            ]
            affected_countries_str = ", ".join(affected_countries)
            if affected_countries:
                print(f"Exposed countries: {affected_countries_str}")
            if props.get("population", "N/A") != "N/A":
                print(
                    f"Exposed population: {props.get('population', 'N/A')} in "
                    f"Category 1 or higher"
                )
            if props.get("maxwindspeed", "N/A") != "N/A":
                print(
                    f"Maximum wind speed: {props.get('maxwindspeed', 'N/A')} km/h "  # noqa E501
                    f"Category {props.get('maxwindspeedcat', 'N/A')}"
                )
            if props.get("maxstormsurge", "N/A") != "N/A":
                print(
                    f"Maximum storm surge: {props.get('maxstormsurge', 'N/A')} m "  # noqa E501
                    f"({props.get('maxstormsurgedate', 'N/A')})"
                )
            if props.get("vulnerability", "N/A") != "N/A":
                print(f"Vulnerability: {props.get('vulnerability', 'N/A')}")
            print(f"Alert Level: {props.get('alertlevel', 'N/A')}")
            print(f"GDACS Score: {props.get('alertscore', 'N/A')}")

            modification_date = props.get(
                "datemodified", datetime.now().isoformat()
            )  # noqa E501
            latest_modification_date = get_latest_modification_date(event_id)
            if latest_modification_date and datetime.fromisoformat(
                modification_date
            ) <= datetime.fromisoformat(latest_modification_date):
                print(
                    f"GDACS ID {event_id} has no new updates. Skipping entry."
                )  # noqa E501
                continue

            current_version = get_current_version(event_id) + 1
            store_event_in_db(
                event_id, props, rss_event, current_version, modification_date
            )
        except CustomGDACSAPIError as e:
            print(f"Error fetching details for event ID {event_id}: {e}")
