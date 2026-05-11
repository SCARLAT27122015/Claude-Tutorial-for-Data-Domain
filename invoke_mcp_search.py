from __future__ import annotations

import asyncio
import json
import sys

import structlog
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

logger = structlog.get_logger()


async def invoke_mcp_server() -> None:
    """Invoke the duckduckgo-mcp-server and search for 2026 news."""
    try:
        logger.info("starting_mcp_server", server="duckduckgo-mcp-server")

        # Create server parameters for the duckduckgo-mcp-server
        server_params = StdioServerParameters(
            command="uvx",
            args=["duckduckgo-mcp-server"],
        )

        # Create and manage the MCP session
        async with stdio_client(server_params) as (read_stream, write_stream):
            logger.info("mcp_streams_established")

            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:
                logger.info("mcp_session_established")

                # Perform initialization
                await session.initialize()
                logger.info("mcp_initialization_complete")

                # List available tools
                tools_response = await session.list_tools()
                tool_names = [t.name for t in tools_response.tools]
                logger.info(
                    "available_tools",
                    tool_count=len(tool_names),
                    tools=tool_names,
                )

                # Verify search tool exists
                if "search" not in tool_names:
                    logger.error("search_tool_not_found", available=tool_names)
                    print(
                        "Error: 'search' tool not found. "
                        f"Available tools: {tool_names}"
                    )
                    sys.exit(1)

                # Search for 2026 news
                search_query = "2026 news latest events"
                logger.info("searching", query=search_query)

                # Call the search tool
                result = await session.call_tool(
                    "search",
                    {"query": search_query},
                )

                logger.info("search_complete")
                print("\n" + "=" * 80)
                print(f"Search Results for: {search_query}")
                print("=" * 80 + "\n")

                if result.content:
                    for content in result.content:
                        if hasattr(content, "text"):
                            print(content.text)
                        else:
                            print(json.dumps(content, indent=2))
                else:
                    print("No results found.")

    except Exception as exc:
        logger.error(
            "mcp_error",
            error=str(exc),
            exc_info=True,
        )
        print(f"Error invoking MCP server: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(invoke_mcp_server())
