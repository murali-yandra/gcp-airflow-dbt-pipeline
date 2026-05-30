from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

# Default arguments for enterprise task resilience
default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'gcp_end_to_end_pipeline',
    default_args=default_args,
    description='Automated orchestration for GCS, BigQuery, and dbt Cloud transformations',
    schedule_interval='@daily',
    catchup=False,
) as dag:

# TASK 1: Land local data into the GCS Data Lake
    upload_raw_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_raw_to_gcs',
        # THIS IS THE INTERNAL LINUX PATH
        src='/opt/airflow/dags/sample_products.csv',
        dst='raw/sample_products.csv',
        bucket='faang-data-lake-murali-yandra',
        gcp_conn_id='google_cloud_default'
    )

    # TASK 2: Atomic Batch Ingestion into BigQuery Storage
    gcs_to_bigquery_load = GCSToBigQueryOperator(
        task_id='gcs_to_bigquery_load',
        bucket='faang-data-lake-murali-yandra',
        source_objects=['raw/sample_products.csv'],
        destination_project_dataset_table='faang-data-warehouse-2026.raw_data.sample_products',
        schema_fields=[
            {'name': 'product_id', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            {'name': 'product_name', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'price_usd', 'type': 'FLOAT', 'mode': 'NULLABLE'},
        ],
        write_disposition='WRITE_TRUNCATE', # Overwrites table data with fresh snapshot daily
        skip_leading_rows=1,
        gcp_conn_id='google_cloud_default'
    )

# TASK 3: Trigger the dbt Analytical Transformation Engine via Bash (Idempotent User Space)
    execute_dbt_transformations = BashOperator(
        task_id='execute_dbt_transformations',
        bash_command="""
            # 1. Bulletproof check: Does the dbt application already exist in the backpack?
            if [ ! -f "/home/airflow/.local/bin/dbt" ]; then
                echo "Installing dbt into the Airflow user environment..."
                pip install --no-cache-dir --user dbt-bigquery==1.11.1
            else
                echo "dbt is already installed. Skipping download!"
            fi
            
            # 2. Execute the models and run Data Quality Tests
            cd /opt/airflow/dags/faang_analytics
            # Changed 'run' to 'build' to trigger schema.yml tests
            /home/airflow/.local/bin/dbt build -s dim_products --profiles-dir .
        """,
        env={'GOOGLE_APPLICATION_CREDENTIALS': '/opt/airflow/dags/gcp_key.json'}
    )
    # Define the execution dependencies (The Lineage Graph)
    upload_raw_to_gcs >> gcs_to_bigquery_load >> execute_dbt_transformations