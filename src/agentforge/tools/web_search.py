import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_tavily import TavilySearch

PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv()

_tavily_client = None


def get_tavily_search():
    global _tavily_client
    if _tavily_client is None:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return None
        _tavily_client = TavilySearch(
            max_results=5,
            tavily_api_key=api_key,
        )
    return _tavily_client


# Module-level alias for backward compatibility
class _LazyTavilyProxy:
    def invoke(self, *args, **kwargs):
        client = get_tavily_search()
        if not client:
            raise ValueError("TAVILY_API_KEY is not set. Please add TAVILY_API_KEY to your .env file.")
        return client.invoke(*args, **kwargs)


tavily_search = _LazyTavilyProxy()


def web_search(query: str):
    search_client = get_tavily_search()
    if not search_client:
        return {
            "results": [],
            "error": "Tavily API key is not configured. Please set TAVILY_API_KEY in .env.",
        }

    try:
        results = search_client.invoke({
            "query": query
        })
        return results
    except Exception as exc:
        return {
            "results": [],
            "error": f"Tavily search failed: {exc}",
        }


def format_search_results(results):

    formatted = []

    for result in results.get("results", []):

        title = result.get("title", "")
        url = result.get("url", "")
        content = result.get("content", "")

        formatted.append(
            f"""
TITLE:
{title}

URL:
{url}

CONTENT:
{content}
"""
        )

    return "\n\n".join(formatted)