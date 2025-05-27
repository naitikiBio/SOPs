# Ingesting Data from APIs 📄

This guide provides an overview of how to ingest data from APIs, using the OpenFDA API as an example. It also includes instructions for setting up your Python environment.

---

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
