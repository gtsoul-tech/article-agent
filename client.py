import feedparser
import requests
import time
from datetime import datetime

NEWSBEAST_RSS_URL = "https://www.newsbeast.gr/feed"
AGENT_URL = "http://localhost:8000/classify"

DELAY_SECONDS = 200         # 2 minutes
REQUEST_TIMEOUT = 300      # must be > DELAY_SECONDS

def parse_entry(entry):
    return {
        "source": "apembe",
        "title": entry.get("title", ""),
        "body": entry.get("summary", entry.get("description", "")),
        "timestamp": entry.get("published", datetime.utcnow().isoformat())
    }

def ingest_rss():
    feed = feedparser.parse(NEWSBEAST_RSS_URL)

    if not feed.entries:
        print("Δεν βρέθηκαν άρθρα στο feed.")
        return

    for i, entry in enumerate(feed.entries, start=1):
        article = parse_entry(entry)

        print(f"[{i}/{len(feed.entries)}] Processing: {article['title']}")

        try:
            response = requests.post(
                AGENT_URL,
                json=article,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            result = response.json()
            print(f"→ {result['category']} (confidence={result['confidence']})")

        except requests.RequestException as e:
            print(f"Agent error: {e}")

        # Rate limit
        if i < len(feed.entries):
            print(f"Waiting {DELAY_SECONDS}s before next article...")
            time.sleep(DELAY_SECONDS)

if __name__ == "__main__":
    ingest_rss()
