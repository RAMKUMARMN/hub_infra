from __future__ import annotations

from pathlib import Path

from app.mcp.mcp_registry import (
    mcp_registry,
)


class MCPExecutor:

    def __init__(self):

        self._ready = False

    def build(self):

        if self._ready:
            return

        mcp_registry.build()

        self._ready = True

    def get_server(
        self,
        server_name: str,
    ):

        self.build()

        return (
            mcp_registry.get(
                server_name
            )
        )

    def create_execution_plan(
        self,
        server_name: str,
        mcp_tool: str,
    ):

        server = (
            self.get_server(
                server_name
            )
        )

        if not server:

            raise ValueError(
                f"Unknown MCP server: "
                f"{server_name}"
            )

        root_path = Path(
            server.root_path
        )

        return {

            "repository":
                server.repository,

            "server":
                server.server_name,

            "mcp_tool":
                mcp_tool,

            "root_path":
                str(root_path),

            "package_json":
                str(
                    root_path
                    / "package.json"
                ),

            "server_ts":
                str(
                    root_path
                    / "src"
                    / "server.ts"
                ),

            "command": [
                "node",
                "dist/server.js",
            ],
            "dist_server":
                str(
                    root_path
                    / "dist"
                    / "server.js"
                ),
            }


mcp_executor = MCPExecutor()