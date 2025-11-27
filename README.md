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

> 📊 **[View Detailed Architecture Diagram](./architecture_diagram.md)** - Complete visual architecture with component interactions and data flows

The system uses a hierarchical multi-agent architecture with three key integration patterns:

### 🎯 Root Agent (Coordinator)
The **root_agent** acts as the main orchestrator, managing all wine cellar operations:
- Wine recommendations based on preferences, meal pairings, and origin
- Cellar inventory queries and management
- Delegation to specialized agents and tools
- Review management coordination
- Purchase assistance workflow

**Tools Available**:
- `retrieve_wines`: Direct function tool for cellar inventory
- `mcp_review_wine_server`: MCP server integration (6 review operations)

**Sub-Agents**:
- `StoreWineAgent`: Local sequential agent for adding wines
- `RemoteBuyWineAgent`: Remote A2A agent for purchase assistance

### 📦 Local Sub-Agents

#### StoreWineAgent (Sequential Pipeline)
A two-stage pipeline that automatically researches and stores wines:

1. **Retrieve Wine Information Agent**
   - Uses Google Search to gather wine details
   - Finds 2-3 relevant information sources
   - Output stored in session state as `research_findings`

2. **Writer Agent**
   - Synthesizes research into structured JSON
   - Fields: name, producer, year, colour, country, grape variety, meal pairings
   - Output stored as `final_summary`

### 🌐 Remote A2A Agents

#### Buy Wine Agent (Port 8001)
An independent microservice using **Agent-to-Agent (A2A) protocol**:
- Discovers purchase URLs for specified wines
- Uses Google Search to find 2-3 best retail websites
- Communicates via A2A protocol with agent card
- Runs independently on dedicated port
- Scalable and separately deployable

**Endpoint**: `http://localhost:8001/.well-known/agent`

### 🔌 MCP Servers

#### Wine Review MCP Server (Port 8002)
A **Model Context Protocol (MCP)** server providing standardized review tools:

**Available Tools**:
- `create_review`: Add reviews with ratings, notes, reviewer, and price
- `get_review`: Retrieve specific review by ID
- `list_reviews`: Filter by wine name or minimum rating
- `delete_review`: Remove reviews
- `get_average_rating`: Calculate average rating for wines
- `search_reviews`: Search by keywords in tasting notes

**Technical Details**:
- Built with FastMCP framework
- HTTP transport on port 8002
- In-memory storage with sample data
- JSON response format with status/data structure

**Endpoint**: `http://localhost:8002/mcp`

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
make run-review-mcp-server # This starts the MCP server on http://localhost:8002
make run-buy-agent-server # This starts the remote A2A agent on http://localhost:8001

adk eval wine_cellar agents_tests/integration.evalset.json --config_file_path=agents_tests/test_config.json --print_detailed_results
```

This command:
- Evaluates the agent system using test cases defined in `integration.evalset.json`
- Uses configuration from `test_config.json`
- Prints detailed results for each test scenario


## Project Structure

```
adk_project/
├── main.py                          # Application entry point
├── architecture_diagram.md          # 📊 Visual architecture documentation
├── wine_cellar/
│   ├── agent.py                    # Root coordinator agent
│   ├── shared_library/             # Shared utilities and data
│   │   ├── tools.py                # Wine retrieval function tool
│   │   ├── helper.py               # LLM config, retry logic, utilities
│   │   ├── wine_data.py            # In-memory WINES and REVIEWS data
│   │   └── mcp_client.py           # MCP server HTTP connection setup
│   ├── sub_agents/                 # Local sub-agents
│   │   ├── store_wine.py           # Sequential pipeline: Research → Writer
│   │   └── buy_wine.py             # Remote A2A agent connector
│   ├── a2a_agents/                 # Remote agent-to-agent services
│   │   ├── buy_wine_server.py      # Buy Wine Agent definition (port 8001)
│   │   └── run_buy_wine_a2a.py     # Server startup script
│   └── mcp_servers/                # Model Context Protocol servers
│       └── review_server.py        # Review management MCP server (port 8002)
├── agents_tests/                    # Integration tests
│   ├── integration.evalset.json    # ADK evaluation test cases
│   └── test_config.json            # Test configuration
├── tests/                           # Unit tests
│   ├── test_tools.py               # Wine tools unit tests
│   └── test_review_server.py       # Review server unit tests
├── pyproject.toml                   # Project dependencies and metadata
├── Makefile                         # Build, run, and test commands
└── README.md                        # This file
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Agent Framework** | Google ADK | Multi-agent orchestration and coordination |
| **LLM** | Gemini (Google) | Natural language understanding and generation |
| **A2A Protocol** | Agent-to-Agent | Distributed agent communication via microservices |
| **MCP Protocol** | Model Context Protocol | Standardized tool integration via HTTP |
| **MCP Framework** | FastMCP | Lightweight framework for building MCP servers |
| **External Tools** | Google Search API | Automated web research and information retrieval |
| **Web Server** | uvicorn (ASGI) | Hosting A2A agents and MCP servers |
| **Testing** | pytest | Unit and integration testing |
| **Async Runtime** | asyncio | Asynchronous session and connection management |
| **Data Storage** | In-memory dictionaries | Fast access for development/demo purposes |

## Configuration

The application uses these key configurations (in `wine_cellar/shared_library/helper.py`):
- **LLM Model**: Configurable Gemini model selection
- **Retry Logic**: Automatic retry on API failures
- **Session Management**: In-memory session service for stateful conversations

The MCP server connection is configured in `wine_cellar/shared_library/mcp_client.py`:
- **MCP URL**: `http://localhost:8002/mcp`
- **Connection Type**: Streamable HTTP

## Development Guide

> 💡 **Tip**: Review the [Architecture Diagram](./architecture_diagram.md) to understand component interactions before making changes

### Understanding the Architecture

The application follows three key architectural patterns:

1. **Local Sequential Agents**: For multi-step operations (e.g., Store Wine pipeline)
2. **Remote A2A Agents**: For distributed, independently scalable services (e.g., Buy Wine)
3. **MCP Servers**: For standardized tool integration (e.g., Review Server)

Refer to `architecture_diagram.md` for visual representation and data flow diagrams.

### Developing MCP Servers

The Wine Review MCP Server demonstrates Model Context Protocol integration:

**Characteristics**:
- Independent HTTP service (port 8002)
- FastMCP framework for rapid development
- Exposes tools via `/mcp` endpoint
- Stateless with in-memory storage
- JSON response format: `{"status": "success|error", "data": ...}`

**Development Workflow**:
1. Edit `wine_cellar/mcp_servers/review_server.py`
2. Add new tools using `@mcp.tool()` decorator
3. Restart server: `make run-review-mcp-server`
4. Test at: `http://localhost:8002/mcp`

**Best Practices**:
- Keep tools focused and single-purpose
- Return consistent JSON structure
- Validate inputs and provide clear error messages
- Use type hints for all parameters

### Developing A2A Agents

The Buy Wine Agent demonstrates Agent-to-Agent architecture:

**Characteristics**:
- Independent microservice (port 8001)
- Exposes agent card via `.well-known` endpoint
- Communicates using A2A protocol
- Independently deployable and scalable
- Can be written in any language/framework

**Development Workflow**:
1. Edit `wine_cellar/a2a_agents/buy_wine_server.py`
2. Modify agent definition (model, instructions, tools)
3. Restart server: `make run-buy-agent-server`
4. Verify agent card: `http://localhost:8001/.well-known/agent`

**Best Practices**:
- Keep agents focused on single domains
- Document agent capabilities in description
- Use clear, specific instructions
- Return structured responses

### Extending the System

**Adding New Wines**:
- Via conversation: "Store a new wine: [wine name]"
- Via code: Edit `WINES` list in `wine_cellar/shared_library/wine_data.py`

**Adding Sample Reviews**:
- Edit `FAKE_REVIEWS` dictionary in `wine_cellar/shared_library/wine_data.py`
- Restart MCP server to reload data

**Adding New Agents**:
1. Create agent file in `wine_cellar/sub_agents/` or `wine_cellar/a2a_agents/`
2. Choose pattern: Sequential, A2A, or simple Agent
3. Register in root agent (`wine_cellar/agent.py`):
   - As tool: `tools=[AgentTool(YourAgent)]`
   - As sub-agent: `sub_agents=[YourAgent]`
4. Update root agent instructions with new workflow
5. Add integration tests

**Adding New Tools**:
- For simple functions: Add to `wine_cellar/shared_library/tools.py`
- For complex services: Create new MCP server in `wine_cellar/mcp_servers/`
- For external agents: Use A2A protocol with remote agent

**Modifying the Orchestration**:
- Edit root agent instructions in `wine_cellar/agent.py`
- Update tool/sub-agent descriptions
- Test changes with integration test suite

