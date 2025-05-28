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
[![YouTube](https://youtu.be/HhS6Gn0Rg-0 "YouTube")](https://youtu.be/HhS6Gn0Rg-0 "YouTube")

Review this video for visual representation of the above steps
https://youtu.be/HhS6Gn0Rg-0
