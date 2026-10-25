"""
Optional project capability: Model Context Protocol (MCP).

Implement this module only if this capability is relevant to your application's
user problem. Remove the file if the capability is not used.

Conceptual Overview:
-------------------
Model Context Protocol (MCP) is an open standard protocol that connects AI applications
to external data sources, tools, and services in a standardized format.

Key concepts when integrating MCP:
1. MCP Architecture: Client-Server architecture separating the host application (client)
   from data providers / tools (MCP servers).
2. Protocol Capabilities: Resources (reading files/data), Tools (executing actions),
   and Prompts (reusable prompt templates).
3. Standardized Connectivity: Interacting with external systems via standard MCP server endpoints.

Note:
-----
Do not implement MCP unless your project specifically requires integrating standard MCP servers
or building a custom MCP tool server.
"""

# Implement custom MCP client/server integration below if selected.

from typing import Literal

from mcp.server import MCPServer

from src.capabilities.tools import lookup_product_deadline
from src.schemas.responses import ProductObservation

product_server = MCPServer("Fictional Product Information")


@product_server.tool(name="lookup_product_deadline")
def mcp_lookup_product_deadline(
    product_id: str, stage: Literal["manufacturing", "testing", "shipping"]
) -> ProductObservation:
    """Read the deadline for the manufacturing, testing or shipping stage of a product."""
    return lookup_product_deadline(product_id, stage)