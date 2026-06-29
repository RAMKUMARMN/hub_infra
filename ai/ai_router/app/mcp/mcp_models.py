from pathlib import Path
from typing import List

from pydantic import BaseModel, Field


class MCPToolInfo(BaseModel):
    name: str
    path: Path


class MCPServerInfo(BaseModel):
    repository: str
    server_name: str
    root_path: Path

    tools: List[MCPToolInfo] = Field(
        default_factory=list
    )


class MCPDiscoveryResult(BaseModel):
    servers: List[MCPServerInfo] = Field(
        default_factory=list
    )

    def total_servers(self) -> int:
        return len(self.servers)

    def total_tools(self) -> int:
        return sum(
            len(server.tools)
            for server in self.servers
        )