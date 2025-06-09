from __future__ import annotations

import pendulum
import logging

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.email import send_email

# --- Configuration Section ---
# Define configurable parameters for your ETL DAG.
# These can be accessed within tasks using config["key_name"].
# For dynamic values like execution date, Airflow Jinja templating is used.
config = {
  "source_system_name": "crm_data", # Example: Name of the source system
  "target_dataset_name": "data_warehouse", # Example: Target BigQuery dataset or database schema
  "target_table_prefix": "stg_", # Prefix for staging tables
  "gcs_bucket_name": "your-etl-data-bucket", # Your Google Cloud Storage bucket
  "raw_data_path_template": "raw_data/{{ ds_nodash }}/{{ source_system_name }}/",
  "processed_data_path_template": "processed_data/{{ ds_nodash }}/{{ source_system_name }}/",
  "email_on_failure": ["your_email@example.com"], # Email recipient for failure alerts
  "slack_webhook_url": None, # Optional: Slack webhook URL for notifications
}

# --- Common ETL Functions (Python Callables) ---
# These functions define the actual logic for your ETL steps.
# They are designed to be called by PythonOperator.
# Use **kwargs to access Airflow context variables (e.g., dag_run, task_instance).

def extract_data_from_source(**kwargs):
  pass
