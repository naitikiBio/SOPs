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
