import os
import textwrap
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from kagiapi import KagiClient  # type: ignore
from kagiapi.models import FastGPTResponse  # type: ignore
from mcp.server.fastmcp import FastMCP
from pydantic import Field

# Feature flags from environment variables with defaults
ENABLE_SEARCH = os.environ.get("KAGI_ENABLE_SEARCH", "true").lower() == "true"
ENABLE_FASTGPT = os.environ.get("KAGI_ENABLE_FASTGPT", "true").lower() == "true"

# Initialize Kagi client
kagi_client = KagiClient()
mcp = FastMCP("kagimcp", dependencies=["kagiapi", "mcp[cli]"])


if ENABLE_SEARCH:
    @mcp.tool()
    def search(
        queries: list[str] = Field(
            description="One or more concise, keyword-focused search queries. "
            "Include essential context within each query for standalone use."
        ),
    ) -> str:
        """Perform web search based on one or more queries.
        
        Results are from all queries given. They are numbered continuously,
        so that a user may be able to refer to a result by a specific number.
        """
        # Check for empty queries before entering try block
        if not queries:
            raise ValueError("Search called with no queries.")
            
        try:
            with ThreadPoolExecutor() as executor:
                results = list(executor.map(kagi_client.search, queries, timeout=10))

            return format_search_results(queries, results)

        except Exception as e:
            return f"Error: {str(e) or repr(e)}"


if ENABLE_FASTGPT:
    @mcp.tool()
    def fast_gpt(
        query: str = Field(
            description="A query to summarize search results for. "
            "Should be a specific, information-seeking question."
        ),
        cache: bool = Field(
            default=True,
            description="Whether to allow cached requests & responses.",
        ),
    ) -> str:
        """Use FastGPT to summarize web search results for a query.
        
        Returns an AI-generated answer with references to sources.
        """
        try:
            # Add detailed error logging
            import logging
            logging.info(f"Calling FastGPT with query: {query}")
            response: FastGPTResponse = kagi_client.fastgpt(query=query)
            logging.info("FastGPT response received successfully")
            return format_fastgpt_response(response)
        except Exception as e:
            import traceback
            error_details = f"Error: {str(e) or repr(e)}\n{traceback.format_exc()}"
            logging.error(error_details)
            return error_details


def format_fastgpt_response(response: FastGPTResponse) -> str:
    """Format the FastGPT response for display."""
    result = str(response["data"]["output"])

    if response["data"]["references"]:
        result += "\n\n## References\n"
        for i, ref in enumerate(response["data"]["references"], 1):
            result += f"{i}. [{ref['title']}]({ref['url']})\n"
    
    return result


def format_search_results(
    queries: list[str], responses: Sequence[dict[str, Any]]
) -> str:
    """Format search results for response. Consider both LLM and human parsing."""

    result_template = textwrap.dedent("""
        {result_number}: {title}
        {url}
        Published Date: {published}
        {snippet}
    """).strip()

    query_response_template = textwrap.dedent("""
        -----
        Results for search query \"{query}\":
        -----
        {formatted_search_results}
    """).strip()

    per_query_response_strs = []

    start_index = 1
    for query, response in zip(queries, responses, strict=True):
        # t == 0 is search result, t == 1 is related searches
        results = [result for result in response["data"] if result["t"] == 0]

        # published date is not always present
        formatted_results_list = [
            result_template.format(
                result_number=result_number,
                title=result["title"],
                url=result["url"],
                published=result.get("published", "Not Available"),
                snippet=result["snippet"],
            )
            for result_number, result in enumerate(results, start=start_index)
        ]

        start_index += len(results)

        formatted_results_str = "\n\n".join(formatted_results_list)
        query_response_str = query_response_template.format(
            query=query, formatted_search_results=formatted_results_str
        )
        per_query_response_strs.append(query_response_str)

    return "\n\n".join(per_query_response_strs)


def main() -> None:
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
