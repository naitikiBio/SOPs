### Manual CSV Uploads to BigQuery
Version 1.0
Effective Date: 5/28/2025
Author: Naitik Shah

#### 1. Purpose
This Standard Operating Procedure (SOP) outlines the steps for manually uploading Comma-Seperated Values (CSV) files to Google BigQuery. It covers schema definition, uploading via the Google Cloud Platform (GCP) Console, programmatic ingestion using Pythonlibraries (pandas-gbq and google-cloud-bigquery), and common error resolution. 

------------


#### 2. Scope
This SOP applies to all personnel involved in uploading CSV data to BigQuery, including data analysts, data engineers, and other relevant stakeholders.

------------


#### 3. Prerequisites
- A valid Google Cloud Platform (GCP) account with necessary permissions for BigQuery (e.g,. BigQuery Data Editor, BigQuery Job User) and also the necessary project where the CSV is to be uploaded

- A CSV file

- For Python-based ingestion:
	- Python installed (version 3.11 or higher recommended).
		 - For assistance in Python download and install, refer: https://github.com/naitikiBio/SOPs/blob/main/Ingesting_Data_From_APIs.md
		 - This SOP is written using Python 3.11, if unable to download from python.org, find the source file in this GitHub repository
	- The pandas, pandas-gbq, and google-cloud-bigquery libraries installed.
		 - To install the above libraries
		  1. **Open Terminal/Command Prompt**: Make sure your Python environment is active (especially if using virtual environments).
		  2. Run `python3 -m pip install pandas-gbq google-cloud-bigquery`

	- Google Cloud SDK configured for authentication, or a service account key with appropriate permissions.

------------

#### 4. Procedures
**4.1. Schema definition in BigQuery**
Defining a schema upfront ensures data integrity and proper type handling.

**4.1.1. Auto-detect Schema (Recommended for initial exploration or simple CSVs):**
1.  **Navigate to GCP Console**:  https://console.cloud.google.com/ 
2.  **Select the project you want to upload your CSV to**: Right besides Google Cloud on the top left, you would either have select project or your project's id, make sure you select the correct project
3.  **Open BigQuery** (Make sure you have access to BigQuery enabled)
4. **Click the toggle button right besides the project name and select the datatset where you want to upload your CSV**: Click the three vertical dots besides the dataset to open up menu. Note: If you don't have a dataset, create one by clicking the three vertical dots besides the project name
5. **Create Table**: In the menu, click "Create Table"
6. **Source**: 
	 - **Create table from**: Select "Upload".
	 - **Select file**: Browse and select your CSV file.
	 - **File format**: Select "CSV".
7. **Destination**:
	 -  **Project name**: Pre-filled.
	 - **Dataset name**: Pre-filled.
	 - **Table name**: Enter a descriptive name for your new table.
	 - **Table type**: Select "Native table".
8. **Schema**:
	- Enable **"Auto detect schema and input parameters"**.
	- BigQuery will attempt to infer the schema (column names and data types) from the CSV header and a sample of rows.
9.  **Advanced Options (Optional but Recommended)**:
	 - **Header rows to skip**: Enter 1 if your CSV has a header row (this is typical).
	 - **Field delimiter**: Usually "Comma".
	 - **Allow jagged rows**: If rows can have a varying number of columns.
	 - **Allow quoted newlines**: If fields can contain newline characters within quotes.
	 - **Null marker**: Specify how NULL values are represented in your CSV (e.g., \N, empty string).
10. **Create**: Click "Create table".

Review this video for visual representation of the above steps
https://youtu.be/HhS6Gn0Rg-0

**4.1.2. Manual Schema Definition (Recommended for production, complex CSVs, or when auto-detect is insufficient)**:
1.  **Follow steps 1-7 from 4.1.1.**
2.  **Schema**:
	 - Disable "Auto detect schema and input parameters".
	 - You can define the schema in three ways:
	 	 -  **Edit as text**: Provide the schema as a JSON array.
		 	 - Example:
       			```JSON
			 	[
					{"name": "column_name1", "type": "STRING", "mode": "NULLABLE"},
					{"name": "column_name2", "type": "INTEGER", "mode": "NULLABLE"},
					{"name": "column_name3", "type": "FLOAT", "mode": "NULLABLE"},
					{"name": "column_name4", "type": "DATE", "mode": "NULLABLE"},
					{"name": "column_name5", "type": "BOOLEAN", "mode": "NULLABLE"}
				]
    			```
		- **Common Types**: STRING, BYTES, INTEGER (or INT64), FLOAT (or FLOAT64), NUMERIC, BIGNUMERIC, BOOLEAN (or BOOL), TIMESTAMP, DATE, TIME, DATETIME, GEOGRAPHY, JSON.
		- **Modes**:
			- NULLABLE: The column allows NULL values (most common).
			- REQUIRED: The column does not allow NULL values.
			- REPEATED: The column contains an array of values of the specified type.
	 - **Add field (+)**: Use the UI to add each filed one by one, specifying its Name, Type, Mode, and optionally a Description.
	 - **Upload schema file**: If you have a JSON schema file, you can upload it.
3.  **Advanced Options**: Configure as described in 4.1.1., step 9
4. **Create Table**: Click "Create table".

**4.2. Using Python for Ingestion**
This method is suitable for automated workflows, larger files (though direct GCS to BigQuery is better for very large files), or when preprocessing with Pandas is needed.

**4.2.1. Using pandas-gbq**

This library provides a high-level interface for interacting with BigQuery through Pandas DataFrames.
1.  **Installation**:
	Install the required dependencies if not (refer to the start of this SOP)
2.  **Python Script**:
	```python
	import pandas as pd
	from pandas_gbq import to_gbq, read_gbq

 	# --- Configuration ---
 	# Additionally you can replace all this using .env
 	project_id = "your-gcp-project-id"
 	dataset_id = "your_table_id"
 	table_id = "your_tbale_id"
 	csv_file_path = "path/to/your/file.csv

 	# Optionally, you can define what to do if the table already exists
 	# 'fail': If table exists, do nothing.
 	# 'replace': If table exists, drop it, recreate it, and insert data.
 	# 'append': If table exists, insert data. Create if does not exist.
 	if_exists_strategy = 'append' # or select from the above list

 	# --- Load CSV into Pandas Dataframe ---
 	try:
 		df = pd.read_csv(csv_file_path)
 		print(f"Succesfully loaded CSV '{csv_file_path}' into DataFrame.")
 		print("DataFrame info:")
 		df.info()
 		print("\nFirst 5 rows:")
 		print(df.head())
 	except FileNotFoundError:
 		print(f"Error: CSV file not found at '{csv_file_path}'")
 		exit()
 	except pd.errors.EmptyDataError:
 		print(f"Error: CSV file '{csv_file_path}' is empty.")
 		exit()
 	except Exception as e:
 		print(f"Error reading CSV file '{csv_file_path}': {e}")
 		exit()

 	# --- Define Table Schema (Optional but Recommended for `pandas-bgq` for explicit control) ---
 	# pandas-bgq can infer schema, but explicit definition is safer.
 	# The schema should be a list of dictionaries, matching BigQuery's schema format.
 	# Comment this code out if not defining schema explicitly
 	table_schema = [
 		{'name': 'column_name1', 'type': 'STRING'},
 		{'name': 'column_name2', 'type': 'INTEGER'},
 		# Add all your columns here
	]

 	# --- Checking Datatypes ---
 	# Make sure pandas assigned the correct datatypes to your dataset columns, for that run `df.dtypes()` where df is the DataFrame name you gave when reading
 	# To convert any columnn datatype
 	df['date_column'] = pd.to_datetime(df['date_column']) # Example type conversion

 	# --- Upload DataFrame to BigQuery ---
 	full_table_id = f"{dataset_id}.{table_id}"
 	try:
 		print(f"\nUploading DataFrame to BigQuery table: {project_id}.{full_table_id} with strategy: {if_exists_strategy}")
 		to_gbq(
 			dataframe = df,
 			destination_table = full_table_id,
 			project_id = project_id,
 			if_exists = if_exists_strategy,
 			table_schema = table_schema # Comment this out if you are not explicitly defining schema
 		)
 		print(f"Succesfully uploaded data to {full_table_id}.")

 	except Exception as e:
 		print(f"Error uploading data to BigQuery: {e}")

 	# --- Optionally to verify your data ---
 	try:
 		query = f"SELECT * FROM `{project_id}.{full_table_id}' LIMIT 5"
 		df_from_bgq = read_bgq(query, project_id = project_id)
 		print("\nFirst 5 rows from BugQuery table:")
 		print(df_from_gbq)
 	except Exception as e:
 		print(f"Error reading data back from BigQuery: {e}")
	```
 	

 4. **Run the script**: Save the above script and then execute `python your_script_name.py` in your terminal (make sure you are in the directory in the terminal where your script is saved)

**4.3.2. Using google-cloud-bigquery**

This library provides more granular control over BigQuery operations.
1. **Installation (if not already installed)**:
Install the required dependencies if not (refer to the start of this SOP)

2. **Authentication**:
Same as for pandas-gbq

3. **Python Script**:
	```python
 	import pandas as pd
 	from google.cloud import bigquery
 	from google.oauth2 import service_account # if using service key

 	# --- Configuration ---
 	project_id = "your-gcp-project-id"
 	dataset_id = "your_dataset_id"
 	table_id = "your_table_id"
 	csv_file_path = "path/to/your/file.csv"
 	# Optional: Path to your service account key JSON file
 	# service_account_key_path = "path/to/your-service-account-key.json"

 	# --- Initialize BigQuery Client ---
 	try:
		# Using either one of these, comment the other one, so if using service account key, comment the ADC lines and vice versa
 		# If using a service account key:
 		# credentials = service_account.Credentials.from_service_account_file(service_account_key_path)
 		# client = bigquery.Client(credentials = credentials, project = project_id)

 		# If using Application Default Credentials (ADC):
 		client = bigquery.Client(project = project_id)
 		print("BigQuery client initialized succesfully.")
 	except Exception as e:
 		print(f"Error initializing BigQuery client: {e}")
 		exit()

 	# --- Define Table Schema (Required if table doesn't exist or if you want to ensure schema) ---
 	schema = [
		bigquery.SchemaField("column_name1", "STRING", mode = "NULLABLE"),
 		bigquery.SchemaField("column_name2", "INTEGER", mode = "NULLABLE"),
 		bigquery.SchemaField("column_name3", "FLOAT", mode = "NULLABLE"),
 		bigquery.SchemaField("column_name4", "DATE", mode = "NULLABLE") # Ensure CSV data is 'YYYY-MM-DD'
 		# Add all your columns here, matching the CSV header and desired BQ types 
 	]

 	# --- Construct Table Reference ---
 	table_ref = client.dataset(dataset_id).table(table_id)
 	full_table_id_str = f"{project_id}.{dataset_id}.{table_id}"

 	# --- Configure Load Job ---
 	job_config = bigquery.LoadJobConfig()
 	job_config.source_format = bigquery.SourceFormat.CSV
 	job_config.skip_leading_rows = 1 # Skip the header row
 	job_config.autodetect = False # Set to True if you want BigQuery to auto detect schema, but explicit schema is better
 	job_config.schema = schema # Use the explicitly defined schema
 	job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND # Or WRITE_TRUNCATE, WRITE_EMPTY

 	# Optional variables
 	# job_config.null_marker = "\\N" # If NULLS are represented as \N
 	# job_config.allow_jagged_rows = True # Optional Allow missing trailing optional columns
 	# job_config.allow_quoted_newlines = True # Optional Allow quoted data containing newline characters (CSV only)

 	# --- Load Data from CSV file ---
 	try:
 		with open(csv_file_path, "rb") as source_file:
 			print(f"\nStarting load job for '{csv_file_path}' into BigQuery table: {full_table_id_str}")
 			load_job = client.load_table_from_file(
 				source_file,
 				table_ref,
 				job_config = job_config
 			)
 			print(f"Load job {load_job.job-id} submitted.")
 			load_job.result() # Waits for the job to complete
 			print(f"Load job completed. Loaded {load_job.output_rows} rows to {full_table_id_str}.")
 	except FileNotFoundError:
 		print(f"Error: CSV file not found at '{csv_file_path}'")
 	except Exception as e:
 		print(f"Error during BigQuery load job: {e}")
 		if hasattr(e, 'errors') and e.errors:
 			for error in e.errors:
 				print(f" -Reason: {error.get('reason')}, Location: {error.get('location')}, Message: {error.get('message')}")

 	# --- (Optional) Verify by Querying data ---
 	try:
 		query = f"SELECT * FROM `{full_table_id_str}` LIMIT 5"
 		query_job = client.query(query)
 		results = query_job.results() # Waits for the job to complete
 		print("\nFirst 5 rows from BigQuery table:")
 		for row in results:
 			print(row)
 		except Exception as e:
 			print(f"Error querying data from BigQuery: {e}")
 
4. **Run the script**: Save the above script, ensuring `.py` extension and then execute by running `python your_script_name.py` in the terminal (Make sure you have navigated to the file directory in the terminal before executing the above command.
