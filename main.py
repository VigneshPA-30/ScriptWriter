import asyncio
from backend.agents import agents_for_research
from backend.utils import user_niche
from IPython.display import Markdown, display
from agents import run_demo_loop

async def main():
    print("Hello from Scriptwriter!")
     
    result = await agents_for_research(user_niche)
     
    print("FINAL SCRIPT :")

    
    print(result[3])


if __name__ == "__main__":
   asyncio.run(main())
