---
name: visualize
description: Visualizes data using various libraries and tools.
---

## Usage

### Step 1: Pick the python environment
Before you start, make sure to pick the python environment in which you want to run the code  You can run/install dependencies using the .venv environment which is located here: "D:\Documentos\estudioProgramacion\claude_tutorial\.venv".

### Step 2: Use the Python scripts in the scripts folder to explore the data and build KPIs
- You use the scripts located here to explore the data and build kpis:

D:\Documentos\estudioProgramacion\claude_tutorial\.claude\skills\visualizers\scripts

- The scripts are:
    - explore_data.py: This script is used to explore the data and understand the structure of the data. It will print the first 5 rows of each csv file and the summary statistics of each csv file.
    - build_kpis.py: This script is used to build KPIs from the data. It will create a new directory with name "kpis" in the visualizers skill directory and store the KPIs in that directory as CSV files. The file names should be the name of the KPI (e.g., "total_sales.csv", "average_sales.csv", etc.).