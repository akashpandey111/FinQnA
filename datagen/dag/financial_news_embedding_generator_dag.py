import os

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()

from utils.alpaca_handler import download_historical_news
from orchestration import embed_news_into_qdrant

default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'start_date': datetime.today(),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'financial_news_embedding_generator',
    default_args=default_args,
    description='DAG to process financial news',
    schedule_interval=timedelta(days=1),
)

# Get the current date
current_date = datetime.now()

# Calculate the date one month ago
six_month_ago = current_date - timedelta(days=180)

download_task = PythonOperator(
    task_id='download_financial_news',
    python_callable=download_historical_news,
    provide_context=True,
    op_kwargs={"from_date": six_month_ago, "to_date": current_date},
    dag=dag,
)

embed_and_push_task = PythonOperator(
    task_id='embed_and_push_to_qdrant',
    python_callable=embed_news_into_qdrant,
    provide_context=True,
    op_args=[],
    dag=dag,
)

download_task >> embed_and_push_task
