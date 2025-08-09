from agents import function_tool, Agent ,Runner
from googlesearch import search
from .prompts import search_prompt
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs
import asyncio
from .models import gemini_model
import requests
import time



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



# ...existing code...

async def run_with_retry(*args, max_retries=5, **kwargs):
    for attempt in range(max_retries):
        try:
            return await Runner.run(*args, **kwargs)
        except Exception as e:
            error_message = str(e)
            # Handle rate limit error
            if hasattr(e, "args") and any("retryDelay" in str(arg) for arg in e.args):
                delay = 2 ** attempt
                for arg in e.args:
                    if "retryDelay" in str(arg):
                        import re
                        match = re.search(r'"retryDelay":\s*"(\d+)s"', str(arg))
                        if match:
                            delay = int(match.group(1))
                print(f"Rate limited. Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            # Handle payload too large error
            elif "data payload too large" in error_message:
                print("Input too large, splitting and retrying...")
                # Try to split the input into 2 or 3 parts and run separately
                input_text = kwargs.get("input")
                if not input_text or len(input_text) < 10:
                    raise RuntimeError("Input too large and cannot be split further.")
                # Split into 3 parts
                parts = []
                n = len(input_text)
                step = n // 3
                for i in range(3):
                    start = i * step
                    end = (i + 1) * step if i < 2 else n
                    parts.append(input_text[start:end])
                results = []
                for idx, part in enumerate(parts):
                    print(f"Processing part {idx+1}/3...")
                    part_kwargs = dict(kwargs)
                    part_kwargs["input"] = part
                    result = await run_with_retry(*args, max_retries=max_retries, **part_kwargs)
                    results.append(result)
                # Combine results (if possible)
                # If result has 'final_output', concatenate those; otherwise, just return the list
                if all(hasattr(r, "final_output") for r in results):
                    combined = "".join(r.final_output for r in results)
                    class DummyResult:
                        final_output = combined
                    return DummyResult()
                return results
            else:
                raise
    raise RuntimeError("Max retries exceeded for Runner.run")
# ...existing code...

async def search_agent_function(page_content:str) -> str:


    search_agent = Agent(
                name="search_agent_tool",
                model=gemini_model,
                instructions=search_prompt,
            )

    result = await run_with_retry(
                    starting_agent=search_agent,
                    input=f"page_content:\n {page_content}"
                )

    return result.final_output


@function_tool
async def get_search_agent_tool(url:str)->list:
    """
    Gets the webpage URL as an input.
    Gives the summary of the URL with the URL as list as output.
    Uses BeatifulSoup for extraction.
    """
    print(f"Called get_search_agent_tool with {url}")
    try:
        page_content = get_page_content(url)
    except Exception as e:
        print(f"Error Occurred for [{url}]")
        return [url, f"Error Occurred : {e}"]

    print(f"Fetched Page Content of [{url}]")

    await asyncio.sleep(3)

    page_summary = await search_agent_function(page_content)

    print(f"AI returned Summary for {url}")

    return [url,page_summary]





def download_transcript(vid):
    """
    Downloads transcripts for each video and writes to a single CSV file.
    Skips videos without available transcripts.
    """
    final_script= ""
    vid_id =""
    parsed = urlparse(vid)
    #youtube = build('youtube', 'v3')
    if parsed.hostname in ('youtu.be','www.youtu.be'):
        vid_id = parsed.path.lstrip('/')
    else:
        if parsed.path.startswith("/shorts/"):
            path_parts = parsed.path.split('/')
            vid_id = path_parts[2] if len(path_parts) > 2 else None
            print(vid_id)
        else:
            print(parsed)
            url_dict = parse_qs(parsed.query)
            print(url_dict)
            vid_id = url_dict.get('v',[None])[0]
            print(vid_id)


    try:
        yt = YouTubeTranscriptApi()
        transcript_list = yt.fetch(video_id = vid_id)
        print(type(transcript_list))
        for transcript in transcript_list:
            final_script += transcript.text
        print(f"Downloaded transcript for {vid_id}")
    except (TranscriptsDisabled, NoTranscriptFound):
        print(f"No transcript for {vid_id}, skipping.")
    except Exception as e:
        raise f"Error occurred on youtube transcript downoad:\n{e}"

    return final_script

@function_tool
async def youtube_transcript_summary_tool(url:str)->list:
    """
    Gets the youtube URL as input.
    Gives the summary of the URL with the URL as list as output.
    Uses YOutubeTranscriptAPI for extraction.
    """
    print(f"Called youtube_transcript_summary_tool with URL {url}")
    try:
        video_content = download_transcript(url)
    except Exception as e:
        print(f"Error Occurred for [{url}]")
        return [url, f"Error Occurred : {e}"]

    print(f"Fetched Page Content of [{url}]")

    await asyncio.sleep(3)

    page_summary = await search_agent_function(video_content)

    print(f"AI returned Summary for {url}")

    return [url,page_summary]




"""Addd this code in above calls to prevent 429 errors"""


def make_request_with_retry(url, max_retries=5, initial_delay=1):
    """
    Makes an HTTP GET request to the given URL, with retry logic for 429 errors.

    Args:
        url (str): The URL to request.
        max_retries (int): The maximum number of retry attempts.
        initial_delay (int): The initial delay in seconds before retrying.

    Returns:
        requests.Response: The response object if successful, None otherwise.
    """
    retries = 0
    current_delay = initial_delay

    while retries < max_retries:
        try:
            response = requests.get(url)

            if response.status_code == 429:
                # Server sent a Retry-After header
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    try:
                        # Attempt to parse as seconds or a date
                        wait_time = int(retry_after)
                    except ValueError:
                        # If it's a date, calculate the time until then
                        # This requires more complex date parsing, for simplicity,
                        # we'll just use a default or exponential backoff here.
                        print(f"Warning: 'Retry-After' header is a date, using default delay.")
                        wait_time = current_delay
                else:
                    # No Retry-After header, use exponential backoff
                    wait_time = current_delay

                print(f"Rate limit hit (429). Retrying after {wait_time} seconds...")
                time.sleep(wait_time)
                current_delay *= 2  # Exponential backoff
                retries += 1
            elif response.status_code == 200:
                return response  # Success
            else:
                print(f"Request failed with status code: {response.status_code}")
                return None  # Handle other HTTP errors as needed

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the request: {e}")
            return None

    print(f"Max retries ({max_retries}) exceeded for {url}.")
    return None

# Example usage:
api_url = "https://api.example.com/data"  # Replace with your actual API endpoint
response = make_request_with_retry(api_url)

if response:
    print("Request successful!")
    print(response.json())
else:
    print("Failed to get a successful response.")