from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from ..shared_library.helper import LLM_MODEL, retry_config

# Retrieve Information Agent: Its job is to use the google_search tool and present findings.
RetrieveWineInformationAgent = Agent(
    name="retrieve_wine_information_agent",
    model=Gemini(model=LLM_MODEL, retry_options=retry_config),
    instruction="""You are a specialized research agent. Your only job is to use the
    google_search tool to find 2-3 pieces of relevant information on the given wine.""",
    tools=[google_search],
    output_key="research_findings", # The result of this agent will be stored in the session state with this key.
)


# Summarizer Agent: Its job is to summarize the text it receives.
WriterAgent = Agent(
    name="writer_agent",
    model=Gemini(model=LLM_MODEL, retry_options=retry_config),
    instruction="""Read the provided research findings: {research_findings}
    Create a JSON summary of the wine with the following fields:
	- name: wine name
	- producer: winery or producer
	- year: vintage year (int)
	- colour: 'red'|'white'|'rosé'|'sparkling'
	- country_origin: country of origin
	- grape_variety: primary grape or blend description
	- best_meals: list of meal pairing suggestions
    Ensure the summary is concise and captures all key details.
    Reply only with the JSON object
    """,
    output_key="final_summary",
)

StoreWineAgent = SequentialAgent(
    name="store_wine_agent",
    description="Agent to retrieve detailed information about a wine, store it in the cellar, and provide the json object to the user.",
    sub_agents=[RetrieveWineInformationAgent, WriterAgent],
)