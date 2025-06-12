# Connect SAS v9.4 to BigQuery using ODBC

Version: 1.0

Effective Date: 6/12/2025

Author: Naitik Shah

## 1. Background and Google Cloud Platform Setup

### 1.1 Optional, but recommended to test successful BigQuery connection without manipulating your main dataset

1. Log in to Google Cloud Console: Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Create a new Project (if needed): From the project dropdown at the top, click “New Project.” Give it a name (e.g., `sas-bq-test`) and create it.
3. Navigate to BigQuery: In the left-hand navigation pane, search for “BigQuery” or go to `Analytics > BigQuery`.
4. Create a Dataset:
    - In the BigQuery console, click on your project name in the left pane.
    - Click “CREATE DATASET”.
    - Name it (e.g., `demo_dataset`). Choose a data location and optionally set a default table expiration. Click “CREATE DATASET”.
        
        To follow the above steps in a more visual way, see this video:
        
        [https://youtu.be/H0WLpVu5P_Q](https://youtu.be/H0WLpVu5P_Q)
        
5. **Create a Sample Table:**
    - Click on your newly created `demo_dataset`.
    - Click “CREATE TABLE”.
    - Select “Empty table” as the source.
    - Name the table (e.g., `sample_table`).
    - Define a simple schema (e.g., `id` (INTEGER), `name` (STRING), `value` (NUMERIC)).
    - Click “CREATE TABLE”.
        
        To visually follow the steps, check this video:
        
        [https://youtu.be/BeWg0zwEcl4](https://youtu.be/BeWg0zwEcl4)
        
6. **Insert Sample Data (Optional but Recommended):**
    - Click on your `sample_table`.
    - Click “DETAILS” then “QUERY”.
    - Run an `INSERT` statement:
        
        ```sql
        INSERT INTO 'your_project_id.demo_dataset.sample_table' (id, name, value)
        VALUES
        	(1, 'Alpha', 10.5)
        	(2, 'Beta', 20.0)
        	(3, 'Gamma', 15.2);
        ```
        
        Replace `your_project_id` with your actual GCP project ID.
        
        For more visual way to follow, check out this video:
        
        [https://www.youtube.com/watch?v=EH0KkkAjzy4](https://www.youtube.com/watch?v=EH0KkkAjzy4)
        
    
    ### 1.2 Enable BigQuery API and Download ODBC Driver
    
    1. **Enable BigQuery API:**
        - In the Google Cloud Console, navigate to `APIs & Services > Dashboard`.
        - Click “+ ENABLE APIS AND SERVICES”.
        - Search for “BigQuery API” and enable it.
            
            Video to follow:
            
            [https://youtu.be/a-hQTmfWyNE](https://youtu.be/a-hQTmfWyNE)
            
    2. **Download BigQuery ODBC Driver:**
        - Search online for “Simba BigQuery ODBC Driver” or “CData BigQuery ODBC Driver”. (For this guide, I will be setting up Simba)
        - Visit the official vendor website and download the driver compatible with your operating system (Windows/Linux) and the bitness of your SAS v9.4 installation (32-bit or 64-bit).
            
            Official Link: [ODBC and JDBC drivers for BigQuery  |  Google Cloud](https://cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers)
            
    
    ### Generate a Service Account Key for Authentication (Recommended for Automation)
    
    While user-based OAuth is common for intitial setup, service accounts are preferred for production and automated processes.
    
    1. **Navigate to IAM & Admin:** In the Google Cloud Console, go to `IAM & Admin > Service Accounts`.
    2. **Create a Service Account:**
        - Click “+CREATE SERVICE ACCOUNT”.
        - Provide a Service account name (e.g., `sas-bigquery-connector`).
        - Click “CREATE AND CONTINUE”.
    3. **Grant Permissions:** In the “Grant this service account access to project” step, grant it the necessary BigQuery roles. For read-only access to tables, consider:
        - `BigQuery Data Viewer`
        - `BigQuery Read Session User`
        - Click “CONTINUE” and then “DONE”.
    4. **Generate a Key:**
        - Back in the “Service Accounts” list, click on the newly created service account.
        - Go to the “KEYS” tab.
        - Click “ADD KEY” > “Create new key”.
        - Select “JSON” as the key type and click “CREATE”.
        - A JSON key file will be downloaded to your computer. **Store the file securely.** This file contains credentials for the service account.
    
    For more visual guide, check this video:
    
    [https://youtu.be/vpYLirCR7-4](https://youtu.be/vpYLirCR7-4)
    

## 2. Local Prototyping

### 2.1. Install BigQuery ODBC Driver

1. **Windows:** Run the downloaded installer(`.msi` file). Follow the on-screen prompts.
2. **Linux:** 
    - Extract the downloaded archive (e.g., `.tar.gz` ).
    - Follow the installation instructions in the driver’s documentation, which usually involves copying files and setting environment variables like `LD_LIBRARY_PATH`.

### 2.2. Configure a DSN Connection

This step registers the BigQuery ODBC driver with your operating system, creating a Data Source Name (DSN) that SAS can use.

**Windows DSN Configuration:**

1. Open the **ODBC Data Source Administrator** (e.g., search “ODBC” in Windows, then select `ODBC Data Sources (64-bit)`  or `32-bit`  based on your SAS installation).
2. Go to the **System DSN** tab.
3. Click **Add…**
4. Select the **Simba ODBC Driver for Google BigQuery** (or your chosen driver) from the list and click **Finish**.
5. In the driver configuration window (this will vary slightly by driver, but common fields include):
    - **Data Source Name (DSN):** Enter `BigQueryDSN`  (or a name of your choice).
    - **Project ID:** Enter your GCP project ID.
    - **Dataset ID:** Enter `demo_dataset`.
    - **Authentication:**
        - If using **OAuth User Authentication**: Follow the prompt to “Sign in with Google.” A browser window will open for authentication. once authorized, a refresh token will be automatically retrieved, or you’ll be prompted to copy/paste it. Ensure `Save Token` is selected.
        - If using **Service Account Authentication**: Select `Service Account` as the authentication mechanism. Provide the full path t your downloaded JSON key file in the `KeyFilePath` field.
    - Click **Test Connection** to verify connectivity.
    - Click **OK** to save the DSN.

**Linux DSN Configuration (Edit** `odbc.ini` ):

1. Open your `odbc.ini`  file using a text editor (e.g., `sudo nano /etc/odbc.ini` ).
2. Add the following entry. Adjust paths and details for your specific driver and setup:
    
    ```bash
    [BigQueryDSN]
    Driver = /opt/simba/googlebigqueryodbc/lib/64/libgooglebigqueryodbc_sb64.so  ; Adjust path as needed
    Description = Google BigQuery via Simba ODBC
    Catalog = your_google_cloud_project_id
    DataSetId = demo_dataset
    # For OAuth User Authentication (requires initial generation via driver's utility):
    # OAuthMechanism = 0
    # RefreshToken = <your_generated_refresh_token>
    # For Service Account Authentication:
    OAuthMechanism = 1
    ServiceAccountEmail = sas-bigquery-connector@your-project-id.iam.gserviceaccount.com
    KeyFilePath = /path/to/your/service-account-key.json
    SQLDialect = 1 ; (1 for Standard SQL, 0 for Legacy SQL)
    ```
    
3. Ensure your `~/.bashrc`  or system-wide environment variables (`/etc/profile.d/`) include:
    
    ```bash
    export ODBCINI=/etc/odbc.ini
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/simba/googlebigqueryodbc/lib/64 ; Adjust path
    ```
    
    Then run `source ~/.bashrc` or reboot.
    

### 2.3. Draft Sample SAS Code

Below is a sample SAS code to connect to BigQuery. This assumes your DSN is named `BigQueryDSN`  and your dummy dataset is `demo_dataset` containing `sample_table` .

```bash
* Define a SAS LIBNAME statement to connect to BigQuery via ODBC;
* 'BigQueryDSN' should match the DSN name configured in your ODBC Data Source Administrator;
* 'schema=' specifies the BigQuery dataset to access (e.g., 'demo_dataset');
* 'user=' and 'password=' might be optional if your DSN handles authentication (e.g., OAuth);
* For service account authentication, you typically don't specify user/password in LIBNAME,
* as the DSN points to the key file;

LIBNAME bq ODBCA
    DATASRC='BigQueryDSN'
    SCHEMA='demo_dataset'
    ; /* Remove ODBCA if not using explicit authentication options in LIBNAME */

* If your ODBC driver requires user/password for the LIBNAME statement
* (less common with BigQuery's OAuth/Service Account methods, but possible with some drivers):
* LIBNAME bq ODBC
* DATASRC='BigQueryDSN'
* USER='your_google_username'          * Placeholder: Your Google account email;
* PASSWORD='your_google_password'      * Placeholder: Your Google account password or OAuth token;
* SCHEMA='demo_dataset'
* ;

* Use PROC SQL to query the BigQuery table;
* The syntax is 'libref.tablename' (e.g., bq.sample_table);
PROC SQL;
    CREATE TABLE work.bigquery_data AS
    SELECT *
    FROM bq.sample_table;

    * Optionally, display the data;
    SELECT * FROM work.bigquery_data;
QUIT;

* You can also use PROC PRINT to view the data directly from the LIBNAME;
PROC PRINT DATA=bq.sample_table;
    TITLE "Data from BigQuery Sample Table";
RUN;

* Clear the LIBNAME connection when done;
LIBNAME bq CLEAR;
```

### Troubleshooting and FAQ Section

| Problem | Possible Cause | Resolution |
| --- | --- | --- |
| `ERROR: CLI error trying to establish connection: [Simba][BigQuery] (100) Error interacting with REST API Timeout was reached.`  | Firewall blocking access to BigQuery API endpoints (`bigquery.googleapis.com`). Incorrect proxy settings in DSN configuration. Slow network connection or large query timeout setting too low. | Verify your firewall allows outbound HTTPS (port 443) traffic to `bigquery.googleapis.com` . If using a proxy, ensure proxy details are correctly configured in your ODBC DSN settings. Increase the `Timeout`  property in your ODBC DSN’s advanced settings (consult driver documentation). |
| `ERROR: Authentication failed.` | Incorrect Google account or service account credentials in DSN. Expired OAuth refresh token. Insufficient IAM permissions for the account. JSON key file path for service account is incorrect or file is corrupted/inaccessible. | Re-authenticate through the ODBC Data Source Administrator (for OAuth). Verify the Service Account Email and KeyFilePath in the DSN configuration.In GCP IAM, ensure the connecting account has at least `BigQuery Data Viewer` and `BigQuery Read Session User` roles on the relevant project/dataset. Ensure the JSON key file is readable by the user running SAS.|
| `ERROR: Table not found` or `Dataset not found`. | Typo in table name or dataset name in SAS `LIBNAME` or `PROC SQL`.Incorrect `SCHEMA` option in `LIBNAME` statement. Table/Dataset does not exist or has been deleted. | Double-check the spelling of the dataset (schema) and table names in your SAS code and DSN. BigQuery names are case-sensitive. Verify the table and dataset exist in the BigQuery console. Ensure the `SCHEMA` option in `LIBNAME` correctly points to the BigQuery dataset ID. |
| `ERROR: [ODBC Driver] ... Driver Manager cannot load …` | ODBC driver not installed correctly. Driver bitness (32-bit/64-bit) mismatch with SAS. Missing or incorrect `LD_LIBRARY_PATH` (Linux). | Reinstall the ODBC driver, ensuring it matches your SAS version's bitness. On Linux, verify `LD_LIBRARY_PATH` includes the directory containing the ODBC driver's `.so` files and that `odbc.ini` points to the correct driver path. |
| **FAQ: Do I need SAS/ACCESS Interface to BigQuery?** | SAS does offer a specific SAS/ACCESS Interface to Google BigQuery. While the ODBC method works, the native SAS/ACCESS interface might offer optimized performance and additional features specifically for BigQuery, leveraging its unique capabilities more directly than a generic ODBC connection. For production use, evaluating the native SAS/ACCESS product might be beneficial. | For this SOP, we are focusing on the generic ODBC method, which requires SAS/ACCESS Interface to ODBC. If you have the native SAS/ACCESS Interface to BigQuery, consult its documentation for alternative connection methods that might be more performant or feature-rich. |
| **FAQ: Why use a Service Account vs. my Google Account?** | Service accounts are better for automated processes and provide a more secure, auditable, and manageable way to control access to GCP resources from applications like SAS, without relying on individual user credentials. | For local prototyping, your Google Account via OAuth is often simpler. For production, transition to a dedicated service account with granular permissions. |
