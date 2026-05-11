---
name: fetch_api
description: "Fetch data from an API endpoint handles responses. Use when interacting with external APIs or services that provide data from web responses."
---

## Usage

### Step 0: Pick the python environment: 
Before running the code, make sure to pick the python environment in which you have installed the required libraries (httpx, pandas, etc.). You can install them in the .venv environment which is located here: "D:\Documentos\estudioProgramacion\claude_tutorial\.venv".

### Step 1: Fetch Data from API
You need to make python API calls to fetch data from the following URLs using async httpx:
[
  "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_customer.csv",

  "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_store.csv",

  "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_date.csv",

  "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_product.csv",

  "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_sales.csv",

  "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_returns.csv",
]

### Step 2: Handle API Responses
After fetching the data, you need to create a directory having name with current date and time in the format "YYYY-MM-DD_HH-MM-SS" and store the responses in that directory as CSV files. The file names should be the last part of the URL (e.g., "dim_customer.csv", "dim_store.csv", etc.). The path should be .claude/skills/fetch_api/data/YYYY-MM-DD_HH-MM-SS/dim_customer.csv, .claude/skills/fetch_api/data/YYYY-MM-DD_HH-MM-SS/dim_store.csv, etc.

### Step 3: logging
You need to create a log directory at .claude/skills/fetch_api/logs/ with name current date and time in the format "YYYY-MM-DD_HH-MM-SS" and store the logs in that directory. The log file should be named "fetch_api.log". You need to log the following information  :
- When the API call is initiated for each URL.
- When the API call is successful for each URL.
- When the API call fails for each URL, along with the error message.
- When the data is successfully stored in the directory for each URL.
- When the data storage fails for each URL, along with the error message.
- When the entire process is completed successfully.
- When the entire process fails, along with the error message.
- What API was called.
