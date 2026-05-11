from __future__ import annotations

import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

import httpx


async def main() -> None:
    urls: list[str] = [
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_customer.csv",
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_store.csv",
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_date.csv",
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_product.csv",
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_sales.csv",
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_returns.csv",
    ]

    timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    data_dir: Path = (
        Path(".claude/skills/fetch_api/data") / timestamp
    )
    logs_dir: Path = (
        Path(".claude/skills/fetch_api/logs") / timestamp
    )

    data_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file: Path = logs_dir / "fetch_api.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout),
        ],
    )
    logger: logging.Logger = logging.getLogger(__name__)

    logger.info("Starting fetch_api process")
    logger.info(f"Timestamp: {timestamp}")
    logger.info(f"Data directory: {data_dir}")
    logger.info(f"Logs directory: {logs_dir}")

    async with httpx.AsyncClient() as client:
        tasks: list = []
        for url in urls:
            tasks.append(fetch_and_save(client, url, data_dir, logger))

        results: list = await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )

    failed_count: int = sum(
        1 for result in results if isinstance(result, Exception)
    )
    success_count: int = len(results) - failed_count

    if failed_count == 0:
        logger.info(
            f"Process completed successfully. "
            f"{success_count} files fetched and saved."
        )
    else:
        logger.error(
            f"Process completed with errors. "
            f"Success: {success_count}, Failed: {failed_count}"
        )


async def fetch_and_save(
    client: httpx.AsyncClient,
    url: str,
    data_dir: Path,
    logger: logging.Logger,
) -> None:
    filename: str = url.split("/")[-1]
    logger.info(f"API call initiated: {url}")

    try:
        response: httpx.Response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        logger.info(f"API call successful: {url}")

        file_path: Path = data_dir / filename
        file_path.write_bytes(response.content)
        logger.info(
            f"Data successfully stored: {file_path}"
        )

    except httpx.HTTPError as exc:
        logger.error(
            f"API call failed: {url}. Error: {str(exc)}"
        )
        raise
    except OSError as exc:
        logger.error(
            f"Data storage failed for {filename}. "
            f"Error: {str(exc)}"
        )
        raise


if __name__ == "__main__":
    asyncio.run(main())
