from __future__ import annotations

import httpx
import json
from duckduckgo_search import DDGS


def search_news_2026() -> None:
    """Search for 2026 news using DuckDuckGo."""
    queries = [
        "breaking news May 2026",
        "latest news today",
        "world news 2026",
    ]

    for query in queries:
        try:
            print(f"\n{'=' * 80}")
            print(f"Searching for: {query}")
            print("=" * 80 + "\n")

            results = DDGS().text(query, max_results=5)

            if not results:
                print("No results found for this query.\n")
                continue

            for i, result in enumerate(results, 1):
                print(f"{i}. {result.get('title', 'No title')}")
                print(f"   URL: {result.get('href', 'No URL')}")
                print(
                    f"   {result.get('body', 'No description')[:200]}...\n"
                )

            print(f"Found {len(results)} results\n")

        except Exception as e:
            print(f"Error searching for '{query}': {e}\n")


if __name__ == "__main__":
    search_news_2026()
