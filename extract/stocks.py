import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
import time

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

TICKERS = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]

def extract_stocks():
    results = []
    for ticker in TICKERS:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()
        quote = data["Global Quote"]
        results.append({
            "ticker": ticker,
            "price": quote["05. price"],
            "change": quote["09. change"],
            "change_percent": quote["10. change percent"],
            "volume": quote["06. volume"],
            "extracted_at": datetime.utcnow().isoformat()
        })
        print(f"Extracted: {ticker}")
        time.sleep(12)

    df = pd.DataFrame(results)
    print(df)
    return df

if __name__ == "__main__":
    extract_stocks()
