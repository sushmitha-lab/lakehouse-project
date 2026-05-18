from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

files = [
    ("extract/weather_test.parquet", "raw/weather/data.parquet"),
    ("extract/stocks_test.parquet", "raw/stocks/data.parquet"),
    ("extract/news_test.parquet", "raw/news/data.parquet"),
]

def upload_files():
    for local_path, remote_path in files:
        with open(local_path, "rb") as f:
            supabase.storage.from_("raw-data").upload(
                remote_path,
                f.read(),
                {"content-type": "application/octet-stream"}
            )
        print(f"Uploaded: {remote_path}")

if __name__ == "__main__":
    upload_files()
