from __future__ import annotations

from mcp.client.stdio import stdio_client
import inspect

print("stdio_client signature:")
print(inspect.signature(stdio_client))
print("\n" + "=" * 50 + "\n")
print("Documentation:")
print(inspect.getdoc(stdio_client))
