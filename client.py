import feedparser
import requests
from datetime import datetime

# URL του RSS feed Newsbeast
NEWSBEAST_RSS_URL = "https://www.newsbeast.gr/feed"

# URL του MCP Agent
AGENT_URL = "http://localhost:8000/classify"

def parse_entry(entry):
    """
    Μετατρέπει ένα RSS entry σε ApempeArticle contract.
    """
    return {
        "source": "apembe",  # σταθερό για MCP contract
        "title": entry.get("title", ""),
        "body": entry.get("summary", entry.get("description", "")),
        "timestamp": entry.get("published", datetime.utcnow().isoformat())
    }

def ingest_rss():
    """
    Διαβάζει το RSS feed, στέλνει κάθε άρθρο στον Agent και τυπώνει το αποτέλεσμα.
    """
    feed = feedparser.parse(NEWSBEAST_RSS_URL)

    if not feed.entries:
        print("Δεν βρέθηκαν άρθρα στο feed.")
        return

    for entry in feed.entries:
        article = parse_entry(entry)

        try:
            response = requests.post(AGENT_URL, json=article, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Σφάλμα κατά την επικοινωνία με Agent: {e}")
            continue

        result = response.json()
        print(f"[{result['category']}] {article['title']}")

if __name__ == "__main__":
    ingest_rss()
