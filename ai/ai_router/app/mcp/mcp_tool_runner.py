from __future__ import annotations

from app.mcp.mcp_invoker import (
    mcp_invoker,
)


class MCPToolRunner:

    async def _execute_single(
        self,
        execution_plan: dict,
        arguments: dict | None = None,
    ) -> dict:

        merged_arguments = {}

        merged_arguments.update(
            execution_plan.get(
                "arguments",
                {}
            )
        )

        if arguments:

            merged_arguments.update(
                arguments
            )

        DEBUG = False

        if DEBUG:

            print(
                "RUNNER ARGUMENTS",
                merged_arguments
            )

        result = await (

            mcp_invoker.invoke(
                execution_plan,
                merged_arguments,
            )

        )

        output = []

        if hasattr(
            result,
            "content",
        ):

            for item in result.content:

                text = getattr(
                    item,
                    "text",
                    None,
                )

                if text:

                    output.append(
                        text
                    )

        return {

            "success": (
                not getattr(
                    result,
                    "isError",
                    False,
                )
            ),

            "repository":
                execution_plan[
                    "repository"
                ],

            "server":
                execution_plan[
                    "server"
                ],

            "tool":
                execution_plan[
                    "mcp_tool"
                ],

            "content":
                output,
        }

    async def run(
        self,
        execution_plan: dict,
        arguments: dict | None = None,
    ) -> dict:

        plan_type = (
            execution_plan.get(
                "type"
            )
        )

        # ----------------------------------
        # Cross Repository MCP Execution
        # ----------------------------------

        if (
            plan_type
            == "cross_repo_mcp"
        ):

            results = []

            merged_arguments = (
                execution_plan.get(
                    "arguments",
                    {}
                )
            )

            if arguments:

                merged_arguments.update(
                    arguments
                )

            for execution in (
                execution_plan[
                    "executions"
                ]
            ):

                single_plan = {

                    "type":
                        "mcp",

                    "repository":
                        execution[
                            "repository"
                        ],

                    "skill":
                        execution[
                            "skill"
                        ],

                    "server":
                        execution[
                            "server"
                        ],

                    "tool":
                        execution[
                            "tool"
                        ],

                    "mcp_tool":
                        execution[
                            "mcp_tool"
                        ],

                    "execution":
                        execution[
                            "execution"
                        ],
                }

                result = await (
                    self._execute_single(
                        single_plan,
                        merged_arguments,
                    )
                )

                results.append(
                    result
                )

            return {

                "success": True,

                "repositories":
                    execution_plan[
                        "repositories"
                    ],

                "results":
                    results,
            }

        # ----------------------------------
        # Multi MCP Execution
        # ----------------------------------

        if (
            plan_type
            == "multi_mcp"
        ):

            results = []

            merged_arguments = (
                execution_plan.get(
                    "arguments",
                    {}
                )
            )

            if arguments:

                merged_arguments.update(
                    arguments
                )

            for execution in (
                execution_plan[
                    "executions"
                ]
            ):

                single_plan = {

                    "type":
                        "mcp",

                    "repository":
                        execution_plan[
                            "repository"
                        ],

                    "skill":
                        execution[
                            "skill"
                        ],

                    "server":
                        execution[
                            "server"
                        ],

                    "tool":
                        execution[
                            "tool"
                        ],

                    "mcp_tool":
                        execution[
                            "mcp_tool"
                        ],

                    "execution":
                        execution[
                            "execution"
                        ],
                }

                result = await (
                    self._execute_single(
                        single_plan,
                        merged_arguments,
                    )
                )

                results.append(
                    result
                )

            return {

                "success": True,

                "repository":
                    execution_plan[
                        "repository"
                    ],

                "results":
                    results,
            }

        # ----------------------------------
        # Single MCP Execution
        # ----------------------------------

        return await (
            self._execute_single(
                execution_plan,
                arguments,
            )
        )


mcp_tool_runner = (
    MCPToolRunner()
)