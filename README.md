# Wine Cellar Management Agent

An intelligent wine cellar management system built with Google's Agent Development Kit (ADK). This project demonstrates a multi-agent architecture with MCP (Model Context Protocol) integration for managing wine recommendations, cellar inventory, reviews, and wine purchases.

## Overview

This application uses a coordinated multi-agent system to:
- Provide personalized wine recommendations based on meal pairings, colour, origin, and preferences
- Query and manage wine cellar inventory
- Automatically research and store new wines with detailed information
- Create, search, and manage wine reviews with ratings and tasting notes
- Find and recommend online retailers for purchasing specific wines

## Architecture

The system uses a hierarchical agent architecture with local sub-agents, remote A2A agents, and MCP (Model Context Protocol) servers:

### Root Agent
The **root_agent** acts as the main coordinator, orchestrating all workflows:
- Handles wine recommendations by analyzing cellar inventory
- Manages cellar inventory queries
- Delegates wine storage tasks to the specialized StoreWineAgent
- Coordinates with the remote BuyWineAgent for purchasing recommendations
- Integrates with the MCP Review Server for managing wine reviews
- Politely declines non-wine-related requests

### Sub-Agents

#### StoreWineAgent (Sequential Agent)
A two-stage sequential agent that stores new wines:

1. **RetrieveWineInformationAgent**: Uses Google Search to find 2-3 relevant pieces of information about the wine
2. **WriterAgent**: Synthesizes the research into a structured JSON summary with all wine details

#### BuyWineAgent (Remote A2A Agent)
An **Agent-to-Agent (A2A)** remote agent that helps users purchase wines:
- Runs as a separate microservice on port 8001
- Uses Google Search to find 2-3 best websites for purchasing specified wines
- Communicates with the root agent via the A2A protocol
- Returns URLs of recommended online retailers

### MCP Servers

#### Wine Review MCP Server
A **Model Context Protocol (MCP)** server that manages wine reviews:
- Runs as an independent service on port 8002
- Provides standardized tools for review management
- Maintains in-memory review database with persistent data
- Exposes tools via HTTP at `http://localhost:8002/mcp`
- Pre-populated with sample reviews for demonstration

## Features

- **Wine Recommendations**: Get personalized suggestions based on:
  - Meal pairings (e.g., "wine for steak dinner")
  - Wine colour preferences (red, white, rosé, sparkling)
  - Country of origin
  - Grape varieties

- **Inventory Management**: Query current cellar contents with detailed wine information

- **Smart Wine Storage**: Add new wines to the cellar with automatic information retrieval including:
  - Producer/winery details
  - Vintage year
  - Grape varieties
  - Optimal meal pairings

- **Wine Review Management**: Comprehensive review system powered by MCP server:
  - Create new reviews with ratings (1-5 stars), tasting notes, and prices
  - Search reviews by wine name, rating, or keywords in tasting notes
  - Calculate average ratings for specific wines
  - List and filter reviews by wine name or minimum rating
  - Delete reviews when needed
  - Pre-loaded with sample reviews for testing

- **Wine Purchase Assistance**: Find online retailers for purchasing wines:
  - Searches for best websites to buy specific wines
  - Returns curated list of URLs for online wine merchants
  - Powered by remote A2A agent architecture

- **Stateful Sessions**: Maintains conversation context across interactions

## Prerequisites

- Python 3.12 or higher
- Google ADK API access
- API keys configured in `.env` file

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd adk_project
```

2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up environment variables:
Create a `.env` file in the project root with your API credentials:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

### Running the Application

**Important**: The system requires two separate services to be running for full functionality:

1. **Start the Wine Review MCP Server** (required for review features):
```bash
make run-review-mcp-server
# This starts the MCP server on http://localhost:8002
```

2. **Start the Buy Wine Agent Server** (required for wine purchase features):
```bash
make run-buy-agent-server
# This starts the remote A2A agent on http://localhost:8001
```

3. **Start the main application** (in a separate terminal):
```bash
make run
# or
python main.py
```

For debug logging:
```bash
make run-debug
# or
python main.py --debug
```

### Example Interactions

```
> What wines do you have?
[Returns list of all wines in the cellar with details]

> Recommend a wine for grilled steak
[Analyzes cellar and suggests wines that pair well with steak]

> Store a new wine: Opus One 2019
[Researches the wine and stores it with complete details]

> What white wines are from France?
[Filters and returns French white wines from inventory]

> Create a review for Barolo 2013 with rating 5 and notes "Exceptional wine with truffle notes"
[Creates a new review in the MCP server database]

> Show me all reviews for Château Margaux
[Retrieves and displays all reviews for the specified wine]

> What's the average rating for Barolo?
[Calculates and returns the average rating from all Barolo reviews]

> Search reviews for the keyword "fruity"
[Finds all reviews with "fruity" in the tasting notes]

> I want to buy the wine "Batasiolo Barolo Riserva 2014"
[Searches for best websites to purchase the wine and returns URLs]
```

Type `exit` or `quit` to stop the application.

### Running Tests

#### Unit Tests

Execute the unit test suite:
```bash
make test
# or
pytest tests/
```

The test suite includes:

**Wine Tools Tests** (`tests/test_tools.py`):
- Validates wine retrieval functionality
- Verifies data structure and count

**Review Server Tests** (`tests/test_review_server.py`):
- `TestCreateReview`: Tests review creation with various parameters and validation
- `TestGetReview`: Tests retrieving reviews by ID
- `TestListReviews`: Tests listing and filtering reviews by wine name and rating
- `TestDeleteReview`: Tests review deletion
- `TestGetAverageRating`: Tests average rating calculation for wines
- `TestSearchReviews`: Tests keyword search in tasting notes
- `TestIntegrationScenarios`: End-to-end workflows combining multiple operations

Run specific test files:
```bash
pytest tests/test_review_server.py -v  # Review server tests with verbose output
pytest tests/test_tools.py -v          # Wine tools tests with verbose output
```

#### Integration Tests

Run integration tests using ADK's evaluation framework:
```bash
adk eval agents agents_tests/integration.evalset.json --config_file_path=agents_tests/test_config.json --print_detailed_results
```

This command:
- Evaluates the agent system using test cases defined in `integration.evalset.json`
- Uses configuration from `test_config.json`
- Prints detailed results for each test scenario

The integration tests validate end-to-end functionality including:
- Wine recommendation queries
- Cellar inventory management
- New wine storage with automatic research
- Wine purchase website recommendations
- Wine review creation and retrieval

## Project Structure

```
adk_project/
├── main.py                          # Application entry point
├── wine_cellar/
│   ├── agent.py                    # Root coordinator agent
│   ├── shared_library/
│   │   ├── tools.py                # Wine retrieval functions
│   │   ├── helper.py               # Utility functions and configurations
│   │   ├── wine_data.py            # Shared wine and review data
│   │   └── mcp_client.py           # MCP server connection setup
│   ├── sub_agents/
│   │   ├── store_wine.py           # Sequential agent for storing wines
│   │   └── buy_wine.py             # Remote A2A agent connector
│   ├── a2a_agents/
│   │   ├── buy_wine_server.py      # Buy Wine Agent server definition
│   │   └── run_buy_wine_a2a.py     # Server startup script
│   └── mcp_servers/
│       └── review_server.py        # Wine Review MCP server
├── agents_tests/
│   ├── integration.evalset.json    # Integration test cases
│   └── test_config.json            # Test configuration
├── tests/
│   ├── test_tools.py               # Wine tools unit tests
│   └── test_review_server.py       # Review server unit tests
├── pyproject.toml                   # Project dependencies
├── Makefile                         # Build and run commands
└── README.md                        # This file
```

## Technology Stack

- **Google ADK (Agent Development Kit)**: Multi-agent orchestration framework
- **Agent-to-Agent (A2A) Protocol**: Enables distributed agent communication via microservices
- **Model Context Protocol (MCP)**: Standardized protocol for tool integration via HTTP
- **FastMCP**: Lightweight framework for building MCP servers
- **Gemini LLM**: Google's large language model for natural language understanding
- **Google Search Tool**: Automated web research capability
- **uvicorn**: ASGI server for hosting A2A agents and MCP servers
- **pytest**: Testing framework
- **asyncio**: Asynchronous session management

## Configuration

The application uses these key configurations (in `wine_cellar/shared_library/helper.py`):
- **LLM Model**: Configurable Gemini model selection
- **Retry Logic**: Automatic retry on API failures
- **Session Management**: In-memory session service for stateful conversations

The MCP server connection is configured in `wine_cellar/shared_library/mcp_client.py`:
- **MCP URL**: `http://localhost:8002/mcp`
- **Connection Type**: Streamable HTTP

## Development

### Model Context Protocol (MCP) Server

The Wine Review MCP Server demonstrates MCP integration:
- Runs as an independent HTTP service on port 8002
- Built with FastMCP framework for simplicity
- Exposes standardized tools via `/mcp` endpoint
- Uses in-memory storage with pre-populated sample data
- Provides six review management operations:
  - `create_review`: Add new wine reviews
  - `get_review`: Retrieve specific review by ID
  - `list_reviews`: List all reviews with optional filtering
  - `delete_review`: Remove a review
  - `get_average_rating`: Calculate average rating for a wine
  - `search_reviews`: Search reviews by keywords

To develop or modify the Review MCP Server:
1. Edit `wine_cellar/mcp_servers/review_server.py`
2. Restart the server: `make run-review-mcp-server`
3. The server will be available at: `http://localhost:8002/mcp`

### Agent-to-Agent (A2A) Architecture

The Buy Wine Agent demonstrates A2A architecture:
- Runs as an independent microservice on port 8001
- Exposes agent capabilities via HTTP endpoints
- Uses the A2A protocol for inter-agent communication
- Can be deployed and scaled independently from the main application

To develop or modify the Buy Wine Agent:
1. Edit `wine_cellar/a2a_agents/buy_wine_server.py`
2. Restart the server: `make run-buy-agent-server`
3. The agent card is available at: `http://localhost:8001/.well-known/agent-card.json`

### Adding New Wines

Wines can be added through conversation or by modifying the `WINES` list in `wine_cellar/shared_library/wine_data.py`.

### Adding Sample Reviews

Sample reviews can be added by modifying the `FAKE_REVIEWS` dictionary in `wine_cellar/shared_library/wine_data.py`.

### Extending Functionality

To add new capabilities:
1. Create new agent in `wine_cellar/` or `wine_cellar/sub_agents/`
2. Register as a tool or sub-agent in the root agent
3. Update root agent instructions to include new workflow
4. For external services, consider creating a new MCP server in `wine_cellar/mcp_servers/`

