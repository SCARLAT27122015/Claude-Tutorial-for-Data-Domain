from __future__ import annotations

import asyncio
import io
from datetime import datetime
from pathlib import Path

import httpx
import pandas as pd

API_URLS: list[str] = [
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_customer.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_store.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_date.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_product.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_sales.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_returns.csv",
]

BASE_DATA_DIR = Path(".claude/skills/fetch_api/data")
BASE_LOGS_DIR = Path(".claude/skills/fetch_api/logs")


class _FileLogger:
    def __init__(self, filepath: Path,) -> None:
        self.filepath = filepath

    def msg(self, message: str,) -> None:
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(message + "\n")


def _setup_logger(log_dir: Path) -> _FileLogger:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "fetch_api.log"
    return _FileLogger(log_file)


async def _fetch_and_save_csv(
    url: str,
    data_dir: Path,
    logger: _FileLogger,
) -> bool:
    filename = url.split("/")[-1]

    try:
        logger.msg(f"API call initiated: {url}")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()

        logger.msg(f"API call successful: {url}")

        df = pd.read_csv(io.StringIO(response.text))
        output_path = data_dir / filename
        df.to_csv(output_path, index=False)

        logger.msg(f"Data storage successful: {url} -> {output_path}")
        return True

    except httpx.HTTPError as exc:
        logger.msg(f"API call failed: {url} - Error: {exc}")
        return False

    except (pd.errors.ParserError, OSError) as exc:
        logger.msg(f"Data storage failed: {url} - Error: {exc}")
        return False


async def fetch_all_data() -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    data_dir = BASE_DATA_DIR / timestamp
    log_dir = BASE_LOGS_DIR / timestamp

    logger = _setup_logger(log_dir)

    logger.msg(f"Fetch process started at {timestamp}")

    data_dir.mkdir(parents=True, exist_ok=True)

    tasks = [
        _fetch_and_save_csv(url, data_dir, logger) for url in API_URLS
    ]
    results = await asyncio.gather(*tasks)

    successful = sum(results)
    total = len(results)

    if all(results):
        logger.msg(
            f"Fetch process completed successfully: "
            f"{successful}/{total} URLs fetched"
        )
    else:
        logger.msg(
            f"Fetch process completed with errors: "
            f"{successful}/{total} succeeded, {total - successful} failed"
        )


if __name__ == "__main__":
    asyncio.run(fetch_all_data())
