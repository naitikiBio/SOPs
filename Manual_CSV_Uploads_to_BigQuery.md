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
2. **Authentication**: Ensure you are authenticated, if not follow either of these methods
   - **Method 1**: `gcloud auth application-default login`
     1. Install Google Cloud CLI (`gcloud`) on your system by following these steps: https://cloud.google.com/sdk/docs/install#windows (Ensure you are following the steps for your OS)
     2. Open your terminal or command prompt and run the following command:
        ```bash
        gcloud auth application-default login
        ```
     3. Browser-based authentication: This command will typically open a web browser and redirect you to a Google sign-in page.
     4. Sign in with your Google account: Choose the Google account you want to use for accessing your Google Cloud resources. This account should have the necessary permissions for the tasks you intend to perform.
     5. Grant access to the Google Cloud CLI: You will be asked to grant the Google Cloud CLI permission to access your Google account. Review the requested permissions and click "Allow" if you agree.
     6. Credentials stored locally: Once you've succesffuly signed in and granted access, the Google Cloud CLI will download and store your authentication credentials on your local machine. The location of this file depends on your operating system:
        - Linux/macOS: `~/.config/gcloud/application_default_credentials.json`
        - Windows: `%APPDATA%\gcloud\application_default_credentials.json`
     7. Verification (optional): You can verify that the credentials have been set by running the following command:
        ```bash
        gcloud auth application-default print-access-token
        ```
        This command should output a long string, which is your access token.
     - When to use it:
       	- Local development and testing: This is the most common way to authenticate when you are running code on your local machine that needs to access Google Cloud.
       	- One-time setup: You typically only need to run this command once unless your credentials expire or you want to use a different Google account.

   - **Method 2**: Setting the `GOOGLE_APPLICATION_CREDENTIALS` environment variable
     This method explicitly tells your application where to find the service account key file. Service accounts are non-human accounts that applications can use to authenticate. This method is particularly useful in production environments or when you want to use a specific service account for authentication.
     **Step-by-Step Explanation**:
     1. **Create a service account (if you haven't already)**:
        - Go to the Google Cloud Console
        - Navigate to IAM & Admin > Service accounts.
        - Click + CREATE SERVICE ACCOUNT.
        - Enter a service account name, ID, and description (optional).
        - Click CREATE AND CONTINUE.
        - Grant the service account the necessary roles for the resources it needs to access.
        - Click CONTINUE.
        - Click CREATE KEY.
        - Choose JSON as the Key type.
        - Click CREATE. This will download a JSON file containing your service account's private key to your local machine. Keep this file secure.
     2. **Identify the path to your service account key file**: Note the exact location where you saved the downloaded JSON key file. For example: `/path/to/your/service-account-key.json`.
     3. **Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable**:
        - **Linux/macOS**:
          ```bash
          export GOOGLE_APPLICATION_CREDENTIALS = "/path/to/your/service-account-key.json"
          ```
          Replace `/path/to/your/service-account-key.json` with the actual path to your key file. This setting is usually temporary for the current terminal session. To make it permanent, you can add this line to your shell's configuration file (e.g., `~/.bashrc`, `~/.zshrc`).
        - **Windows (Command Prompt)**:
          ```bash
          set GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\your\service-account-key.json"
          ```
          Replace `C:\path\to\your\service-account-key.json` with the actual path. This is also typically temporary. To make it permanent, you can use the `setx` command:
          ```bash
          setx GOOGLE_APPLICATION_CREDENTIALS "C:\path\to\your\service-account-key.json"
          ```
          Note that changes made with `setx` might require restarting your command prompt or even your system to take effect.
        - **Windows (PowerShell)**:
          ```bash
          $env: GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\your\service-account-key.json"
          ```
          To make it persistent, you can add this line to your PowerShell profile.
    4. **Run your application or `gcloud` commands**: Once the environment variable is set, your application or the `gcloud` CLI will automatically look athe specified path for the service account key file and use it for authentication.

    **When to use it**:
      - **Production environments**: This is a common way to authenticate applications running on virtual machines, containers, or other server environments.
      - **Automated tasks and scripts**: When you need to run scripts or automated processes that interact with Google Cloud without human intervention.
      - **Specific service account permissions**: When your application needs to operate with a defined set of permissions granted to a service account.

    **Important Security Considerations:**
      - **Never store service account key files in your code repository.**
      - **Restrict access to the service account key file on your systems.**
      - **Grant service accounts only the necessary permissions (principle of least privilege).**
      - 
4.  **Python Script**:
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
 	

 5. **Run the script**: Save the above script and then execute `python your_script_name.py` in your terminal (make sure you are in the directory in the terminal where your script is saved)

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

 	```
4. **Run the script**: Save the above script, ensuring `.py` extension and then execute by running `python your_script_name.py` in the terminal (Make sure you have navigated to the file directory in the terminal before executing the above command.

**4.4. Common Errors and Troubleshooting**

**4.4.1.Schema Mismatch**:
- **Error Message (Example)**: "Error while reading data, error message: CSV table encountered too many errors, giving up. Rows: 1; errors: 1. Missing data for column: column_x." or "Provided schema doesn not match Table project:dataset.table. Field field_name has changed type from TYPE_A TO TYPE_B"
- **Cause**:
	- The number of columns in the CSV file foes not match the number of columns in the BigQuery table schema.
 	- The data type of a column in the CSV file in incompatible with the data type defined in the BigQuery schema (e.g., trying to load "abc" into an INTEGER column).
  	- Column order in CSV doesn't match schema if not using header row for mapping.
- **Resolution**:
  1. **Verify CSV Header**: Ensure the CSV header row (if used and skipped) matched the column named and order executed by the schema.
  2. **Check Column Count**: Manually inspect a few rows of the CSV to ensure the correct number of delimiters (commas) per row.
  3. **Review Schema**: Double-check the BigQuery table schema against the CSV structure.
     - Use "Auto detect schema" (4.1.1) on a small samle of the CSV to see how BigQuery interprets it, then compare with your manual schema.
     - For pandas-gbq, ensure DataFrame dtypes are appropriate or provide an explicit table_schema
     - For google-cloud-bigquery, ensure your bigquery.SchemaField definitions are correct.
  4. **Data Cleansing**: Clean the CSV data to correct type inconsistencies before uploading (e.g., remove non-numeric characters from a column intended to be INTEGER). Pandas can be very usefulfor this preprocessing step.
  5. **Adjust skip_leading_rows**: Ensure this is set correctly (usually 1 for a header).
  6. **Consider allow_jagged_rows**: If some rows legitimately have fewer columns, and missing values should be NULL, this option can help (use with caution, as it can mask other issues).
 
  **4.4.2. NULL Handling/Empty Values**:
  - **Error Message (Example)**: "Could not parse" as INT64 for column column_y" or issues with REQUIRED fields.
  - **Cause**:
    - Empty strings ("") in the CSV are being interpreted as values that cannot be cast to the trget data type (e.g., an empty string for an INTEGER column).
    - A REQUIRED (NOT NULL) column in BigQuery is receiving a NULL or empty value from the CSV.
  - **Resolution**:
    1. **Specify null_maker**: If your CSV uses a specific string to represent NULLs (e.g., \N, NULL, NA), specify this in the "Null marker" field (GCP Console) or job_config.null_marker (Python google-cloud-bigquery). pandas-gpq handles Pandas NaN values correctly as NULLs.
    2. **Preprocessing with Pandas**:
       - Replace empty strings or custom NULL representations with numpy.nan before uploading with pandas-gbq, as NaN is translated to NULL be BigQuery.
       - ```python
         import numpy as np
         df.replace(", np.nan, inpace = True) # Replace empty strings with NaN
         df.replace('NA', np.nan, inplace = True) # Replace 'NA' strings with NaN
         ```
       - Ensure columns intended for numeric types do not contain empty strings if those should be NULL.
    3. **Schema Mode**: If a column can legitimately contain NULLs, ensure its mode is NULLABLE in the BigQuery schema. If it's REQUIRED, you must provide a valid, non-null value in the CSV or preprocess it.
    4. **Default Values**: For REQUIRED fields, if appropriate, consider transforming empty/null CSV values to a default value during preprocessing before loading.

**4.4.3. Encoding Issues**:
- **Error Message (Example)**: "Error while reading data, error message: CSV table encountered too many errors, giving up. Rows: 1; errors: 1. Error detected while parsing row starting at position: X. Error: UTF-8 decoding error."
- **Cause**: The CSV file is not encoded in UTF-8, which is the default expected by BigQuery.
- **Resolution**:
  1. **Convert CSV to UTF-8**: Before uploading, convert your CSV file to UTF-8 encoding. You can use text editors (like VS Code, Notepad++ "Convert to UTF-8") or command-line tools (like iconv).
  2. **Specify Encoding (Python)**:
     - When reading with Pandas: `pd.read_csv(csv_file_path, encoding = 'your-actual-encoding')` then save it as UTF-8 before passing to BigQuery, or let pandas-gbq handle it if the DataFrame is correctly loaded.
     - google-cloud-bigquery: The LoadJobConfig has an eocnding property (e.g., job_config.encoding = "UTF-8: or other encodings like ISO-8859-1 if absolutely necessary, though UTF-8 is strongly preferred).

**4.4.4. Quoting and Delimiter Issues**:
- **Error Message (Example)**: "Too many values in row X." or fields being incorrectly split or merged.
- **Cause**:
  - Fields containing the delimiter (e.g., a comma withing a text field) are not properly quoted.
  - Fields containing newline characters are not properly quoted and allow_quoted_newlines is not enabled.
  - Incorrect field delimiter specified.
- **Resolution**:
  - **Ensure Proper Quoting**: Fields containing the delimiter, quotes, or newlines should be enclosed in double quotes (e.g., "this, field, has, commas"). Double quotes within a quoted field should be escaped (usually by another double quote, e.g., "He said ""Hello"".").
  - **Set allowed_quoted_newlines**: If your CSV data has newlines within quoted fields, enable this option in the GCP console or set `job_config.allow_quoted_newlines = True` in Python.
  - **Verify Field Delimiter**: Ensure the correct delimiter is specified (usually comma, but could be tab, pipe, etc.).
 
------------


#### 5. Revision History
| Version  | Date  | Author  | Changes  |
| ------------ | ------------ | ------------ | ------------ |
| 1.0  | 29th May 2025  | Naitik Shah  | Initial Draft  |
