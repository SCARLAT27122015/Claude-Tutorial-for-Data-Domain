# CLAUDE.md

This file provides guidance to Claude when working with this data engineering Python project.

---

## Project Overview

A Python-based data engineering project responsible for ingesting, transforming, and delivering data across pipelines. The codebase prioritizes correctness, observability, and maintainability over cleverness.

---

## Coding Conventions & Style

### General Python

- Target **Python 3.11+**. Use modern syntax: `match`, `tomllib`, `Self`, `TypeAlias`, etc.
- Prefer **explicit over implicit** — no magic, no clever one-liners that sacrifice readability.
- Maximum line length: **100 characters**.
- Use **double quotes** for strings consistently.
- Always include a **trailing comma** in multi-line collections and function signatures.

### Type Annotations

- All functions and methods **must** have full type annotations (arguments + return type).
- Use `from __future__ import annotations` at the top of every module.
- Prefer `X | Y` union syntax over `Union[X, Y]`.
- Use `TypedDict` for structured dicts; avoid raw `dict[str, Any]` unless unavoidable.
- Never use `Any` without a `# noqa: ANN401` comment explaining why.

```python
# Good
def extract(source: str, limit: int = 1000) -> list[dict[str, str]]:
    ...

# Bad
def extract(source, limit=1000):
    ...
```

### Naming Conventions

| Construct | Convention | Example |
|---|---|---|
| Modules | `snake_case` | `bronze_loader.py` |
| Classes | `PascalCase` | `SalesTransformer` |
| Functions / methods | `snake_case` | `load_to_warehouse()` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT = 3` |
| Private helpers | leading `_` | `_normalize_schema()` |
| Pipeline stages | prefixed noun | `extract_`, `transform_`, `load_` |

### Data Pipeline Structure

Pipelines follow the **ETL layering pattern**:

```
src/
├── extract/       # Source connectors and raw ingestion
├── transform/     # Business logic, cleaning, enrichment
├── load/          # Sink writers (warehouse, lake, API)
├── models/        # Pydantic or dataclass schemas
├── utils/         # Shared helpers (logging, retry, config)
└── config/        # Environment and pipeline config
```

- Each stage is a **pure function or class** — no cross-stage imports except through `models/`.
- Pipeline orchestration lives outside the stage modules (e.g., in `pipelines/` or DAG files).

### Data Models

- Use **Pydantic v2** for all data contracts at pipeline boundaries.
- Define models in `src/models/` — one file per domain entity.
- Never pass raw dicts across pipeline stage boundaries; use typed models.
- Validate at ingestion time, not at transformation time.

```python
from pydantic import BaseModel, Field

class OrderRecord(BaseModel):
    order_id: str = Field(..., description="Unique order identifier")
    amount: float = Field(..., ge=0)
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
```

### Error Handling

- Never use bare `except:` — always catch specific exceptions.
- Use **custom exception classes** for domain errors (e.g., `ExtractionError`, `SchemaValidationError`).
- Log errors with context before re-raising; don't swallow exceptions silently.
- Transient failures (network, rate limits) must use retry logic with exponential backoff.

```python
# Good
try:
    records = fetch_from_api(endpoint)
except httpx.TimeoutException as exc:
    logger.error("API timeout", endpoint=endpoint, exc_info=exc)
    raise ExtractionError(f"Timeout fetching {endpoint}") from exc
```

### Logging

- Use **`structlog`** for structured, JSON-compatible logging throughout.
- Never use `print()` in pipeline code — always `logger.info/warning/error`.
- Bind contextual metadata early (pipeline name, run ID, source) using `structlog.contextvars`.
- Log at stage entry/exit with record counts.

```python
import structlog
logger = structlog.get_logger()

logger.info("extraction_complete", source=source, records=len(records))
```

### SQL Style (inline or `.sql` files)

- Keywords in **UPPERCASE**: `SELECT`, `FROM`, `WHERE`, `GROUP BY`.
- One clause per line; indent subqueries with 4 spaces.
- Use **CTEs** instead of nested subqueries — name them descriptively.
- Always alias columns explicitly; never `SELECT *` in production queries.

```sql
WITH daily_sales AS (
    SELECT
        order_date,
        SUM(amount) AS total_amount
    FROM orders
    WHERE status = 'completed'
    GROUP BY order_date
)
SELECT *
FROM daily_sales
WHERE total_amount > 1000
```

### Testing

- Use **`pytest`** with fixtures scoped appropriately (`function` for unit, `session` for integration).
- Unit test each stage (extract, transform, load) in isolation using mocks/stubs.
- Transformation functions should be **pure and deterministic** — straightforward to test.
- Test file naming: `test_<module_name>.py`, e.g., `test_sales_transformer.py`.
- Aim for **≥ 80% coverage** on `transform/` — this is where bugs live.

### Linting & Formatting

- **Formatter:** `ruff format` (replaces Black)
- **Linter:** `ruff check` with rules: `E, F, I, N, ANN, UP, B, SIM`
- **Type checker:** `mypy --strict`
- All three must pass with **zero warnings** before committing.

---

## What Claude Should Avoid

- Don't introduce new dependencies without checking `pyproject.toml` first.
- Don't use `pandas` for large-scale transformations — prefer `polars` or PySpark.
- Don't write pipeline logic inside notebook cells — notebooks are for exploration only.
- Don't use mutable default arguments (e.g., `def f(items=[]):`).
- Don't skip type annotations to save time — always annotate.