from __future__ import annotations

from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel

from app.plugin.plugin_discovery import (
    discover_all,
)


class AgentDefinition(BaseModel):

    repository: str

    agent_id: str

    name: str

    description: str = ""

    skills: List[str] = []


class AgentRegistry:

    def __init__(self):

        self._agents: Dict[
            str,
            AgentDefinition
        ] = {}

        self._repository_index: Dict[
            str,
            Dict[str, AgentDefinition]
        ] = {}

    def build(self):

        self._agents.clear()

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

            agents = getattr(
                repo,
                "agents",
                []
            )

            for agent in agents:

                definition = AgentDefinition(
                    repository=repository,
                    agent_id=agent.name,
                    name=agent.name,
                    description="",
                    skills=[]
                )

                key = (
                    f"{repository}:"
                    f"{agent.name}"
                )

                self._agents[
                    key
                ] = definition

                self._repository_index[
                    repository
                ][
                    agent.name
                ] = definition

    def get(
        self,
        repository: str,
        agent_id: str
    ) -> Optional[AgentDefinition]:

        return (
            self._repository_index
            .get(repository, {})
            .get(agent_id)
        )

    def get_repository_agents(
        self,
        repository: str
    ) -> List[AgentDefinition]:

        return list(
            self._repository_index
            .get(repository, {})
            .values()
        )

    def get_all(
        self
    ) -> List[AgentDefinition]:

        return list(
            self._agents.values()
        )

    def repositories(
        self
    ) -> List[str]:

        return list(
            self._repository_index.keys()
        )


agent_registry = AgentRegistry()