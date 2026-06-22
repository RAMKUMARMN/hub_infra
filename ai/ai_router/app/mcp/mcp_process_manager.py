from __future__ import annotations

import subprocess

from app.mcp.mcp_executor import (
    mcp_executor,
)


class MCPProcessManager:

    def __init__(self):

        self._processes = {}

    def is_running(
        self,
        server_name: str,
    ) -> bool:

        process = (
            self._processes.get(
                server_name
            )
        )

        return (
            process is not None
            and process.poll()
            is None
        )

    def start_server(
        self,
        server_name: str,
    ):

        if self.is_running(
            server_name
        ):

            return self._processes[
                server_name
            ]

        plan = (
            mcp_executor
            .create_execution_plan(
                server_name,
                "",
            )
        )

        process = (
            subprocess.Popen(
                plan["command"],
                cwd=plan[
                    "root_path"
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        )

        self._processes[
            server_name
        ] = process

        return process

    def stop_server(
        self,
        server_name: str,
    ):

        process = (
            self._processes.get(
                server_name
            )
        )

        if not process:

            return

        process.terminate()

        del self._processes[
            server_name
        ]

    def stop_all(self):

        for server_name in list(
            self._processes.keys()
        ):

            self.stop_server(
                server_name
            )


mcp_process_manager = (
    MCPProcessManager()
)