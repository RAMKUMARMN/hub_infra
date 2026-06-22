from __future__ import annotations

from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel

from app.mcp.mcp_discovery import (
    discover_all_mcp_servers,
)


class MCPServerDefinition(
    BaseModel
):

    repository: str

    server_name: str

    root_path: str

    tools: List[str]


class MCPRegistry:

    def __init__(self):

        self._servers: Dict[
            str,
            MCPServerDefinition
        ] = {}

    def build(self):

        self._servers.clear()

        result = (
            discover_all_mcp_servers()
        )

        for server in (
            result.servers
        ):

            self._servers[
                server.server_name
            ] = (
                MCPServerDefinition(
                    repository=
                        server.repository,

                    server_name=
                        server.server_name,

                    root_path=str(
                        server.root_path
                    ),

                    tools=[
                        tool.name
                        for tool
                        in server.tools
                    ],
                )
            )

    def get(
        self,
        server_name: str,
    ) -> Optional[
        MCPServerDefinition
    ]:

        return (
            self._servers.get(
                server_name
            )
        )

    def get_all(
        self,
    ) -> List[
        MCPServerDefinition
    ]:

        return list(
            self._servers.values()
        )


mcp_registry = MCPRegistry()