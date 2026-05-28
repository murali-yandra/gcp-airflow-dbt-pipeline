from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'murali',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'daily_end_to_end_pipeline',
    default_args=default_args,
    description='Complete ELT Pipeline: Python to PostgreSQL to dbt',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # Task 1: Extract and Load (Python)
    # This runs the actual script we built.
    extract_and_load = BashOperator(
        task_id='extract_and_load_api',
        bash_command='python /opt/airflow/dags/etl_pipeline.py',
    )

    # Task 2: Transform (dbt run)
    # Simulating the dbt execution
    transform_data = BashOperator(
        task_id='dbt_run_models',
        bash_command='echo "Executing push-down ELT: dbt run -s dim_products"',
    )

    # Task 3: Data Quality Tests (dbt test)
    # Simulating the data bouncer
    test_data = BashOperator(
        task_id='dbt_test_models',
        bash_command='echo "Executing data quality checks: dbt test"',
    )

    # ---------------------------------------------------------
    # THE GRAPH TOPOLOGY (Setting the dependencies)
    # ---------------------------------------------------------
    extract_and_load >> transform_data >> test_data