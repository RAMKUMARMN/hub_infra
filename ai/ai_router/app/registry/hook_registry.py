from __future__ import annotations

from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel

from app.plugin.plugin_discovery import (
    discover_all,
)


class HookDefinition(BaseModel):

    repository: str

    hook_id: str

    name: str

    description: str = ""


class HookRegistry:

    def __init__(self):

        self._hooks: Dict[
            str,
            HookDefinition
        ] = {}

        self._repository_index: Dict[
            str,
            Dict[str, HookDefinition]
        ] = {}

    def build(self):

        self._hooks.clear()

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

            hooks = getattr(
                repo,
                "hooks",
                []
            )

            for hook in hooks:

                definition = HookDefinition(
                    repository=repository,
                    hook_id=hook.name,
                    name=hook.name,
                    description=""
                )

                key = (
                    f"{repository}:"
                    f"{hook.name}"
                )

                self._hooks[
                    key
                ] = definition

                self._repository_index[
                    repository
                ][
                    hook.name
                ] = definition

    def get(
        self,
        repository: str,
        hook_id: str
    ) -> Optional[HookDefinition]:

        return (
            self._repository_index
            .get(repository, {})
            .get(hook_id)
        )

    def get_repository_hooks(
        self,
        repository: str
    ) -> List[HookDefinition]:

        return list(
            self._repository_index
            .get(repository, {})
            .values()
        )

    def get_all(
        self
    ) -> List[HookDefinition]:

        return list(
            self._hooks.values()
        )


hook_registry = HookRegistry()