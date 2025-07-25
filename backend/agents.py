from agents import Agent, Runner , trace 
from backend.prompts import research_prompt,topic_research_prompt,script_prompt,hook_prompt
from backend.tools import search_web, get_search_agent_tool, get_page_content
from dotenv import load_dotenv
from backend.models import gemini_model
from typing import List
import asyncio




load_dotenv()

def choice_selector(user_choices:List):
    return 3
             

async def agents_for_research(user_niche:str) -> List:
    print("Inside AGENTS")
    print("\n\n")
    final_results =[]



    research_agents_kwargs = {
                "model":gemini_model,
                "tools":[search_web, get_search_agent_tool]
    }

    research_agent = Agent(
                name = "research-bot",
                **research_agents_kwargs,
                instructions = research_prompt
                #output_type = ResearchOutputList
            )

    topic_research_agent = Agent(
                name = "Topic-Research_Bot",
                **research_agents_kwargs,
                instructions=topic_research_prompt,    
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
            
            print("Starting Searching Agent...")

            result =  await Runner.run(
                    starting_agent=research_agent,
                    input=f"Topics that will go viral in niche {user_niche}, If you encounter any technical difficulty while calling a tool tell me in detail what problem you faced",
                    max_turns=15,
            )
  
            final_result = result.final_output

            final_results.append(final_result)
            user_choice = choice_selector(result.final_output)

            #  user_topic = final_results[0].research_list[user_choice]
            print(f"\n\n{final_result}\n")
            print(f"{10*"-"}Passing the work to Topic Research Agent in 5 seconds{10*"-"}")
            print("\n")

            await asyncio.sleep(1)

            result = await Runner.run(
                    starting_agent = topic_research_agent,
                    input = f"Use the {user_choice}rd topic from this {final_result} and do research only for that topic.",
                    max_turns=25,
                    # hooks = DelayHook(tell_the_agent = True)
            )

                    
            final_result = result.final_output
            final_results.append(final_result)

            print(f"\n\nREPORT:\n{final_results[1]}")

            print("\n")
            print(f"{10*"-"}Passing the work to Hook Agent in 5 seconds{10*"-"}")
    

            await asyncio.sleep(1)

            result = await Runner.run(
                    starting_agent = hook_agent,
                    input = f"here is the report you can use to create hook \n {final_results[1]}",
                    max_turns=25,
            )

            final_result = result.final_output
            final_results.append(final_result)

            print("\n")
            print(f"HOOK:{final_results[2]}")
            

            print("\n\n")
            print(f"{10*"-"}Passing the work to Script Agent in 5 seconds{10*"-"}")
            

            await asyncio.sleep(1)

            result = await Runner.run(
                    starting_agent = script_agent,
                    input = f"Use this Hook to create the script --\n {final_results[2]}\n\n Use this report of information for the Script:\n{final_results[1]} ",
                    max_turns=25,
            )

            final_result = result.final_output
            final_results.append(final_result)
            print("\n")
            print(f"SCRIPT:\n{final_results[3]}")
                 

    return final_results
