from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/Users/sushmithakatherinej/lakehouse-project')

from extract.weather import extract_weather
from extract.stocks import extract_stocks
from extract.news import extract_news

default_args = {
    'owner': 'sushmitha',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def save_weather():
    df = extract_weather()
    df.to_parquet('/Users/sushmithakatherinej/lakehouse-project/extract/weather_test.parquet')
    print('Weather saved!')

def save_stocks():
    df = extract_stocks()
    df.to_parquet('/Users/sushmithakatherinej/lakehouse-project/extract/stocks_test.parquet')
    print('Stocks saved!')

def save_news():
    df = extract_news()
    df.to_parquet('/Users/sushmithakatherinej/lakehouse-project/extract/news_test.parquet')
    print('News saved!')

with DAG(
    'lakehouse_pipeline',
    default_args=default_args,
    description='Daily ELT pipeline',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    extract_weather_task = PythonOperator(
        task_id='extract_weather',
        python_callable=save_weather,
    )

    extract_stocks_task = PythonOperator(
        task_id='extract_stocks',
        python_callable=save_stocks,
    )

    extract_news_task = PythonOperator(
        task_id='extract_news',
        python_callable=save_news,
    )

    extract_weather_task >> extract_stocks_task >> extract_news_task
