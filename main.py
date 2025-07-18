import asyncio
from backend.agents import agents_for_research

def main():
    print("Hello from scriptwriter!")
    print(50*"#")
    result = asyncio.run(agents_for_research("best non AI startups"))
    print(result)


if __name__ == "__main__":
    main()
