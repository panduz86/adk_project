import logging

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, FunctionTool
from .shared_library.helper import LLM_MODEL, retry_config
from .shared_library.tools import retrieve_wines
from .sub_agents.store_wine import StoreWineAgent

# Root Coordinator: Orchestrates the workflow by calling the sub-agents as tools.
root_agent = Agent(
    name="root_agent",
    model=Gemini(model=LLM_MODEL, retry_options=retry_config),
    description="Agent to coordinate wine cellar management and recommendations.",
    # This instruction tells the root agent HOW to use its tools (which are the other agents).
    instruction="""
        Your goal is to answer the user's query by orchestrating a workflow.
        
        You have access to the following tools:
        1. retrieve_wines: Provides a list of wines available in the cellar.
        2. store_wine_agent: Given a wine name, it retrieves detailed information about the wine and stores it in the cellar.
        
        You manage only these kind of requests:
        1. wine recommendations
        2. cellar inventory inquiries
        3. store a new wine in the cellar
        4. all other requests should be politely declined.
        
        Directives to follow **always**:
        - When a user asks for wine recommendations, use the retrieve_wines tool to get the list of wines. Analyze the list based on the user's preferences (e.g., meal pairings, wine colour, country of origin) and recommend the most suitable wines.
        - When a user raise question about the cellar inventory, use the retrieve_wines tool to get the list of wines.
        - When a user wants to store a new wine, use the store_wine_agent tool and after successfully storing a wine, **always** respond by confirming the action and then immediately list the details of the wine that was stored

    """,
    tools=[FunctionTool(retrieve_wines), AgentTool(StoreWineAgent)],
)

