from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)
import warnings

warnings.filterwarnings("ignore")

RemoteBuyWineAgent = RemoteA2aAgent(
    name="buy_wine_agent",
    description="Remote buy wine agent from external server that provides the website URL to use.",
    # Point to the agent card URL - this is where the A2A protocol metadata lives
    agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
)