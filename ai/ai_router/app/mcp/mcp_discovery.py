from __future__ import annotations

from pathlib import Path

from .mcp_models import (
    MCPDiscoveryResult,
    MCPServerInfo,
    MCPToolInfo,
)

from ..plugin.plugin_discovery import (
    discover_all,
)


def discover_tool_files(
    tools_path: Path,
) -> list[MCPToolInfo]:

    tools: list[MCPToolInfo] = []

    if not tools_path.exists():
        return tools

    for item in sorted(tools_path.iterdir()):

        if item.name.startswith("."):
            continue

        if item.is_file() and item.suffix in {
            ".ts",
            ".js",
        }:

            tools.append(
                MCPToolInfo(
                    name=item.stem,
                    path=item,
                )
            )

    return tools


def discover_mcp_server(
    repository_inventory,
) -> MCPServerInfo | None:

    manifest = repository_inventory.manifest

    server_name = (
        manifest.mcp_server.name
    )

    mcp_root = (
        repository_inventory.root_path
        / server_name
    )

    if not mcp_root.exists():
        return None

    tools_path = (
        mcp_root
        / "src"
        / "tools"
    )

    tools = discover_tool_files(
        tools_path
    )

    return MCPServerInfo(
        repository=repository_inventory.repository,
        server_name=server_name,
        root_path=mcp_root,
        tools=tools,
    )


def discover_all_mcp_servers(
) -> MCPDiscoveryResult:

    plugin_inventory = discover_all()

    result = MCPDiscoveryResult()

    for repository in (
        plugin_inventory.repositories
    ):

        server = discover_mcp_server(
            repository
        )

        if server:
            result.servers.append(
                server
            )

    return result