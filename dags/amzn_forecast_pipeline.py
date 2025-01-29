from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os

# Default DAG arguments
default_args = {
    "owner": "Fran",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    "amzn_forecast_pipeline",
    default_args=default_args,
    description="Pipeline for AMZN stock forecasting",
    schedule_interval="@daily",
    catchup=False,
)

# Define Python functions for tasks
def extract_data():
    """Extract AMZN stock data from Alpha Vantage API."""
    os.system("python scripts/extract_data.py")

def preprocess_data():
    """Preprocess stock data and compute indicators."""
    os.system("python scripts/preprocess_data.py")

def train_model():
    """Train HGBR model on processed stock data."""
    os.system("python scripts/train_model.py")

def predict():
    """Generate stock price predictions using trained model."""
    os.system("python scripts/predict.py")

def visualize_predictions():
    """Generate a visualization of actual vs predicted stock prices."""
    os.system("python scripts/visualize_predictions.py")

# Define Airflow tasks
extract_task = PythonOperator(
    task_id="extract_data",
    python_callable=extract_data,
    dag=dag,
)

preprocess_task = PythonOperator(
    task_id="preprocess_data",
    python_callable=preprocess_data,
    dag=dag,
)

train_task = PythonOperator(
    task_id="train_model",
    python_callable=train_model,
    dag=dag,
)

predict_task = PythonOperator(
    task_id="predict",
    python_callable=predict,
    dag=dag,
)

visualize_task = PythonOperator(
    task_id="visualize_predictions",
    python_callable=visualize_predictions,
    dag=dag,
)

# Define task execution order
extract_task >> preprocess_task >> train_task >> predict_task >> visualize_task
