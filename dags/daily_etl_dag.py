from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# 1. Define the default arguments for the DAG
# This tells Airflow how to handle failures
default_args = {
    'owner': 'murali',
    'depends_on_past': False,
    'start_date': days_ago(1), # Start yesterday so it runs immediately
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 2. Instantiate the DAG
# We give it a name, attach the arguments, and set the schedule
with DAG(
    'daily_product_etl',
    default_args=default_args,
    description='A simple DAG to run our Python ETL pipeline',
    schedule_interval='@daily', # Run at midnight every day
    catchup=False,
) as dag:

    # 3. Define the Tasks
    # We use a BashOperator to literally type "python etl_pipeline.py" into the terminal
    run_etl_script = BashOperator(
        task_id='execute_python_script',
        # Airflow runs inside Docker, so we map the path to where the file lives inside the container
        bash_command='python /opt/airflow/dags/etl_pipeline.py',
    )

    # 4. Set the Dependencies (The Graph)
    # Since we only have one task, it just runs. 
    # If we had multiple, it would look like: extract >> transform >> load
    run_etl_script