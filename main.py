import asyncio
from backend.agents import agents_for_research
from backend.utils import user_niche


async def main():
    print("Hello from Scriptwriter!")
     
    result = await agents_for_research(user_niche)
     


if __name__ == "__main__":
   asyncio.run(main())
