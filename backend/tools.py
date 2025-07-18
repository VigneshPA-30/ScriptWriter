from agents import function_tool
from duckduckgo_search import DDGS

@function_tool
def search_web(query: str, num_results: int = 5) -> list[dict]:
    """
    Performs a web search using DuckDuckGo and returns a list of results.
    Each result is a dictionary containing 'title', 'href', and 'body' (snippet).
    """
    print(f"\nPerforming web search for: '{query}'...")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=num_results))

        if not results:
            print("No search results found.")
            return []
        print(results)
        print("-----------------------------------------")
        print(f"Found {len(results)} search results.")
        # for i, result in enumerate(results):
        #     print(f"  {i+1}. {result.get('title', 'N/A')}")
        return results
    except Exception as e:
        print(f"Error during web search: {e}")
        return []