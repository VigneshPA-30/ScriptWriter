from agents import function_tool
from googlesearch import search

@function_tool
def search_web(query: str, num_results: int = 5) -> list[dict]:
    """
    Performs a web search using Google Search and returns a list of URLS.
    Takes in search query as String for input
    """
    print(f"\nPerforming Google search for: '{query}'...")
    urls = []
    for url in search(query, num_results=num_results):
        urls.append(url)
    print(f"Found {len(urls)} result{'s' if len(urls)!=1 else ''}.")
    return urls


