from __future__ import annotations

from pathlib import Path

import pandas as pd

data_dir = Path("D:\\Documentos\\estudioProgramacion\\claude_tutorial\\.claude\\skills\\migrate\\data")
latest_data_dir = sorted(data_dir.glob("*"))[-1]

fact_sales = pd.read_parquet(latest_data_dir / "fact_sales.parquet")
fact_returns = pd.read_parquet(latest_data_dir / "fact_returns.parquet")

print("fact_sales columns:")
print(fact_sales.columns.tolist())
print("\nfact_sales dtypes:")
print(fact_sales.dtypes)
print("\nfact_sales head:")
print(fact_sales.head(3))

print("\n\nfact_returns columns:")
print(fact_returns.columns.tolist())
print("\nfact_returns dtypes:")
print(fact_returns.dtypes)
print("\nfact_returns head:")
print(fact_returns.head(3))
