from __future__ import annotations

import json
from pathlib import Path
from typing import List

from .plugin_models import (
    DiscoveryResult,
    MCPServerInfo,
    OrchestratorRegistration,
    PluginItem,
    RepositoryInventory,
    RepositoryManifest,
)


SMART_HUB_REPOSITORIES = {
    "hub_backend",
    "hub_infra",
    "hub_notify",
    "hub_frontend",
    "hub_mobile",
    "hub_android",
    "hub_ios",
}


def find_workspace_root() -> Path:
    """
    Dynamically locate cixio_hub workspace.

    Never hardcode paths.
    Works across laptops and developers.
    """

    current = Path(__file__).resolve()

    while current.parent != current:
        if current.name == "hub_infra":
            return current.parent
        current = current.parent

    raise RuntimeError(
        "Unable to locate SmartHub workspace root."
    )


def discover_repositories() -> List[Path]:
    workspace_root = find_workspace_root()

    repositories = []

    for child in workspace_root.iterdir():
        if (
            child.is_dir()
            and child.name in SMART_HUB_REPOSITORIES
        ):
            repositories.append(child)

    return sorted(repositories)


def load_manifest(
    repository_root: Path,
) -> RepositoryManifest | None:

    manifest_path = (
        repository_root
        / "plugin"
        / ".plugin"
        / "plugin.json"
    )

    if not manifest_path.exists():
        return None

    with open(manifest_path, "r", encoding="utf-8") as file:
        raw = json.load(file)

    return RepositoryManifest(
        repository=raw["repository"],
        repository_role=raw["repository_role"],
        name=raw["name"],
        version=raw["version"],
        repository_priority=raw["repository_priority"],
        mcp_server=MCPServerInfo(**raw["mcp_server"]),
        orchestrator_registration=OrchestratorRegistration(
            **raw["orchestrator_registration"]
        ),
    )


def discover_plugin_items(
    repository_root: Path,
    category: str,
) -> List[PluginItem]:

    plugin_dir = (
        repository_root
        / "plugin"
        / category
    )

    if not plugin_dir.exists():
        return []

    results: List[PluginItem] = []

    for item in sorted(plugin_dir.iterdir()):
        if item.name.startswith("."):
            continue

        results.append(
            PluginItem(
                name=item.stem,
                category=category,
                path=item,
            )
        )

    return results


def discover_repository(
    repository_root: Path,
) -> RepositoryInventory | None:

    manifest = load_manifest(repository_root)

    if manifest is None:
        return None

    return RepositoryInventory(
        repository=manifest.repository,
        repository_role=manifest.repository_role,
        root_path=repository_root,
        manifest=manifest,
        agents=discover_plugin_items(
            repository_root,
            "agents",
        ),
        skills=discover_plugin_items(
            repository_root,
            "skills",
        ),
        rules=discover_plugin_items(
            repository_root,
            "rules",
        ),
        hooks=discover_plugin_items(
            repository_root,
            "hooks",
        ),
    )
def get_repository_manifest(
    repository_name: str,
) -> RepositoryManifest | None:

    result = discover_all()

    for repo in result.repositories:
        if repo.repository == repository_name:
            return repo.manifest

    return None

def discover_all() -> DiscoveryResult:

    result = DiscoveryResult()

    for repository in discover_repositories():

        inventory = discover_repository(
            repository
        )

        if inventory:
            result.repositories.append(
                inventory
            )

    return result