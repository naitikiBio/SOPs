# Connect SAS v9.4 to BigQuery using ODBC

## 1. Background and Google Cloud Platform Setup

### 1.1 Optional, but recommended to test successful BigQuery connection without manipulating your main dataset

1. Log in to Google Cloud Console: Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Create a new Project (if needed): From the project dropdown at the top, click “New Project.” Give it a name (e.g., `sas-bq-test`) and create it.
3. Navigate to BigQuery: In the left-hand navigation pane, search for “BigQuery” or go to `Analytics > BigQuery`.
4. Create a Dataset:
    1. In the BigQuery console, click on your project name in the left pane.
    2. Click “CREATE DATASET”.
    3. Name it (e.g., `demo_dataset`). Choose a data location and optionally set a default table expiration. Click “CREATE DATASET”.
    
    To follow the above steps in a more visual way, see this video:
    
    [https://youtu.be/H0WLpVu5P_Q](https://youtu.be/H0WLpVu5P_Q)