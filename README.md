# Market & Weather Intelligence : ELT Lakehouse

A production-style ELT data pipeline built with modern data engineering tools.

🔴 **[View Live Dashboard](https://lakehouse-project-mzgx8ogbwzevad9fxr8ry7.streamlit.app)**

## What it does
Pulls live data from 3 APIs daily (weather, stocks, news), stores it in a cloud 
data lake, transforms it with dbt, orchestrates with Airflow, and serves it via 
an interactive public dashboard.

## Architecture
## Tech stack
- **Extract:** Python, requests
- **Storage:** Supabase (cloud data lake), Parquet
- **Warehouse:** DuckDB
- **Transform:** dbt (6 automated data quality tests)
- **Orchestration:** Apache Airflow (daily schedule)
- **Dashboard:** Streamlit, Plotly

## Data sources
- OpenWeatherMap / wttr.in — live weather for 5 US cities
- Alpha Vantage — daily stock prices (AAPL, GOOGL, MSFT, AMZN, TSLA)
- NewsAPI — latest headlines by ticker

## How to run locally
1. Clone the repo
2. `python3 -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your API keys
5. `python3 extract/weather.py`
6. `streamlit run dashboard.py`
