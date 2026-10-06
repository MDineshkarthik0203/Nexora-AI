from dotenv import load_dotenv
from langchain_tavily import TavilySearch

load_dotenv()


tavily_search = TavilySearch(
    max_results=5
)


def web_search(query: str):

    results = tavily_search.invoke({
        "query": query
    })

    return results


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