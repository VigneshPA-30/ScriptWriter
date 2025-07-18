from agents import Agent, Runner , trace 
from backend.mcp_servers import playwright_srv
from backend.prompts import research_prompt,search_prompt
from backend.tools import search_web
from dotenv import load_dotenv

load_dotenv()


async def agents_for_research(user_niche:str):
    print("Inside AGENTS")
    print(50*"#")
    async with playwright_srv as pw_srv:
            search_agent = Agent(
                name="search_agent_tool",
                model="gpt-4o-mini",
                instructions=search_prompt,
                mcp_servers=[pw_srv]        # ← key change
            )

            search_agent_tool = search_agent.as_tool( 
                    tool_name = "search_agent_tool",
                    tool_description = "This tool takes in a URL as a string and returns a summary of the page content"
                )


    async with playwright_srv as pw_srv:
        agent = Agent(
                    name="Browser-Bot",
                    model="gpt-4.1-mini",
                    instructions=research_prompt,
                    tools=[search_web,search_agent_tool]          # ← key change
                )

        with trace("Viral Topic Agent"):
                    result = await Runner.run(
                        starting_agent=agent,
                        input=f"Topics that will go viral in niche {user_niche}, If you encounter any technical difficulty while calling a tool tell me in detail what problem you faced",
                        max_turns=15
                    )

    return result.final_output