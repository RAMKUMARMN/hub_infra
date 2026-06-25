from __future__ import annotations

from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel

from app.plugin.plugin_discovery import (
    discover_all,
)


class RuleDefinition(BaseModel):

    repository: str

    rule_id: str

    name: str

    description: str = ""


class RuleRegistry:

    def __init__(self):

        self._rules: Dict[
            str,
            RuleDefinition
        ] = {}

        self._repository_index: Dict[
            str,
            Dict[str, RuleDefinition]
        ] = {}

    def build(self):

        self._rules.clear()

        self._repository_index.clear()

        inventory = discover_all()

        for repo in inventory.repositories:

            repository = repo.repository

            if (
                repository
                not in self._repository_index
            ):
                self._repository_index[
                    repository
                ] = {}

            rules = getattr(
                repo,
                "rules",
                []
            )

            for rule in rules:

                definition = RuleDefinition(
                    repository=repository,
                    rule_id=rule.name,
                    name=rule.name,
                    description=""
                )

                key = (
                    f"{repository}:"
                    f"{rule.name}"
                )

                self._rules[
                    key
                ] = definition

                self._repository_index[
                    repository
                ][
                    rule.name
                ] = definition

    def get(
        self,
        repository: str,
        rule_id: str
    ) -> Optional[RuleDefinition]:

        return (
            self._repository_index
            .get(repository, {})
            .get(rule_id)
        )

    def get_repository_rules(
        self,
        repository: str
    ) -> List[RuleDefinition]:

        return list(
            self._repository_index
            .get(repository, {})
            .values()
        )

    def get_all(
        self
    ) -> List[RuleDefinition]:

        return list(
            self._rules.values()
        )


rule_registry = RuleRegistry()