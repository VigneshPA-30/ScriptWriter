from agents import function_tool, Agent ,Runner
from googlesearch import search
from backend.prompts import search_prompt
import requests
from bs4 import BeautifulSoup
import asyncio
from backend.models import gemini_model



@function_tool
def search_web(query: str, num_results: int = 10) -> list[dict]:
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




def get_page_content(url: str) -> str:
    """
    Fetch the given URL and return its visible text content only.
    """
    visible_text = ""

    try:
    # 1. Download the page
        response = requests.get(url, timeout=10)  # timeout to avoid hanging
        #response.raise_for_status()  # raises an error if the HTTP request failed [an unexpected problem]

        # 2. Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Remove scripts and styles so they don’t pollute the text
        for tag in soup(['script', 'style']):
            tag.decompose()  # completely remove the tag and its contents

        # 4. Extract text and collapse extra whitespace
        text = soup.get_text(separator='\n')  
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        visible_text = '\n'.join(chunk for chunk in chunks if chunk)

    except Exception as e:
        visible_text = f"Error Occurred {e}"
    
    #print(f"Web Page Text :\n{visible_text}")

    return visible_text



async def search_agent_function(page_content:str) -> str:

    search_agent = Agent(
            name="search_agent_tool",
            model=gemini_model,
            instructions=search_prompt,
        )

    result = await Runner.run(
            starting_agent=search_agent,
            input=f"page_content:\n {page_content}"
        )

    return result.final_output


@function_tool
async def get_search_agent_tool(url:str)->list:
    """
    Creates and returns the search_agent_tool.
    This tool is an agent that can visit a URL and return a summary.
    It requires an active Playwright MCP server.
    """
    try:
        page_content = get_page_content(url)
    except Exception as e:
        print(f"Error Occurred for [{url}]")
        return [url, f"Error Occurred : {e}"]

    print(f"Fetched Page Content of [{url}]")

    await asyncio.sleep(1)

    page_summary = await search_agent_function(page_content)

    print(f"AI returned Summary for {url}")

    return [url,page_summary]


