import feedparser


def fetch_latest_rss_events(alert_levels=["Red", "Orange"], limit=10):
    rss_url = "https://www.gdacs.org/xml/rss.xml"
    feed = feedparser.parse(rss_url)
    filtered_events = [
        entry
        for entry in feed.entries
        if any(alert in entry.title for alert in alert_levels)
    ][:limit]
    return filtered_events
