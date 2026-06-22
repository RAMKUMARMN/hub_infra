from __future__ import annotations

from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel

from app.mcp.mcp_discovery import (
    discover_all_mcp_servers,
)


class ToolDefinition(BaseModel):

    repository: str

    server: str

    name: str

    mcp_tool_name: str

    path: str = ""

    description: str = ""


class ToolRegistry:

    def __init__(self):

        self._tools: Dict[
            str,
            ToolDefinition
        ] = {}

        self._server_index: Dict[
            str,
            Dict[str, ToolDefinition]
        ] = {}

        self._repository_index: Dict[
            str,
            Dict[str, ToolDefinition]
        ] = {}

    def _to_mcp_tool_name(
        self,
        tool_name: str,
    ) -> str:

        result = []

        for char in tool_name:

            if char.isupper():

                result.append("_")
                result.append(
                    char.lower()
                )

            else:

                result.append(char)

        return "".join(result)
    def to_mcp_tool_name(
        self,
        tool_name: str,
    ) -> str:

        return self._to_mcp_tool_name(
            tool_name
        )
    def build(self):

        self._tools.clear()

        self._server_index.clear()

        self._repository_index.clear()

        discovery_result = (
            discover_all_mcp_servers()
        )

        servers = discovery_result.servers

        for server in servers:

            repository = (
                server.repository
            )

            server_name = (
                server.server_name
            )

            if (
                server_name
                not in self._server_index
            ):

                self._server_index[
                    server_name
                ] = {}

            if (
                repository
                not in self._repository_index
            ):

                self._repository_index[
                    repository
                ] = {}

            for tool in server.tools:

                definition = ToolDefinition(
                    repository=repository,
                    server=server_name,
                    name=tool.name,
                    mcp_tool_name=(
                        self._to_mcp_tool_name(
                            tool.name
                        )
                    ),
                    path=str(
                        tool.path
                    ),
                    description=""
                )

                unique_key = (
                    f"{server_name}:"
                    f"{tool.name}"
                )

                self._tools[
                    unique_key
                ] = definition

                self._server_index[
                    server_name
                ][
                    tool.name
                ] = definition

                self._repository_index[
                    repository
                ][
                    tool.name
                ] = definition

    def get(
        self,
        server: str,
        tool_name: str,
    ) -> Optional[ToolDefinition]:

        return (
            self._server_index
            .get(server, {})
            .get(tool_name)
        )

    def get_tool(
        self,
        server: str,
        tool_name: str,
    ) -> Optional[ToolDefinition]:

        return self.get(
            server,
            tool_name,
        )

    def get_server_tools(
        self,
        server: str,
    ) -> List[ToolDefinition]:

        return list(
            self._server_index
            .get(server, {})
            .values()
        )

    def get_repository_tools(
        self,
        repository: str,
    ) -> List[ToolDefinition]:

        return list(
            self._repository_index
            .get(repository, {})
            .values()
        )

    def get_all(
        self,
    ) -> List[ToolDefinition]:

        return list(
            self._tools.values()
        )

    def servers(
        self,
    ) -> List[str]:

        return list(
            self._server_index.keys()
        )

    def repositories(
        self,
    ) -> List[str]:

        return list(
            self._repository_index.keys()
        )

    def has_tool(
        self,
        server: str,
        tool_name: str,
    ) -> bool:

        return (
            self.get(
                server,
                tool_name,
            )
            is not None
        )


tool_registry = ToolRegistry()