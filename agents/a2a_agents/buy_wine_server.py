from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from agents.shared_library.helper import LLM_MODEL, retry_config

BuyWineAgent = Agent(
    name="buy_wine_agent",
    model=Gemini(model=LLM_MODEL, retry_options=retry_config),
    description="Agent for buying wines",
    instruction="""You are a specialized for buying wine.
    When you receive a query with the name of a wine to buy, you have to search for the best 2-3 websites
    where to buy it using the google_search tool.
    You must return the URLs of the websites found.
    Example query: "Where can I buy the wine 'Batasiolo Barolo Riserva 2014'?"
    Example response: "You can buy 'Batasiolo Barolo Riserva 2014' at the following websites: [list of URLs]"
    """,
    tools=[google_search],
    output_key="how_to_buy_findings"
)

app = to_a2a(
    BuyWineAgent, port=8001  # Port where this agent will be served
)