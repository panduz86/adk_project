from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, FunctionTool
from .shared_library.helper import LLM_MODEL, retry_config
from .shared_library.tools import retrieve_wines
from .shared_library.mcp_client import mcp_review_wine_server
from .sub_agents.store_wine import StoreWineAgent
from .sub_agents.buy_wine import RemoteBuyWineAgent

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
        3. mcp_review_wine_server: Manages wine reviews with tools to create, retrieve, list, search, and delete reviews. Can filter by wine name/rating, search tasting notes by keyword, and calculate average ratings. Reviews include wine name, vintage, rating (1-5), tasting notes, reviewer name, and optional price.
        
        You have access to the following sub agents:
        1. buy_wine_agent: Given a wine name, it proposes the URLs of the best websites where to buy the wine.
        
        You manage only these kind of requests:
        1. wine recommendations
        2. cellar inventory inquiries
        3. store a new wine in the cellar
        4. buy a wine on Internet
        5. manage the reviews of the wines
        6. all other requests should be politely declined.
        
        Directives to follow **always**:
        - When an user asks for wine recommendations, use the retrieve_wines tool to get the list of wines. Analyze the list based on the user's preferences (e.g., meal pairings, wine colour, country of origin) and recommend the most suitable wines.
        - When an user raise question about the cellar inventory, use the retrieve_wines tool to get the list of wines.
        - When an user wants to store a new wine, use the store_wine_agent tool and after successfully storing a wine, **always** respond by confirming the action and then immediately list the details of the wine that was stored
        - When an user wants to buy a wine, use the sub agent buy_wine_agent which will provide you the URLs of the best websites where to buy the wine. **Always** provide the URLs found to the user.
        - When an user want to create, retrieve, list, search, and delete reviews, use the tool mcp_review_wine_server
        - If the user's request does not fall into one of these categories, politely inform them that you are unable to assist with that request.

    """,
    tools=[FunctionTool(retrieve_wines), AgentTool(StoreWineAgent),mcp_review_wine_server],
    sub_agents=[RemoteBuyWineAgent]
)

