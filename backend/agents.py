from agents import Agent, Runner , trace 
from .prompts import research_prompt,topic_research_prompt,script_prompt,hook_prompt
from .tools import search_web, get_search_agent_tool,youtube_transcript_summary_tool
from dotenv import load_dotenv
from .models import gemini_model
from .output_format import ResearchOutputList
from typing import List
import asyncio
import json
import time
import random



load_dotenv()

# --- Agent Definitions ---
# It's good practice to define agents once if they are stateless.
research_agents_kwargs = {
    "model": gemini_model,
    "tools": [search_web, get_search_agent_tool,youtube_transcript_summary_tool]
}

research_agent = Agent(
    name="research-bot",
    **research_agents_kwargs,
    instructions=research_prompt,
    #output_type=ResearchOutputList  # Use Pydantic for structured output
)

topic_research_agent = Agent(
    name="Topic-Research_Bot",
    **research_agents_kwargs,
    instructions=topic_research_prompt,
)

hook_agent = Agent(
    name="Hook_Bot",
    model=gemini_model,
    instructions=hook_prompt
)

script_agent = Agent(
    name="Script_Bot",
    model=gemini_model,
    instructions=script_prompt
)

#  ---Exponentital backOff---



async def run_with_retry(*args, max_retries=5, **kwargs):
    for attempt in range(max_retries):
        try:
            return await Runner.run(*args, **kwargs)
        except Exception as e:
            # Check for retryable error
            if hasattr(e, "args") and any("retryDelay" in str(arg) for arg in e.args):
                # Extract retry delay if present, else use exponential backoff
                delay = 2 ** attempt
                for arg in e.args:
                    if "retryDelay" in str(arg):
                        import re
                        match = re.search(r'"retryDelay":\s*"(\d+)s"', str(arg))
                        if match:
                            delay = int(match.group(1))
                print(f"Rate limited. Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                raise
    raise RuntimeError("Max retries exceeded for Runner.run")

# --- Service Functions for API ---

async def get_topic_ideas(user_niche: str) :
    """
    Runs the research agent to generate a list of topic ideas for a given niche.
    """
    print("Starting research for topic ideas...")
    with trace("Topic search"):
        result = await run_with_retry(
            starting_agent=research_agent,
            input=f"Topics that will go viral in niche {user_niche}, If you encounter any technical difficulty while calling a tool tell me in detail what problem you faced",
            max_turns=25,
        )
    print(f"Finished research for topic Ideas with type {type(result.final_output)}")

    return result.final_output

async def research_topic(topic: str, topic_selected:int) -> str:
    """
    Runs the topic research agent to generate a detailed report on a given topic.
    """
    print(f"Starting in-depth research for topic: {topic}")
    if topic_selected ==0:topic_selected = random.randint(1,6)
    with trace("Topic research"):
        result = await run_with_retry(
            starting_agent=topic_research_agent,
            input=f"Do in-depth research only for the topic number : {topic_selected} only : {topic}. The user has selected the topic number : {topic_selected}, so research only for that topic",
            max_turns=25,
        )
    print(f"Finished in-depth research for topic number {topic_selected} with type {type(result.final_output)}")
    
    return result.final_output

async def generate_hook(research_report: str) -> str:
    """
    Generates a hook based on a research report.
    """
    print("Starting hook generation...")
    with trace("Hook generation"):
        result = await run_with_retry(
            starting_agent=hook_agent,
            input=f"here is the report you can use to create hook \n {research_report}",
            max_turns=25,
        )
    print("Finished hook generation.")
    return result.final_output

async def generate_script(hook: str, research_report: str) -> str:
    """
    Generates a full script based on a hook and a research report.
    """
    print("Starting script generation...")
    with trace("Script generation"):
        result = await run_with_retry(
            starting_agent=script_agent,
            input=f"Use this Hook to create the script --\n {hook}\n\n Use this report of information for the Script:\n{research_report} ",
            max_turns=25,
        )
    print("Finished script generation.")
    return result.final_output
