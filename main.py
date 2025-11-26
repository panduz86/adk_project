from dotenv import load_dotenv
import asyncio
import argparse

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from wine_cellar.agent import root_agent
from google.adk.plugins.logging_plugin import (
    LoggingPlugin,
)

from wine_cellar.shared_library.helper import APP_NAME, run_session


async def main():
    parser = argparse.ArgumentParser(description="Run the agent with optional debug logging")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging with LoggingPlugin")
    args = parser.parse_args()
    
    load_dotenv()
    
    session_service = InMemorySessionService()
    
    plugins = [LoggingPlugin()] if args.debug else []
    
    runner = Runner(agent=root_agent, 
                    app_name=APP_NAME, 
                    session_service=session_service,
                    plugins=plugins
                    )

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
