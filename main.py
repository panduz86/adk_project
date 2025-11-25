from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agents.agent import root_agent
from helper import APP_NAME, run_session
import asyncio



async def main():
    load_dotenv()
    
    session_service = InMemorySessionService()
    
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

    session_name = "stateful-agentic-session"
    
    print("Enter messages to send to the agent. Type 'exit' or 'quit' to stop.")
    try:
        while True:
            # use asyncio.to_thread so input() doesn't block the event loop
            user_input = await asyncio.to_thread(input, "> ")
            if not user_input:
                continue
            if user_input.strip().lower() in ("exit", "quit"):
                break
            await run_session(
               runner,
                [user_input],
                session_service=session_service,
                session_name=session_name,
            )
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")

    

if __name__ == "__main__":
    asyncio.run(main())
