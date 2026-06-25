from __future__ import annotations

from typing import Dict
from typing import List

from app.registry.skill_registry import (
    skill_registry,
)

from app.registry.tool_registry import (
    tool_registry,
)


def validate_skill_mappings():

    skill_registry.build()

    tool_registry.build()

    valid_skills = []

    invalid_skills = []

    missing_servers = []

    missing_tools = []

    known_servers = set(
        tool_registry.servers()
    )

    for skill in skill_registry.get_all():

        if not skill.mcp_server:

            invalid_skills.append(skill)

            continue

        if not skill.tool:

            invalid_skills.append(skill)

            continue

        if (
            skill.mcp_server
            not in known_servers
        ):

            invalid_skills.append(skill)

            missing_servers.append(
                {
                    "repository":
                        skill.repository,
                    "skill":
                        skill.skill_id,
                    "server":
                        skill.mcp_server,
                }
            )

            continue

        tool_exists = (
            tool_registry.has_tool(
                skill.mcp_server,
                skill.tool
            )
        )

        if not tool_exists:

            invalid_skills.append(skill)

            missing_tools.append(
                {
                    "repository":
                        skill.repository,
                    "skill":
                        skill.skill_id,
                    "server":
                        skill.mcp_server,
                    "tool":
                        skill.tool,
                }
            )

            continue

        valid_skills.append(skill)

    return {
        "summary": {
            "valid_skills":
                len(valid_skills),
            "invalid_skills":
                len(invalid_skills),
            "missing_servers":
                len(missing_servers),
            "missing_tools":
                len(missing_tools),
        },
        "valid_skills":
            valid_skills,
        "invalid_skills":
            invalid_skills,
        "missing_servers":
            missing_servers,
        "missing_tools":
            missing_tools,
    }


if __name__ == "__main__":

    report = (
        validate_skill_mappings()
    )

    print(
        "\n=== SUMMARY ===\n"
    )

    for key, value in (
        report["summary"]
        .items()
    ):

        print(
            f"{key}: {value}"
        )

    print(
        "\n=== MISSING SERVERS ===\n"
    )

    for item in (
        report["missing_servers"]
    ):

        print(
            f"[{item['repository']}] "
            f"{item['skill']}"
            f" -> "
            f"{item['server']}"
        )

    print(
        "\n=== MISSING TOOLS ===\n"
    )

    for item in (
        report["missing_tools"]
    ):

        print(
            f"[{item['repository']}] "
            f"{item['skill']}"
            f" -> "
            f"{item['tool']}"
            f" @ "
            f"{item['server']}"
        )