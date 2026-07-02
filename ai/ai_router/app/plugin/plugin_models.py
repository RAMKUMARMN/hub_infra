from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field


class MCPServerInfo(BaseModel):
    name: str
    enabled: bool = True
    auto_start: bool = True
    is_controller: bool = False


class OrchestratorRegistration(BaseModel):
    enabled: bool = True
    managed_by: str = "hub_infra"
    auto_discover: bool = True
    allow_remote_reload: bool = True
    allow_remote_validation: bool = True


class RepositoryManifest(BaseModel):
    repository: str
    repository_role: str

    name: str
    version: str

    repository_priority: int

    mcp_server: MCPServerInfo

    orchestrator_registration: OrchestratorRegistration


class PluginItem(BaseModel):
    name: str
    category: str
    path: Path


class RepositoryInventory(BaseModel):
    repository: str
    repository_role: str

    root_path: Path

    manifest: RepositoryManifest

    agents: List[PluginItem] = Field(default_factory=list)

    skills: List[PluginItem] = Field(default_factory=list)

    rules: List[PluginItem] = Field(default_factory=list)

    hooks: List[PluginItem] = Field(default_factory=list)


class DiscoveryResult(BaseModel):
    repositories: List[RepositoryInventory] = Field(
        default_factory=list
    )

    def total_agents(self) -> int:
        return sum(len(repo.agents) for repo in self.repositories)

    def total_skills(self) -> int:
        return sum(len(repo.skills) for repo in self.repositories)

    def total_rules(self) -> int:
        return sum(len(repo.rules) for repo in self.repositories)

    def total_hooks(self) -> int:
        return sum(len(repo.hooks) for repo in self.repositories)