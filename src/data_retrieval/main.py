import time

from display.display import display_event_details
from fetcher.rss_fetcher import fetch_latest_rss_events


def main():
    while True:
        latest_rss_events = fetch_latest_rss_events()
        if latest_rss_events:
            display_event_details(latest_rss_events)
        else:
            print("No events found.")
        time.sleep(300)


if __name__ == "__main__":
    main()
