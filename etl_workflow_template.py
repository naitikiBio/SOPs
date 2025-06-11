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
  """
  Placeholder function for extracting data from a source system.
  Replace with actual data extraction logic (e.g., pulling from a database, API).
  """
  source_name = kwargs["params"].get("source_system", config["source_system_name"])
  execution_date_str = kwargs["ds_nodash"]
  logging.info(f"Starting data extraction for {source_name} on {execution_date_str}...")

  # Example: Simulate data extraction
  # In a real scenario, you'd use a database hook, API client, etc.
  # from google.cloud import bigquery # Example for BigQuery
  # client = bigquery.Client()
  # query = f"SELECT * FROM `{source_name}.source_table` WHERE date = '{execution_date_str}'"
  # results = client.query(query).result()
  # for row in results:
  #   logging.info(row)

  # Push extracted file path (or other identifier) to XCom for downstream tasks
  # XComs are a way for tasks to exchange small amounts of data.
  extracted_file_path = f"gs://{config['gcs_bucket_name']}/{config['raw_data_path_template']}/extracted_data.csv"
  kwargs['ti'].cxom_push(key='extracted_file_path', value = extracted_file_path)
  logging.info(f"Data extracted and notionally stored at: {extracted_file_path}")
  logging.info("Data extraction complete.")

def _transform_data(**kwargs):
  """
  Placeholder function for transforming extracted data.
  Replace with actual data transformation logic (e.g., cleaning, aggregation).
  """
  extracted_file_path = kwargs['ti'].cxom_pull(key = 'extracted_file_path', task_ids = 'extract_data_task')
  execution_date_str = kwargs["ds_nodash"]
  logging.info(f"Starting data transformation for {extracted_file_path} on {execution_date_str}...")

  # Example: Simulate data transformation
  # In a real scenario, you might use Pandas, Spark, or BigQuery transformations.
  # import pandas as pd
  # df = pd.read_csv(extracted_file_path) # Not directly from GCS, would need GCSFs
  # df['new_column'] = df['original_column'] * 2
  # transformed_data_path = f"gs://{config['gcs_bucket_name']}/{config['processed_data_path_template']}/transformed_data.parquet"
  # df.to_parquet(transformed_data_path)

  transformed_data_path = f"gs://{config['gcs_bucket_name']}/{config['processed_data_path_template']}/transformed_data.parquet"
  kwargs['ti'].xcom_push(key = 'transformed_data_path', value = transformed_data_path)
  logging.info(f"Data transformed and notionally stored at: {transformed_data_path}")
  logging.info("Data transformation complete.")

def _load_data_to_target(**kwargs):
  """
  Placeholder function for loading transformed data into a target system.
  Replace with actual data loading logic (e.g., writingto BigQuery, Snowflake).
  """
  transformed_data_path = kwargs['ti'].xcom_pull(key = 'transformed_data_path', task_ids = 'transform_data_task')
  target_dataset = kwargs["params"].get("target_dataset", config["target_dataset_name"])
  target_table = kwargs["params"].get("target_table", f"{config['target_table_prefix']}{config['source_system_name']}_daily")
  logging.info(f"Starting data load from {transformed_data_path} to {target_dataset}.{target_table}...")

  # Example: Simulate data loading
  # In a real scenario, you'd use a BigQueryLoadOperator, PostgreOperator, etc.
  # from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
  # load_job = GCSToBigQueryOperator(
  #   task_id = 'gcs_to_bigquery_load',
  #   bucket = config['gcs_bucket_name'],
  #   source_objects = [transformed_data_path.split(f"gs://{config['gcs_bucket_name']}/")[1]],
  #   destination_project_dataset_table = f"{target_dataset}.{target_table}",
  #   source_format = 'PARQUET',
  #   create_disposition = 'CREATE_IF_NEEDED',
  #   write_disposition = 'WRITE_TRUNCATE', # Overwrite table daily
  #   dag = dag,
  # )
  # load_job.execute(context = kwargs) # This would run the load job

  logging.info(f"Data successfully loaded to {target_dataset}.{target_table}.")
  logging.info("Data loading complete.")

def _send_failure_notification(**context):
  """
  Callback function to send an email notification upon task failure.
  Can be extended to send Slack messages or other alerts.
  """
  task_instance = context.get('task_instance')
  dag_id = task_instance.dag_id
  task_id = task_instance.task_id
  execution_date = context.get('ds')
  log_url = task_instance.log_url

  subject = f"Airflow DAG Failure: {dag_id} - Task: {task_id}"
  html_content = f"""
  <html>
  <body>
    <h3>Airflow Task Failed</h3>
    <p><strong>DAG:</strong> {dag_id}</p>
    <p><strong>Task:</strong> {execution_date}</p>
    <p>Please check the logs for more details: <a href = "{log_url}">Task Log Link</a></p>
  </body>
  </html>
  """
  logging.error(f"Sending failure email for {dag_id}.{task_id}...")
  try:
    send_email(to = config["email_on_failure"], subject = subject, html_content = html_content)
    logging.info("Failure email sent.")
  except Exception as e:
    logging.error(f"Error sending email: {e}")

  # Optional: Send Slack notification
  # if config.get("slack_webhook_url"):
  #   from airflow.providers.slack.operators.slack_webhook import SlackWebHookOperator
  #   slack_message = f"DAG: *{dag_id}*, Task: *{task_id}* failed on {execution_date}. <{log_url}|View Logs>"
  #   slack_notification = SlackWebHookOperator(
  #     task_id = 'slack_notification',
  #     slack_webhook_conn_id = 'slack_connection', # Ensure this Airflow connection exists
  #     message = slack_message,
  #     # http_conn_id = 'slack_connection_http', # Alternative if using http_conn_id
  #     # webhook_token = config["slack_webhook_url"], # Or pass directly
  #     dag = context['dag'], # Pass the DAG object from context
  #   )
  #   try:
  #     slack_notification.execute(context = context)
  #     logging.info("Slack notification sent.")
  #   except Exception as e:
  #     logging.error(f"Error sending Slack notification: {e}")

  # --- DAG Definition ---
  # Define the DAG object with its properties.
  with DAG(
    dag_id = "etl_workflow_template",
    start_date = pendulum.datetime(2023, 1, 1, tz="EST"),
    schedule = None, # set your desired schedule (e.g., "@daily", "0 0 * * *", timedelta(days=1))
                     # None means manual trigger, Use timedelta for periodic execution.
    catchup = False, # If true, backfills missing runs from start_date to current date.
    tags = ["etl", "template", "data_pipeline"],
    default_args = {
      "owner": "airflow",
      "depends_on_past": False,
      "email_on_retry": False,
      "retries": 1, # Number of times to retry a task if it fails
      "retry_delay": pendulum.duration(minutes=5), # Delay between retries
      "on_failure_callback": _send_failure_notification, # Function to call on task failure
  )
