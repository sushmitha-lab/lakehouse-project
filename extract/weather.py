import requests
import pandas as pd
from datetime import datetime

CITIES = ["New York", "Los Angeles", "Chicago", "Houston", "Boston"]

def extract_weather():
    results = []
    for city in CITIES:
        url = f"http://wttr.in/{city}?format=j1"
        response = requests.get(url)
        data = response.json()
        current = data["current_condition"][0]
        results.append({
            "city": city,
            "temperature_f": current["temp_F"],
            "humidity": current["humidity"],
            "weather": current["weatherDesc"][0]["value"],
            "wind_speed": current["windspeedMiles"],
            "extracted_at": datetime.utcnow().isoformat()
        })
        print(f"Extracted: {city}")

    df = pd.DataFrame(results)
    print(df)
    return df

if __name__ == "__main__":
    extract_weather()
