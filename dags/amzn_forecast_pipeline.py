from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 1),
    "retries": 1,
}

def run_script(script_name):
    """
    Executes a Python script located in /opt/airflow/scripts/.
    This ensures the script runs inside the Airflow worker.
    """
    script_path = f"/opt/airflow/scripts/{script_name}"
    print(f"🚀 Running script: {script_path}")
    result = subprocess.run(["python", script_path], capture_output=True, text=True)

    print(f"✅ Script Output:\n{result.stdout}")
    if result.stderr:
        print(f"❌ Script Error:\n{result.stderr}")

with DAG(
    "amzn_forecast_pipeline",  # NEW DAG NAME
    default_args=default_args,
    schedule_interval=None,  # Manual trigger only
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=run_script,
        op_kwargs={"script_name": "extract_data.py"},
    )

    preprocess_task = PythonOperator(
        task_id="preprocess_data",
        python_callable=run_script,
        op_kwargs={"script_name": "preprocess_data.py"},
    )

    train_task = PythonOperator(
        task_id="train_model",
        python_callable=run_script,
        op_kwargs={"script_name": "train_model.py"},
    )

    predict_task = PythonOperator(
        task_id="predict",
        python_callable=run_script,
        op_kwargs={"script_name": "predict.py"},
    )

    visualize_task = PythonOperator(
        task_id="visualize_predictions",
        python_callable=run_script,
        op_kwargs={"script_name": "visualize_predictions.py"},
    )

    # Define task dependencies
    extract_task >> preprocess_task >> train_task >> predict_task >> visualize_task
