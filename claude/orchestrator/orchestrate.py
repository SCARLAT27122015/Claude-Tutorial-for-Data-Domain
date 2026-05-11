from __future__ import annotations

import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logging(log_dir: Path) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file: Path = log_dir / "orchestrator.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger(__name__)


def run_fetch_api(logger: logging.Logger) -> bool:
    import subprocess

    logger.info("=" * 60)
    logger.info("STEP 1: Running fetch_api skill...")
    logger.info("=" * 60)

    try:
        result: subprocess.CompletedProcess = subprocess.run(
            [
                sys.executable,
                ".claude/skills/fetch_api/fetch_data.py",
            ],
            cwd=Path.cwd(),
            capture_output=False,
            check=True,
        )
        logger.info("fetch_api completed successfully")
        return True
    except subprocess.CalledProcessError as exc:
        logger.error(f"fetch_api failed with exit code {exc.returncode}")
        return False


def run_migrate(logger: logging.Logger) -> bool:
    import subprocess

    logger.info("=" * 60)
    logger.info("STEP 2: Running migrate skill...")
    logger.info("=" * 60)

    try:
        result: subprocess.CompletedProcess = subprocess.run(
            [
                sys.executable,
                ".claude/skills/migrate/scripts/csv_to_parquet.py",
            ],
            cwd=Path.cwd(),
            capture_output=False,
            check=True,
        )
        logger.info("migrate completed successfully")
        return True
    except subprocess.CalledProcessError as exc:
        logger.error(f"migrate failed with exit code {exc.returncode}")
        return False


def main() -> None:
    timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir: Path = Path(".claude/orchestrator/logs") / timestamp

    logger: logging.Logger = setup_logging(log_dir)

    logger.info("Starting orchestration pipeline")
    logger.info(f"Timestamp: {timestamp}")
    logger.info(f"Log directory: {log_dir}")

    fetch_success: bool = run_fetch_api(logger)
    if not fetch_success:
        logger.error("Orchestration pipeline failed at fetch_api step")
        return

    migrate_success: bool = run_migrate(logger)
    if not migrate_success:
        logger.error("Orchestration pipeline failed at migrate step")
        return

    logger.info("=" * 60)
    logger.info("Orchestration pipeline completed successfully!")
    logger.info("=" * 60)
    logger.info("Data flow:")
    logger.info(
        "  1. Fetched data: .claude/skills/fetch_api/data/{timestamp}/"
    )
    logger.info(
        "  2. Migrated data: .claude/skills/migrate/data/{timestamp}/"
    )


if __name__ == "__main__":
    main()
