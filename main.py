import asyncio
from backend.agents import agents_for_research
from backend.utils import user_niche
from IPython.display import Markdown, display
from agents import run_demo_loop

async def main():
    print("Hello from scriptwriter!")
    print(50*"#")
    result = await agents_for_research(user_niche)
    print(50*"#")
    print("RESULT FROM THE AGENTIC FRAMEWORK")
    print(result)


if __name__ == "__main__":
   asyncio.run(main())
