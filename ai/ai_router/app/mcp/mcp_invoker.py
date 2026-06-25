from __future__ import annotations

from app.mcp.mcp_client_manager import (
    mcp_client_manager,
)


class MCPInvoker:

    async def invoke(
        self,
        execution_plan: dict,
        arguments: dict | None = None,
    ):

        arguments = (
            arguments or {}
        )

        execution = (
            execution_plan[
                "execution"
            ]
        )

        session = (
            await mcp_client_manager
            .get_session(
                server_name=
                execution_plan[
                    "server"
                ],

                command=
                execution[
                    "command"
                ],

                working_dir=
                execution[
                    "root_path"
                ],
            )
        )

        result = (
            await session.call_tool(
                execution_plan[
                    "mcp_tool"
                ],
                arguments,
            )
        )

        return result


mcp_invoker = MCPInvoker()