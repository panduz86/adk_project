from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

mcp_review_wine_server = McpToolset(
    connection_params=StreamableHTTPServerParams(
        url="http://localhost:8002/mcp"
    ),
)

