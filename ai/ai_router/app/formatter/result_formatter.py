from __future__ import annotations

import json


class ResultFormatter:

    def _pretty_content(
        self,
        content: str,
    ) -> str:

        try:

            parsed = json.loads(
                content
            )

            #
            # Feature Trace Result
            #

            if (
                isinstance(
                    parsed,
                    dict,
                )
                and "feature"
                in parsed
            ):

                output = []

                output.append(
                    f"Feature: {parsed.get('feature')}"
                )

                output.append(
                    ""
                )

                output.append(
                    f"Found: {'Yes' if parsed.get('found') else 'No'}"
                )

                locations = (
                    parsed.get(
                        "locations",
                        []
                    )
                )

                if locations:

                    output.append(
                        ""
                    )

                    output.append(
                        "Locations:"
                    )

                    for location in (
                        locations
                    ):

                        output.append(
                            f"- {location}"
                        )

                return "\n".join(
                    output
                )

            #
            # Normal JSON
            #

            return json.dumps(
                parsed,
                indent=2,
            )

        except Exception:

            return content

    def format(
        self,
        result: dict,
    ) -> str:

        if not result:

            return (
                "No result returned."
            )

        # ----------------------------------
        # Multi Result
        # ----------------------------------

        if "results" in result:

            sections = []

            for item in (
                result["results"]
            ):

                repository = (
                    item.get(
                        "repository",
                        ""
                    )
                )

                tool_name = (
                    item.get(
                        "tool",
                        "unknown"
                    )
                    .replace(
                        "_",
                        " "
                    )
                    .title()
                )

                if repository:

                    repo_header = (
                        repository
                        .replace(
                            "hub_",
                            ""
                        )
                        .upper()
                    )

                    sections.append(
                        f"\n[{repo_header}]"
                    )

                sections.append(
                    tool_name
                )

                sections.append(
                    "-" * len(
                        tool_name
                    )
                )

                for content in (
                    item.get(
                        "content",
                        []
                    )
                ):

                    sections.append(
                        self._pretty_content(
                            content
                        )
                    )

            return "\n".join(
                sections
            )

        # ----------------------------------
        # Single Result
        # ----------------------------------

        if "content" in result:

            sections = []

            tool_name = (
                result.get(
                    "tool",
                    "unknown"
                )
                .replace(
                    "_",
                    " "
                )
                .title()
            )

            sections.append(
                tool_name
            )

            sections.append(
                "-" * len(
                    tool_name
                )
            )

            for content in (
                result.get(
                    "content",
                    []
                )
            ):

                sections.append(
                    self._pretty_content(
                        content
                    )
                )

            return "\n".join(
                sections
            )

        return str(
            result
        )


result_formatter = (
    ResultFormatter()
)