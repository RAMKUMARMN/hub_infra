from __future__ import annotations

from collections import defaultdict

from app.registry.skill_registry import (
    skill_registry,
)

from app.mcp.mcp_discovery import (
    discover_all_mcp_servers,
)


def run_orphan_audit():

    skill_registry.build()

    mcp_servers = discover_all_mcp_servers()

    mapped_skills = []
    unmapped_skills = []

    mapped_tools = set()

    orphan_tools = []

    tool_usage = defaultdict(list)

    for skill in skill_registry.get_all():

        if skill.tool:

            mapped_skills.append(skill)

            mapped_tools.add(
                (
                    skill.mcp_server,
                    skill.tool,
                )
            )

            tool_usage[
                (
                    skill.mcp_server,
                    skill.tool,
                )
            ].append(skill)

        else:

            unmapped_skills.append(skill)

    for server in mcp_servers:

        tools = getattr(
            server,
            "tools",
            []
        )

        for tool in tools:

            key = (
                server.name,
                tool.name,
            )

            if key not in mapped_tools:

                orphan_tools.append(
                    {
                        "server": server.name,
                        "tool": tool.name,
                    }
                )

    duplicate_tool_usage = {}

    for key, skills in tool_usage.items():

        if len(skills) > 1:

            duplicate_tool_usage[key] = skills

    summary = {
        "mapped_skill_count": len(
            mapped_skills
        ),
        "unmapped_skill_count": len(
            unmapped_skills
        ),
        "orphan_tool_count": len(
            orphan_tools
        ),
        "duplicate_tool_count": len(
            duplicate_tool_usage
        ),
    }

    return {
        "summary": summary,
        "mapped_skills": mapped_skills,
        "unmapped_skills": unmapped_skills,
        "orphan_tools": orphan_tools,
        "duplicate_tool_usage":
            duplicate_tool_usage,
    }


if __name__ == "__main__":

    report = run_orphan_audit()

    print("\n=== SUMMARY ===\n")

    for key, value in (
        report["summary"]
        .items()
    ):

        print(
            f"{key}: {value}"
        )

    print(
        "\n=== MAPPED SKILLS ===\n"
    )

    for skill in (
        report["mapped_skills"]
    ):

        print(
            f"[{skill.repository}] "
            f"{skill.skill_id}"
            f" -> "
            f"{skill.tool}"
            f" @ "
            f"{skill.mcp_server}"
        )

    print(
        "\n=== UNMAPPED SKILLS ===\n"
    )

    for skill in (
        report["unmapped_skills"]
    ):

        print(
            f"[{skill.repository}] "
            f"{skill.skill_id}"
        )

    print(
        "\n=== ORPHAN TOOLS ===\n"
    )

    for tool in (
        report["orphan_tools"]
    ):

        print(
            f"{tool['server']} "
            f":: "
            f"{tool['tool']}"
        )

    print(
        "\n=== DUPLICATE TOOL USAGE ===\n"
    )

    for key, skills in (
        report[
            "duplicate_tool_usage"
        ].items()
    ):

        server, tool = key

        print(
            f"{server}"
            f" :: "
            f"{tool}"
        )

        for skill in skills:

            print(
                f"   - "
                f"[{skill.repository}] "
                f"{skill.skill_id}"
            )