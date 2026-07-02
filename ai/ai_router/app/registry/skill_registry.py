from __future__ import annotations

import json
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel

from ..plugin.plugin_discovery import discover_all


class SkillDefinition(BaseModel):
    repository: str

    skill_id: str
    name: str

    mcp_server: str
    tool: str

    enabled: bool = True

    path: Path


class SkillRegistry:

    def __init__(self) -> None:

        self._skills: Dict[
            str,
            SkillDefinition
        ] = {}

        self._repo_skill_index: Dict[
            str,
            Dict[str, SkillDefinition]
        ] = {}

    def build(self) -> None:

        discovery = discover_all()

        self._skills.clear()
        self._repo_skill_index.clear()

        for repo in discovery.repositories:

            repo_name = repo.repository

            if repo_name not in self._repo_skill_index:
                self._repo_skill_index[
                    repo_name
                ] = {}

            for skill in repo.skills:

                manifest_path = (
                    skill.path
                    / ".plugin"
                    / "plugin.json"
                )

                if not manifest_path.exists():
                    continue

                try:

                    with open(
                        manifest_path,
                        "r",
                        encoding="utf-8"
                    ) as file:

                        raw = json.load(file)

                    definition = SkillDefinition(
                        repository=repo_name,
                        skill_id=raw["id"],
                        name=raw.get(
                            "name",
                            raw["id"]
                        ),
                        mcp_server=raw.get(
                            "mcp_server",
                            ""
                        ),
                        tool=raw.get(
                            "tool",
                            ""
                        ),
                        enabled=raw.get(
                            "enabled",
                            True
                        ),
                        path=skill.path
                    )

                    # GLOBAL UNIQUE KEY
                    unique_key = (
                        f"{repo_name}:"
                        f"{definition.skill_id}"
                    )

                    self._skills[
                        unique_key
                    ] = definition

                    self._repo_skill_index[
                        repo_name
                    ][
                        definition.skill_id
                    ] = definition

                except Exception as ex:
                    print(
                        "[SkillRegistry] "
                        f"Failed loading "
                        f"{manifest_path}: {ex}"
                    )

    def get(
        self,
        repository: str,
        skill_id: str
    ) -> Optional[SkillDefinition]:

        return (
            self._repo_skill_index
            .get(repository, {})
            .get(skill_id)
        )

    def get_all(
        self
    ) -> List[SkillDefinition]:

        return list(
            self._skills.values()
        )

    def get_repository_skills(
        self,
        repository: str
    ) -> List[SkillDefinition]:

        return list(
            self._repo_skill_index
            .get(repository, {})
            .values()
        )

    def repositories(
        self
    ) -> List[str]:

        return list(
            self._repo_skill_index.keys()
        )


skill_registry = SkillRegistry()