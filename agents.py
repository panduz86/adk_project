from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, FunctionTool, google_search
from helper import LLM_MODEL, retry_config
from tools import retrieve_wines


# Research Agent: Its job is to use the google_search tool and present findings.
# research_agent = Agent(
#     name="ResearchAgent",
#     model=Gemini(model=LLM_MODEL, retry_options=retry_config),
#     instruction="""You are a specialized research agent. Your only job is to use the
#     google_search tool to find 2-3 pieces of relevant information on the given topic and present the findings with citations.""",
#     tools=[google_search],
#     output_key="research_findings", # The result of this agent will be stored in the session state with this key.
# )


# Summarizer Agent: Its job is to summarize the text it receives.
# summarizer_agent = Agent(
#     name="SummarizerAgent",
#     model=Gemini(model=LLM_MODEL, retry_options=retry_config),
#     # The instruction is modified to request a bulleted list for a clear output format.
#     instruction="""Read the provided research findings: {research_findings}
# Create a concise summary as a bulleted list with 3-5 key points.""",
#     output_key="final_summary",
# )


# Root Coordinator: Orchestrates the workflow by calling the sub-agents as tools.
root_agent = Agent(
    name="WineCellarCoordinator",
    model=Gemini(model=LLM_MODEL, retry_options=retry_config),
    description="Agent to coordinate wine cellar management and recommendations.",
    # This instruction tells the root agent HOW to use its tools (which are the other agents).
    instruction="""
        Your goal is to answer the user's query by orchestrating a workflow.
        
        You have access to the following tools:
        1. retrieve_wines: Provides a list of wines available in the cellar.
        
        When a user asks for wine recommendations, use the retrieve_wines tool to get the list of wines.
        Analyze the list based on the user's preferences (e.g., meal pairings, wine colour, country of origin) and recommend the most suitable wines.

    """,
    tools=[FunctionTool(retrieve_wines)],
)

