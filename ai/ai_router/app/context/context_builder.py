from __future__ import annotations

import json


class ContextBuilder:

    def build(
        self,
        mcp_result: dict,
    ) -> str:

        if not mcp_result:

            return ""

        sections = []

        #
        # Multi Result
        #

        if "results" in mcp_result:

            for item in mcp_result["results"]:

                repository = item.get(
                    "repository",
                    ""
                )

                tool = item.get(
                    "tool",
                    ""
                )

                sections.append(
                    f"Repository: {repository}"
                )

                sections.append(
                    f"Tool: {tool}"
                )

                for content in item.get(
                    "content",
                    []
                ):

                    try:

                        parsed = json.loads(
                            content
                        )

                        sections.append(
                            json.dumps(
                                parsed,
                                indent=2,
                            )
                        )

                    except Exception:

                        sections.append(
                            content
                        )

                sections.append("")

            return "\n".join(
                sections
            )

        #
        # Single Result
        #

        repository = mcp_result.get(
            "repository",
            ""
        )

        tool = mcp_result.get(
            "tool",
            ""
        )

        sections.append(
            f"Repository: {repository}"
        )

        sections.append(
            f"Tool: {tool}"
        )

        for content in mcp_result.get(
            "content",
            []
        ):

            try:

                parsed = json.loads(
                    content
                )

                sections.append(
                    json.dumps(
                        parsed,
                        indent=2,
                    )
                )

            except Exception:

                sections.append(
                    content
                )

        return "\n".join(
            sections
        )


context_builder = (
    ContextBuilder()
)