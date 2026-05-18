import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

TOPICS = ["Apple stock", "Google", "Microsoft", "Amazon", "Tesla"]

def extract_news():
    results = []
    for topic in TOPICS:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": topic,
            "apiKey": API_KEY,
            "language": "en",
            "pageSize": 3,
            "sortBy": "publishedAt"
        }
        response = requests.get(url, params=params)
        data = response.json()
        for article in data["articles"]:
            results.append({
                "topic": topic,
                "title": article["title"],
                "source": article["source"]["name"],
                "published_at": article["publishedAt"],
                "extracted_at": datetime.utcnow().isoformat()
            })
        print(f"Extracted: {topic}")

    df = pd.DataFrame(results)
    print(df)
    return df

if __name__ == "__main__":
    extract_news()
