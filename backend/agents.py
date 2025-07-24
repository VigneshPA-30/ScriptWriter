from agents import Agent, Runner , trace , ItemHelpers, handoff, RunContextWrapper, OpenAIChatCompletionsModel
from backend.mcp_servers import playwright_srv
from backend.prompts import research_prompt,topic_research_prompt,script_prompt,hook_prompt
from backend.tools import search_web, get_search_agent_tool, get_page_content
from dotenv import load_dotenv
from backend.utils import complete_automatic, DelayHook
from backend.models import gemini_model
from backend.output_format import ResearchOutputList
from agents.extensions import handoff_filters
from typing import List
import asyncio
import os



load_dotenv()

def choice_selector(user_choices:List):
    return 3
             

async def agents_for_research(user_niche:str) -> List:
    print("Inside AGENTS")
    print("\n\n")
    final_results =[]



    async with playwright_srv as pw_srv:
        #search_agent_tool = await get_search_agent_tool(pw_srv, gemini_model)

        research_agents_kwargs = {
                    "model":gemini_model,
                    "tools":[search_web, get_search_agent_tool]
        }

        

        topic_research_agent = Agent(
                    name = "Topic-Research_Bot",
                    model=gemini_model,
                    tools=[search_web, get_search_agent_tool],
                    instructions=topic_research_prompt,    
        )

        research_agent = Agent(
                    name = "research-bot",
                    model=gemini_model,
                    tools=[search_web, get_search_agent_tool],
                    #output_type = ResearchOutputList
                )
        
        hook_agent = Agent(
              name = "Hook_Bot",
              model = gemini_model,
              instructions =hook_prompt
        )
        
        script_agent = Agent(
              name = "Script_Bot",
              model = gemini_model,
              instructions =script_prompt
        )
        
        '''
        should probabbly take all the inputs and put in seperate file ans call it for every loop
        '''

        with trace("Topic search"):

                    result =  await Runner.run(
                            starting_agent=research_agent,
                            input=f"Topics that will go viral in niche {user_niche}, If you encounter any technical difficulty while calling a tool tell me in detail what problem you faced",
                            max_turns=15,
                    )

                    # async for event in result.stream_events():
                                
                    #     if event.type == "raw_response_event":
                    #         continue
                               
                    #     elif event.type == "agent_updated_stream_event":
                    #         print(f"Agent updated: {event.new_agent.name}")
                    #         continue
                               
                    #     elif event.type == "run_item_stream_event":

                    #         if event.item.type == "tool_call_item":
                    #             print("-- Tool was called")
                    #         elif event.item.type == "tool_call_output_item":
                    #             print(f"-- Tool output: {event.item.output}")
                    #         elif event.item.type == "message_output_item":
                    #             print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
                    #             final_result = event.item
                    #         else:
                    #              pass  
                    final_result = result.final_output

                    final_results.append(final_result)
                    user_choice = choice_selector(result.final_output)

                  #  user_topic = final_results[0].research_list[user_choice]
                    print(f"{final_result}\n")
                    print("Passing the work to Topic Research Agent in 5 seconds")
                    print("\n\n")

                    await asyncio.sleep(10)

                    result = await Runner.run(
                           starting_agent = topic_research_agent,
                           input = f"Use the {user_choice} from this {final_result}",
                           max_turns=25,
                          # hooks = DelayHook(tell_the_agent = True)
                    )


                    # async for event in result.stream_events():
                                
                    #     if event.type == "raw_response_event":
                    #         continue
                               
                    #     elif event.type == "agent_updated_stream_event":
                    #         print(f"Agent updated: {event.new_agent.name}")
                    #         continue
                               
                    #     elif event.type == "run_item_stream_event":

                    #         if event.item.type == "tool_call_item":
                    #             print("-- Tool was called")
                    #         elif event.item.type == "tool_call_output_item":
                    #             print(f"-- Tool output: {event.item.output}")
                    #         elif event.item.type == "message_output_item":
                    #             print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
                    #             final_result = ItemHelpers.text_message_output(event.item)
                    #         else:
                    #              pass  
                            
                    final_result = result.final_output
                    final_results.append(final_result)

                    print(f"REPORT:\n{final_results[1]}")

                    print("\n\n")
                    print("Passing the work to Hook Agent in 5 seconds")
            

                    await asyncio.sleep(10)

                    result = await Runner.run(
                           starting_agent = hook_agent,
                           input = f"here is the report you can use to create hook \n {final_results[1]}",
                           max_turns=25,
                    )

                    final_result = result.final_output
                    final_results.append(final_result)

                    print("\n\n")
                    print(f"HOOK:\n{final_results[2]}")
                    

                    print("\n\n")
                    print("Passing the work to Script Agent in 5 seconds")
                   

                    await asyncio.sleep(10)

                    result = await Runner.run(
                           starting_agent = script_agent,
                           input = f"Use this Hook to create the script --\n {final_results[2]}\n\n Use this report of information for the Script:\n{final_results[1]} ",
                           max_turns=25,
                    )

                    final_result = result.final_output
                    final_results.append(final_result)
                    print("\n\n")
                    print(f"SCRIPT:\n{final_results[3]}")
                 

    return final_results
