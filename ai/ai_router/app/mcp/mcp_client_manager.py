from __future__ import annotations

from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.stdio import (
    stdio_client,
    StdioServerParameters,
)


class ManagedSession:

    def __init__(
        self,
        session,
        stack,
    ):

        self.session = session
        self.stack = stack


class MCPClientManager:

    def __init__(self):

        self._sessions = {}

    async def _create_session(
        self,
        server_name: str,
        command: list[str],
        working_dir: str,
    ):

        stack = AsyncExitStack()

        server_params = (
            StdioServerParameters(
                command=command[0],
                args=command[1:],
                cwd=working_dir,
            )
        )

        read_stream, write_stream = (
            await stack.enter_async_context(
                stdio_client(
                    server_params
                )
            )
        )

        session = (
            await stack.enter_async_context(
                ClientSession(
                    read_stream,
                    write_stream,
                )
            )
        )

        await session.initialize()

        managed = ManagedSession(
            session=session,
            stack=stack,
        )

        self._sessions[
            server_name
        ] = managed

        return managed

    async def get_session(
        self,
        server_name: str,
        command: list[str],
        working_dir: str,
    ):

        managed = (
            self._sessions.get(
                server_name
            )
        )

        if managed:

            try:

                await (
                    managed.session
                    .list_tools()
                )

                return (
                    managed.session
                )

            except Exception:

                try:

                    await (
                        managed.stack
                        .aclose()
                    )

                except Exception:
                    pass

                self._sessions.pop(
                    server_name,
                    None,
                )

        managed = (
            await self._create_session(
                server_name,
                command,
                working_dir,
            )
        )

        return managed.session

    async def shutdown(self):

        sessions = list(
            self._sessions.values()
        )

        self._sessions.clear()

        for managed in sessions:

            try:

                await (
                    managed.stack
                    .aclose()
                )

            except Exception:
                pass


mcp_client_manager = (
    MCPClientManager()
)