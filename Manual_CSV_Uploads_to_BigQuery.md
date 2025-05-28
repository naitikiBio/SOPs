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
```
