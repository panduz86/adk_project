# Wine Cellar Management Agent

An intelligent wine cellar management system built with Google's Agent Development Kit (ADK). This project demonstrates a multi-agent architecture for managing wine recommendations, cellar inventory, and storing new wines with automatic information retrieval.

## Overview

This application uses a coordinated multi-agent system to:
- Provide personalized wine recommendations based on meal pairings, colour, origin, and preferences
- Query and manage wine cellar inventory
- Automatically research and store new wines with detailed information

## Architecture

The system uses a hierarchical agent architecture:

### Root Agent
The **root_agent** acts as the main coordinator, orchestrating all workflows:
- Handles wine recommendations by analyzing cellar inventory
- Manages cellar inventory queries
- Delegates wine storage tasks to the specialized StoreWineAgent
- Politely declines non-wine-related requests

### Sub-Agents

#### StoreWineAgent (Sequential Agent)
A two-stage sequential agent that stores new wines:

1. **RetrieveWineInformationAgent**: Uses Google Search to find 2-3 relevant pieces of information about the wine
2. **WriterAgent**: Synthesizes the research into a structured JSON summary with all wine details

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

Start the interactive chat interface:
```bash
make run
# or
python main.py
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
```

Type `exit` or `quit` to stop the application.

### Running Tests

Execute the test suite:
```bash
make test
```

## Project Structure

```
adk_project/
├── main.py                          # Application entry point
├── agents/
│   ├── agent.py                    # Root coordinator agent
│   ├── shared_library/
│   │   ├── tools.py                # Wine retrieval functions
│   │   └── helper.py               # Utility functions and configurations
│   └── sub_agents/
│       └── store_wine.py           # Sequential agent for storing wines
├── agents_tests/
│   ├── integration.evalset.json    # Integration test cases
│   └── test_config.json            # Test configuration
├── tests/
│   └── test_tools.py               # Unit tests
├── pyproject.toml                   # Project dependencies
├── Makefile                         # Build and run commands
└── README.md                        # This file
```

## Technology Stack

- **Google ADK (Agent Development Kit)**: Multi-agent orchestration framework
- **Gemini LLM**: Google's large language model for natural language understanding
- **Google Search Tool**: Automated web research capability
- **pytest**: Testing framework
- **asyncio**: Asynchronous session management

## Configuration

The application uses these key configurations (in `agents/shared_library/helper.py`):
- **LLM Model**: Configurable Gemini model selection
- **Retry Logic**: Automatic retry on API failures
- **Session Management**: In-memory session service for stateful conversations

## Development

### Adding New Wines

Wines can be added through conversation or by modifying the `retrieve_wines()` function in `agents/shared_library/tools.py`.

### Extending Functionality

To add new capabilities:
1. Create new agent in `agents/` or `agents/sub_agents/`
2. Register as a tool in the root agent
3. Update root agent instructions to include new workflow

