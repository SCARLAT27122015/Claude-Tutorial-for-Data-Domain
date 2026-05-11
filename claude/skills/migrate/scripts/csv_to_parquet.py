from __future__ import annotations

from pathlib import Path

import pandas as pd

SOURCE_BASE = Path(".claude/skills/fetch_api/data")
TARGET_BASE = Path(".claude/skills/migrate/data")


class _FileLogger:
    def __init__(self, filepath: Path,) -> None:
        self.filepath = filepath

    def msg(self, message: str,) -> None:
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(message + "\n")
        print(message)


def _get_latest_dated_folder(base_dir: Path) -> Path | None:
    if not base_dir.exists():
        return None

    folders = sorted(
        [f for f in base_dir.iterdir() if f.is_dir()],
        reverse=True,
    )
    return folders[0] if folders else None


def _convert_csv_to_parquet() -> None:
    latest_folder = _get_latest_dated_folder(SOURCE_BASE)

    if not latest_folder:
        print("No data folders found in fetch_api/data")
        return

    folder_name = latest_folder.name
    target_folder = TARGET_BASE / folder_name
    target_folder.mkdir(parents=True, exist_ok=True)

    log_file = target_folder / "migration.log"
    logger = _FileLogger(log_file)

    logger.msg(f"Starting CSV to Parquet conversion from {latest_folder}")
    logger.msg(f"Target folder: {target_folder}")

    csv_files = sorted(latest_folder.glob("*.csv"))

    if not csv_files:
        logger.msg("No CSV files found in the latest folder")
        return

    successful = 0
    failed = 0

    for csv_file in csv_files:
        try:
            logger.msg(f"Converting {csv_file.name}...")

            df = pd.read_csv(csv_file)
            parquet_file = target_folder / csv_file.stem
            parquet_file = parquet_file.with_suffix(".parquet")

            df.to_parquet(parquet_file, index=False, engine="pyarrow")

            logger.msg(
                f"[OK] Successfully converted: {csv_file.name} "
                f"({len(df)} rows, "
                f"{parquet_file.stat().st_size / 1024:.2f} KB)"
            )
            successful += 1

        except (pd.errors.ParserError, OSError) as exc:
            logger.msg(f"[FAIL] Failed to convert {csv_file.name}: {exc}")
            failed += 1

        except Exception as exc:
            logger.msg(
                f"[FAIL] Unexpected error converting {csv_file.name}: {exc}"
            )
            failed += 1

    total = successful + failed
    logger.msg(
        f"\nConversion complete: {successful}/{total} succeeded, "
        f"{failed} failed"
    )
    logger.msg(f"Output stored in: {target_folder}")


if __name__ == "__main__":
    _convert_csv_to_parquet()
