# Airflow Project: Weather Data Pipeline

A data pipeline project demonstrating Apache Airflow's asset-based triggering and DAG orchestration for weather data processing.

## Project Overview

This project contains a producer-consumer pattern implemented with Airflow DAGs:
- **Producer DAG (`data_fetch`)**: Fetches weather data from an API, transforms it, and materializes it as a file asset
- **Consumer DAG (`data_report`)**: Automatically triggered when the weather asset is updated, reads and analyzes the data

## Architecture

### DAGs

#### 1. **data_fetch** DAG
Orchestrates the complete data pipeline lifecycle:

```
prepare_storage() → fetch_api_data() → transform_data() → materialize_asset()
```

**Tasks:**
- `prepare_storage`: Creates necessary directories in `/opt/airflow/data`
- `fetch_api_data`: Simulates an API call (currently returns mock weather data)
- `transform_data`: Adds processing metadata (timestamp, status)
- `materialize_asset`: Writes processed data to JSON file and marks asset as complete

**Output Asset:** `file:///opt/airflow/data/weather_report.json`

#### 2. **data_report** DAG
Triggered automatically when the weather asset is updated.

**Tasks:**
- `read_asset`: Reads the weather JSON file and logs city/temperature analysis

**Trigger:** Asset-based (depends on `weather_data_asset` from `data_fetch`)

## Key Features

### Asset-Based Triggering
The project demonstrates Airflow's **asset** feature for data-aware scheduling:
- `data_fetch` produces a weather data asset
- `data_report` consumes this asset and automatically triggers when it's updated
- This decouples DAGs and creates event-driven workflows

### Data Flow

```
API (simulated)
    ↓
[data_fetch]
    ├─ Fetch raw data
    ├─ Transform & enrich (add metadata)
    └─ Materialize to file
        ↓
    weather_data_asset
        ↓
    [data_report] (auto-triggered)
        └─ Read & analyze data
```

## Project Structure

```
Airflow_Project/
├── dags/
│   ├── data_fetch.py    # Producer DAG
│   └── data_report.py   # Consumer DAG
└── README.md            # This file
```

## Data Format

The weather data asset is stored as JSON:

```json
{
  "city": "New York",
  "temp": 22,
  "unit": "C",
  "processed_at": "2024-01-15T10:30:45.123456",
  "status": "cleansed"
}
```

## Getting Started

### Prerequisites
- Apache Airflow 2.7+ (with SDK support)
- Python 3.8+
- Proper Airflow environment configuration

### Running the Pipeline

1. **Ensure DAGs are discoverable:**
   - Place both Python files in your Airflow `dags/` folder
   - Verify Airflow can parse them: `airflow dags list`

2. **Trigger the producer DAG:**
   ```bash
   airflow dags trigger data_fetch
   ```
   This will execute the entire data pipeline and create the weather asset.

3. **Monitor the consumer DAG:**
   - The `data_report` DAG will automatically trigger when `data_fetch` completes
   - Check logs to see the weather analysis output

### Manual Testing

To manually test reading the asset:
```bash
python -c "import json; data = json.load(open('/opt/airflow/data/weather_report.json')); print(f\"Weather: {data['city']} - {data['temp']}°{data['unit']}\")"
```

## Future Enhancements

- **Real API Integration**: Replace simulated API call with actual weather service (OpenWeatherMap, etc.)
- **Data Validation**: Add schema validation using Great Expectations
- **Error Handling**: Implement retry logic and alerting for failed tasks
- **Multi-location Support**: Extend to fetch weather for multiple cities
- **Data Storage**: Integrate with databases (PostgreSQL, Snowflake) instead of JSON files
- **Monitoring**: Add data quality checks and SLAs

## Notes

- Currently uses mock API data for demonstration purposes
- Asset URIs point to `/opt/airflow/data/` (Docker container path)
- The project follows Airflow SDK decorators pattern for modern, clean DAG definitions
