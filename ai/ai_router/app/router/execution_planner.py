from __future__ import annotations

from app.mcp.mcp_executor import (
    mcp_executor,
)

from app.router.tool_argument_extractor import (
    tool_argument_extractor,
)


class ExecutionPlanner:

    def create_plan(
        self,
        route_result: dict,
    ) -> dict:

        arguments = (
            tool_argument_extractor
            .extract(
                route_result.get(
                    "query",
                    "",
                )
            )
        )

        route_type = (
            route_result.get(
                "type"
            )
        )

        # ==================================================
        # Cross Repository Plugin Route
        # ==================================================

        if (
            route_type
            == "cross_repo_plugin"
        ):

            executions = []

            for skill in (
                route_result[
                    "skills"
                ]
            ):

                execution = (
                    mcp_executor
                    .create_execution_plan(
                        skill[
                            "server"
                        ],
                        skill[
                            "mcp_tool"
                        ],
                    )
                )

                executions.append(
                    {

                        "repository":
                            skill[
                                "repository"
                            ],

                        "skill":
                            skill[
                                "skill"
                            ],

                        "tool":
                            skill[
                                "tool"
                            ],

                        "server":
                            skill[
                                "server"
                            ],

                        "mcp_tool":
                            skill[
                                "mcp_tool"
                            ],

                        "execution":
                            execution,
                    }
                )

            return {

                "type":
                    "cross_repo_mcp",

                "repositories":
                    route_result[
                        "repositories"
                    ],

                "arguments":
                    arguments,

                "executions":
                    executions,
            }

        # ==================================================
        # Multi Skill Plugin Route
        # ==================================================

        if (
            route_type
            == "multi_plugin"
        ):

            executions = []

            for skill in (
                route_result[
                    "skills"
                ]
            ):

                execution = (
                    mcp_executor
                    .create_execution_plan(
                        skill[
                            "server"
                        ],
                        skill[
                            "mcp_tool"
                        ],
                    )
                )

                executions.append(
                    {

                        "repository":
                            skill.get(
                                "repository"
                            ),

                        "skill":
                            skill[
                                "skill"
                            ],

                        "tool":
                            skill[
                                "tool"
                            ],

                        "server":
                            skill[
                                "server"
                            ],

                        "mcp_tool":
                            skill[
                                "mcp_tool"
                            ],

                        "execution":
                            execution,
                    }
                )

            return {

                "type":
                    "multi_mcp",

                "repository":
                    route_result[
                        "repository"
                    ],

                "arguments":
                    arguments,

                "executions":
                    executions,
            }

        # ==================================================
        # Non Plugin Route
        # ==================================================

        if (
            route_type
            != "plugin"
        ):

            return {

                "type":
                    "llm",

                "route":
                    route_result,
            }

        # ==================================================
        # Single Plugin Route
        # ==================================================

        execution = (
            mcp_executor
            .create_execution_plan(
                route_result[
                    "server"
                ],
                route_result[
                    "mcp_tool"
                ],
            )
        )

        return {

            "type":
                "mcp",

            "repository":
                route_result[
                    "repository"
                ],

            "skill":
                route_result[
                    "skill"
                ],

            "server":
                route_result[
                    "server"
                ],

            "tool":
                route_result[
                    "tool"
                ],

            "mcp_tool":
                route_result[
                    "mcp_tool"
                ],

            "arguments":
                arguments,

            "execution":
                execution,
        }


execution_planner = (
    ExecutionPlanner()
)