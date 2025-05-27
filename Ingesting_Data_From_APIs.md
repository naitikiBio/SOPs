# Ingesting Data from APIs 📄

This guide provides an overview of how to ingest data from APIs, using the OpenFDA API as an example. It also includes instructions for setting up your Python environment.

---

## Table of Contents

1.  [Getting Started: Python 3.11 Installation](#getting-started-python-311-installation-)
    * [Downloading Python 3.11](#1-downloading-python-311)
    * [Installing Python 3.11](#2-installing-python-311)
    * [Using Pip to Install `requests` and `python-dotenv`](#3-using-pip-to-install-requests-and-python-dotenv-)
2.  [Securing API Keys with `.env` Files](#securing-api-keys-with-env-files-)
3.  [Understanding API Authentication](#understanding-api-authentication-)
    * [API Keys](#1-api-keys)
    * [OAuth 2.0 (Open Authorization)](#2-oauth-20-open-authorization)
    * [Getting an OpenFDA API Key](#getting-an-openfda-api-key-)
4.  [Example: Getting OpenFDA API Data](#example-getting-openfda-api-data-)
    * [OpenFDA Overview](#openfda-overview)
    * [Python Code with `.env` for API Key](#python-code-with-env-for-api-key)
    * [Additional Notes on the Code](#additional-notes-on-the-code)
5.  [Standard Operating Procedures (SOPs) and Pseudocode](#standard-operating-procedures-sops-and-pseudocode-)
    * [SOP: API Authentication](#sop-api-authentication)
    * [SOP: Request/Response Handling](#sop-requestresponse-handling)
    * [SOP: Data Validation and Transformation](#sop-data-validation-and-transformation)
    * [SOP: Simulated Push to BigQuery](#sop-simulated-push-to-bigquery)


## Getting Started: Python 3.11 Installation 🐍

To run the example code and interact with APIs using Python, you'll need Python installed on your system. We recommend using Python 3.11 or a newer version.

### 1. Downloading Python 3.11

* **Official Python Website**: The primary source for downloading Python is the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
* Navigate to the downloads page and find the section for Python 3.11.x.

### 2. Installing Python 3.11

#### For Windows 🪟

1.  **Download**: Download the Windows installer (e.g., `python-3.11.x-amd64.exe`).
2.  **Run Installer**: Double-click the downloaded installer.
3.  **Customize Installation (Recommended)**:
    * **Check "Add Python 3.11 to PATH"**: This is crucial for running Python from the command line easily. If you miss this, you'll have to add it manually later.
    * Select "Customize installation."
    * Ensure "pip" is checked (it usually is by default).
    * Optionally, choose an installation location. The default is usually fine.
4.  **Install**: Click "Install" and wait for the installation to complete.
5.  **Verify Installation**:
    * Open Command Prompt (search for `cmd`) or PowerShell.
    * Type `python --version` and press Enter. You should see `Python 3.11.x`.
    * Type `pip --version` and press Enter. You should see pip's version associated with Python 3.11.

#### For macOS 🍎

1.  **Download**: Download the macOS 64-bit universal installer from the [Python website](https://www.python.org/downloads/mac-osx/).
2.  **Run Installer**: Double-click the downloaded `.pkg` file.
3.  **Follow Instructions**: Follow the on-screen prompts. The installation is straightforward. Python will typically be installed in `/Library/Frameworks/Python.framework/Versions/3.11`. A `python3` alias is usually also placed in `/usr/local/bin/`.
4.  **Verify Installation**:
    * Open Terminal (Applications > Utilities > Terminal).
    * Type `python3 --version` and press Enter. You should see `Python 3.11.x`.
    * Type `pip3 --version` and press Enter.

    **Note using Homebrew (Alternative for macOS):**
    If you have [Homebrew](https://brew.sh/) installed, you can install Python 3.11 by running:
    ```bash
    brew install python@3.11
    ```
    Then, follow the instructions provided by Homebrew regarding PATH setup if needed.

#### For Linux 🐧

Installation methods vary slightly depending on your Linux distribution.

1.  **Check if Python 3.11 is already available**:
    * Open your terminal.
    * Try `python3 --version`. Some distributions might already have a recent version of Python 3.

2.  **Using Package Managers (Recommended)**:

    * **Debian/Ubuntu**:
        ```bash
        sudo apt update
        sudo apt install python3.11 python3.11-venv python3-pip
        ```
        (You might need to add a PPA like `deadsnakes` if `python3.11` isn't in the default repositories: `sudo add-apt-repository ppa:deadsnakes/ppa` followed by `sudo apt update`).

    * **Fedora**:
        ```bash
        sudo dnf install python3.11 python3-pip
        ```

    * **CentOS/RHEL (may require EPEL or compiling from source for specific versions)**:
        Newer RHEL versions (8+) might have `python3.11` available via `dnf`. For older versions, or if you need the exact 3.11.x, you might need to compile from source or use a third-party repository like EPEL.

3.  **Compiling from Source (Advanced)**:
    If `python3.11` is not available through your package manager, you can download the source tarball from the [Python website](https://www.python.org/downloads/source/) and compile it. This is a more involved process.
    ```bash
    # Example steps (dependencies might vary):
    sudo apt-get install -y build-essential libssl-dev zlib1g-dev \
        libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev \
        libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev tk-dev \
        libffi-dev wget

    wget [https://www.python.org/ftp/python/3.11.x/Python-3.11.x.tgz](https://www.python.org/ftp/python/3.11.x/Python-3.11.x.tgz) # Replace x with actual version
    tar -xf Python-3.11.x.tgz
    cd Python-3.11.x
    ./configure --enable-optimizations
    make -j $(nproc) # Uses all available processor cores
    sudo make altinstall # Use altinstall to avoid replacing default python3
    ```

4.  **Verify Installation**:
    * Open Terminal.
    * Type `python3.11 --version` (or `python3 --version` if it's the default Python 3).
    * Type `pip3 --version` or `python3.11 -m pip --version`.

---

### 3. Using Pip to Install `requests` 📦

**Pip** is the package installer for Python. You use pip to install packages from the Python Package Index (PyPI). The `requests` library is a popular HTTP library for making API calls.

1.  **Open Terminal/Command Prompt**: Make sure your Python environment is active (especially if using virtual environments).

2.  **Install `requests`**:
    ```bash
    pip install requests
    ```
    Or, if you have multiple Python versions and need to be specific:
    ```bash
    python3 -m pip install requests
    ```
    For Python 3.11 specifically (if `pip` defaults to an older version):
    ```bash
    python3.11 -m pip install requests
    ```

3.  **Verify `requests` Installation**:
    You can verify by opening a Python interpreter and trying to import it:
    ```bash
    python3 # or python or python3.11
    ```
    Then, in the Python interpreter:
    ```python
    import requests
    print(requests.__version__)
    exit()
    ```
    This should print the installed version of the `requests` library without any errors.

**Best Practice: Virtual Environments** ✨

It's highly recommended to use virtual environments for your Python projects. This isolates project dependencies and avoids conflicts between projects.

1.  **Create a virtual environment** (e.g., in your project folder):
    ```bash
    python3 -m venv myenv # 'myenv' is the name of the virtual environment folder
    ```
2.  **Activate the virtual environment**:
    * **Windows (cmd.exe)**:
        ```cmd
        myenv\Scripts\activate
        ```
    * **Windows (PowerShell)**:
        ```powershell
        .\myenv\Scripts\Activate.ps1
        ```
        (You might need to set execution policy: `Set-ExecutionPolicy Unrestricted -Scope Process`)
    * **macOS/Linux (bash/zsh)**:
        ```bash
        source myenv/bin/activate
        ```
3.  **Install packages**: Once activated, `pip install requests` will install `requests` only in this environment.
4.  **Deactivate**: When you're done, simply type:
    ```bash
    deactivate
    ```

---

## Securing API Keys with `.env` Files 🛡️

Hardcoding API keys or other sensitive credentials directly into your scripts is a security risk, especially if the code is shared or committed to version control (like Git). A common practice is to use `.env` files to store these credentials as environment variables.

**What is a `.env` file?**
A `.env` (dot env) file is a simple text file that stores key-value pairs defining environment variables for your project. It's typically placed in the root directory of your project and **should be added to your `.gitignore` file** to prevent it from being committed to your repository.

**How to use it:**

1.  **Create a `.env` file**: In your project's root directory, create a file named `.env`.
2.  **Add your credentials**:
    ```env
    # .env file
    OPENFDA_API_KEY="YOUR_ACTUAL_API_KEY_HERE"
    # Add other environment variables as needed
    # ANOTHER_API_KEY="sk_anotherkey123"
    ```
    Replace `"YOUR_ACTUAL_API_KEY_HERE"` with the real API key you obtain.
3.  **Add `.env` to `.gitignore`**: Create or open your `.gitignore` file (also in the root of your project) and add the following line:
    ```gitignore
    .env
    ```
    This tells Git to ignore the `.env` file.
4.  **Load in Python**: Use the `python-dotenv` library to load these variables into your Python script's environment. This is shown in the OpenFDA example code below.

---

## Understanding API Authentication 🔑

When you interact with APIs, especially those providing access to sensitive data or those that want to track usage, you'll often need to authenticate your requests.

### 1. API Keys

* **What they are**: A unique string (like a password) provided by an API service to identify and authorize an application or user.
* **How they work**: Included in API requests (as a query parameter or HTTP header), allowing the server to verify the caller's identity and permissions, and to track usage.
* **Security**: Treat API keys confidentially. Do not embed them directly in public code. Use environment variables (like the `.env` method described above) or secure vaults.

### 2. OAuth 2.0 (Open Authorization)

* **What it is**: An authorization framework enabling third-party applications to obtain limited access to an HTTP service on behalf of a user, without exposing the user's credentials.
* **Key Concepts**: Resource Owner (user), Client (your app), Authorization Server, Resource Server (API), Access Token (temporary credential), Scopes (permissions).
* **When it's used**: For services where users grant access to their data (e.g., "Sign in with Google," allowing an app to access your cloud photos). It's more complex than API keys but provides granular control.

### Getting an OpenFDA API Key 🇺🇸

While OpenFDA allows some access without an API key, getting one is free and provides a higher rate limit.

1.  **Visit**: [https://open.fda.gov/api/reference/#api-key](https://open.fda.gov/api/reference/#api-key)
2.  **Provide Your Email Address** and agree to terms.
3.  **Receive Your API Key** via email.
4.  **Store it Securely**: Place this key in your `.env` file as `OPENFDA_API_KEY="YOUR_KEY"`.

---

## Getting OpenFDA API Data 💊

The OpenFDA API provides public access to a wealth of data related to drugs, devices, and food. While not compulsory for all API interactions (many third-party APIs require keys from the outset), it's highly recommended to learn about APIs with OpenFDA. Registering for an API key can also grant you a higher request limit.

* **OpenFDA website**: [https://open.fda.gov/apis/try-the-api/](https://open.fda.gov/apis/try-the-api/)

### Code (To get OpenFDA data)

Below is a Python script demonstrating how to fetch data from the OpenFDA API.

```python
# Import necessary libraries
import requests  # For making HTTP requests
import json      # For parsing JSON data

# --- Configuration ---
# Base URL for the API endpoint.
# Always refer to the API provider's documentation, as configurations might change.
base_url = "[https://api.fda.gov/drug/event.json](https://api.fda.gov/drug/event.json)"

# Define the search term.
# Here, it's hardcoded to reduce API load during testing.
# For multiple items, consider using a loop.
search_term = 'patient.reaction.reactionmeddrapt:"Fatigue"'

# Limit the number of search results returned.
# It's good practice to limit results initially, check the output, then adjust or remove the limit.
limit = 10

# Your API Key (Optional for OpenFDA for basic use, but recommended for higher limits).
# Refer to the SOP (Standard Operating Procedure) or OpenFDA documentation to get an API key.
# Although OpenFDA provides output without an API key, adding one is beneficial for testing your system
# and ensuring you don't hit lower unauthenticated rate limits quickly.
api_key = "YOUR_API_KEY_HERE"  # Replace with your actual API key if you have one

# Parameters for the API request
params = {
    "search": search_term,
    "limit": limit
}

# Add API key to parameters if it's provided
if api_key and api_key != "YOUR_API_KEY_HERE":  # Check if api_key is not empty or the placeholder
    params["api_key"] = api_key

# Headers for the API request
# Although not always necessary, setting a User-Agent is good practice.
# It helps the API provider identify the source of requests.
headers = {
    "User-Agent": "MyDataFetcher/1.0 (YourApp; yourcontact@example.com)" # Be descriptive
}

# --- Make the API Request ---
print(f"Sending request to: {base_url} with Parameters: {params}")
try:
    # Make the GET request with a timeout of 30 seconds
    response = requests.get(base_url, params=params, headers=headers, timeout=30)

    # --- Response Handling ---
    # Check if the request was successful (HTTP Status Code 200)
    if response.status_code == 200:
        print("Successfully fetched data from API 👍")
        
        # Parse the JSON response
        data = response.json()

        # Note that the actual data is usually nested, e.g., in 'results' for OpenFDA.
        # Use .get() with a default value (e.g., an empty list []) to avoid KeyErrors if 'results' is missing.
        results = data.get("results", [])
        
        if results:
            print(f"Number of records received: {len(results)}")
            # You can now process the 'results' list, e.g., print the first record:
            # print("First record:", json.dumps(results[0], indent=2))
        else:
            print("No results found for the query. 🤷")

        # To look for pagination info, look at the 'meta' part of the response.
        meta_data = data.get("meta")
        if meta_data:
            print(f"Meta information: {meta_data}")
            # Pagination details like total records, skip, and limit are often here.
            # This is useful if you need to fetch all data in chunks.

    elif response.status_code == 404:
        print(f"Error: API endpoint not found (404). Check URL: {response.url} 🕸️")
    
    # In case you are accessing OpenFDA without the API key, or your key has insufficient privileges,
    # adding a valid API key gives you a higher rate limit.
    elif response.status_code == 429:
        print(f"Error: Rate limit exceeded (429). 🐢 Try again later or check API key usage.")
        print(f"Response content: {response.text}") # See if there is more info (e.g., retry-after header)

    else:
        # Handle other HTTP error codes
        print(f"Error fetching data: Status Code {response.status_code} ❌")
        print(f"Response content: {response.text}") # Print the error message from the API

except requests.exceptions.Timeout:
    print(f"Request timed out after 30 seconds. ⏳ Server might be slow or network issue.")

except requests.exceptions.RequestException as e:
    # Handle other request-related errors (e.g., network issues, DNS failure)
    print(f"Request failed: {e} 💔")

except json.JSONDecodeError:
    # Handle errors if the response is not valid JSON
    print("Error: Failed to decode JSON response from API. 📉")
    # It's helpful to see what non-JSON response was received.
    # Check if 'response' variable exists before trying to access its 'text' attribute.
    print(f"Response content: {response.text if 'response' in locals() else 'N/A (response object not available)'}")
