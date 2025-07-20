from agents import Agent, Runner , trace , ItemHelpers, handoff, RunContextWrapper
from backend.mcp_servers import playwright_srv
from backend.prompts import research_prompt,search_prompt,topic_research_prompt
from backend.tools import search_web
from dotenv import load_dotenv
from backend.utils import complete_automatic, DelayHook
from backend.output_format import HandoffData
from agents.extensions import handoff_filters


load_dotenv()

final_result = ""

async def agents_for_research(user_niche:str):
    print("Inside AGENTS")
    print(50*"#")


    async with playwright_srv as pw_srv:
            
            search_agent_kwargs = {
                "name":"search_agent_tool",
                "model":"gpt-4o-mini",
                "instructions":search_prompt,
                "mcp_servers":[pw_srv]
            }

            search_agent = Agent(
                **search_agent_kwargs
            )

            search_agent_tool = search_agent.as_tool( 
                    tool_name = "search_agent_tool",
                    tool_description = "This tool takes in a URL as a string and returns a summary of the page content"
                )


    async with playwright_srv as pw_srv:

        research_agents_kwargs = {
                    "name":"Research_Bot",
                    "model":"gpt-4o-mini",
                    "tools":[search_web,search_agent_tool]
        }

        topic_research_agent = Agent(
                    **research_agents_kwargs,
                    instructions=topic_research_prompt,    
        )

        
        async def research_handoff(ctx:RunContextWrapper[HandoffData], input_data:HandoffData) -> HandoffData:
            print("INSIDE HANDOFF FUNCTION")
            print(50*"#")
            #user_choice = int(input("Select a topic number from 1 to 6 : "))
            user_choice = 3
            user_selection = f" The user selected the topic number - {user_choice}"if complete_automatic else "No User Input. Select any one from the given 6 topics"
            handoff_data = HandoffData(
                  agent_ip = input_data.agent_ip + input_data.user_input,
                  user_input = user_selection
            )
            print(handoff_data)
            print(50*"#")
            return handoff_data

        handoff_obj = handoff(
             topic_research_agent, 
             on_handoff=research_handoff, 
             input_type=HandoffData,
             input_filter = handoff_filters.remove_all_tools
        )

        research_agent = Agent(
                    **research_agents_kwargs,
                    instructions=research_prompt,
                    handoffs= [handoff_obj]
                )
        
        #delay_hook = DelayHook()

        with trace("Viral Topic Agent"):
                    result =  Runner.run_streamed(
                        starting_agent=research_agent,
                        input=f"Topics that will go viral in niche {user_niche}, If you encounter any technical difficulty while calling a tool tell me in detail what problem you faced",
                        max_turns=15,
                       # hooks= delay_hook
                    )

                    async for event in result.stream_events():
                                
                        if event.type == "raw_response_event":
                            continue
                               
                        elif event.type == "agent_updated_stream_event":
                            print(f"Agent updated: {event.new_agent.name}")
                            continue
                               
                        elif event.type == "run_item_stream_event":

                            if event.item.type == "tool_call_item":
                                print("-- Tool was called")
                            elif event.item.type == "tool_call_output_item":
                                print(f"-- Tool output: {event.item.output}")
                            elif event.item.type == "message_output_item":
                                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
                                final_result = ItemHelpers.text_message_output(event.item)
                            else:
                                 pass  


    return result.final_output
