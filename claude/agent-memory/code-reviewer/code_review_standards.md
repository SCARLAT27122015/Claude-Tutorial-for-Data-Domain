---
name: Code Review Standards for Data Engineering Project
description: Coding standards and conventions for Python data engineering project (CLAUDE.md)
type: project
---

Project uses strict Python data engineering standards (CLAUDE.md):

**Type Annotations:**
- All functions/methods must have full type annotations (args + return type)
- Use `from __future__ import annotations` in every module
- Prefer `X | Y` union syntax over `Union[X, Y]`
- Never use `Any` without `# noqa: ANN401` comment

**Logging:**
- **MUST use `structlog`** for structured, JSON-compatible logging
- **NEVER use `print()`** in pipeline code — always logger.info/warning/error
- Bind contextual metadata early using structlog.contextvars
- Log at stage entry/exit with record counts

**Code Style:**
- Max line length: 100 characters
- Always double quotes for strings
- Trailing commas in multi-line collections/signatures
- Explicit over implicit — no magic or clever one-liners

**Error Handling:**
- Never bare `except:` — always catch specific exceptions
- Use custom exception classes for domain errors
- Log errors with context before re-raising
- Transient failures need retry logic with exponential backoff

**Naming:**
- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private helpers: leading `_`

**Linting:**
- Formatter: `ruff format`
- Linter: `ruff check` (E, F, I, N, ANN, UP, B, SIM rules)
- Type checker: `mypy --strict`
- All must pass with zero warnings before commit
