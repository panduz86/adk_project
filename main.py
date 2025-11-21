from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from agents import root_agent
import asyncio

async def main():
    load_dotenv()
    
    runner = InMemoryRunner(agent=root_agent)
    response = await runner.run_debug("What are the latest advancements in quantum computing and what do they mean for AI?")
    print("Final Response from Root Agent:")
    print(response)
    

if __name__ == "__main__":
    asyncio.run(main())
