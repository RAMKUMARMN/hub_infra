from __future__ import annotations

from typing import Optional
from app.router.skill_keywords import (
    SKILL_KEYWORDS,
)
from app.registry.skill_registry import (
    skill_registry,
)
from app.router.repository_resolver import (
    repository_resolver,
)
from app.router.multi_skill_resolver import (
    multi_skill_resolver,
)
from app.registry.tool_registry import (
    tool_registry,
)


class PluginRouter:

    def __init__(self):

        self._ready = False

        self._skill_keywords = (
            SKILL_KEYWORDS
        )

    def build(self):

        if self._ready:
            return

        skill_registry.build()

        tool_registry.build()

        self._ready = True

    def _candidate_skills(
        self,
        repository: str | None,
    ):

        skills = (
            skill_registry.get_all()
        )

        if not repository:
            return skills

        return [

            skill

            for skill in skills

            if (
                skill.repository
                == repository
            )
        ]

    def find_repository_hint(
        self,
        query: str,
    ) -> Optional[str]:

        query = query.lower()

        aliases = {

            "backend":
                "hub_backend",

            "frontend":
                "hub_frontend",

            "mobile":
                "hub_mobile",

            "android":
                "hub_android",

            "ios":
                "hub_ios",

            "notify":
                "hub_notify",

            "notification":
                "hub_notify",

            "infra":
                "hub_infra",

            "infrastructure":
                "hub_infra",
        }

        for alias, repository in (
            aliases.items()
        ):

            if alias in query:

                return repository

        return None

    def find_exact_skill(
        self,
        query: str,
        repository: str | None = None,
    ):

        query = query.lower()

        skills = (
            self._candidate_skills(
                repository
            )
        )

        for skill in skills:

            skill_name = (
                skill.skill_id
                .replace("-", " ")
                .lower()
            )

            if skill_name in query:

                return skill

        return None

    def find_keyword_skill(
        self,
        query: str,
        repository: str | None = None,
    ):

        query = query.lower()

        skills = (
            self._candidate_skills(
                repository
            )
        )

        for skill in skills:

            keywords = (
                self._skill_keywords.get(
                    skill.skill_id,
                    [],
                )
            )

            for keyword in keywords:

                if keyword in query:

                    return skill

        return None

    def route(
        self,
        user_query: str,
    ):

        self.build()
        repositories = (
            repository_resolver.resolve(
                user_query
            )
        )

        if (
            len(repositories)
            > 1
        ):

            cross_skills = []

            for repository in (
                repositories
            ):

                matched_skills = (
                    multi_skill_resolver
                    .resolve(
                        repository,
                        user_query,
                    )
                )

                for skill in (
                    matched_skills
                ):

                    if (
                        not skill.tool
                        or not skill.mcp_server
                    ):
                        continue

                    cross_skills.append(
                        {

                            "repository":
                                repository,

                            "skill":
                                skill.skill_id,

                            "tool":
                                skill.tool,

                            "mcp_tool":
                                tool_registry
                                .to_mcp_tool_name(
                                    skill.tool
                                ),

                            "server":
                                skill.mcp_server,
                        }
                    )

            if cross_skills:

                return {

                    "type":
                        "cross_repo_plugin",
                    "query":
                        user_query,

                    "repositories":
                        repositories,

                    "skills":
                        cross_skills,
                }
        repository_hint = (
            self.find_repository_hint(
                user_query
            )
        )
        query = (
            user_query.lower()
        )
        #
# Feature tracing priority
#

        if (
            "trace" in query
            and "feature" in query
        ):

            trace_skills = []

            for skill in (
                skill_registry.get_all()
            ):

                if (
                    skill.skill_id
                    in {
                        "trace-backend-features",
                        "trace-frontend-features",
                    }
                ):

                    trace_skills.append(
                        {
                            "repository":
                                skill.repository,

                            "skill":
                                skill.skill_id,

                            "tool":
                                skill.tool,

                            "mcp_tool":
                                tool_registry
                                .to_mcp_tool_name(
                                    skill.tool
                                ),

                            "server":
                                skill.mcp_server,
                        }
                    )

            if trace_skills:

                return {

                    "type":
                        "cross_repo_plugin",

                    "query":
                        user_query,

                    "repositories": [
                        item[
                            "repository"
                        ]
                        for item
                        in trace_skills
                    ],

                    "skills":
                        trace_skills,
                }

        if repository_hint:

            matched_skills = (
                multi_skill_resolver
                .resolve(
                    repository_hint,
                    user_query
                )
            )

            valid_skills = []

            for skill in matched_skills:

                if (
                    not skill.tool
                    or not skill.mcp_server
                ):
                    continue

                valid_skills.append(
                    {

                        "repository":
                            skill.repository,
                        "skill":
                            skill.skill_id,

                        "tool":
                            skill.tool,

                        "mcp_tool":
                            tool_registry
                            .to_mcp_tool_name(
                                skill.tool
                            ),

                        "server":
                            skill.mcp_server,
                    }
                )

            if (
                len(
                    valid_skills
                ) > 1
            ):

                return {

                    "type":
                        "multi_plugin",
                    "query":
                        user_query,

                    "repository":
                        repository_hint,

                    "skills":
                        valid_skills,
                }

        skill = self.find_exact_skill(
            user_query,
            repository_hint,
        )

        if not skill:

            skill = self.find_keyword_skill(
                user_query,
                repository_hint,
            )

        if (
            not skill
            and repository_hint
        ):

            return {

                "type": "llm",

                "repository":
                    repository_hint,

                "skill": None,

                "tool": None,

                "server": None,
            }

        if not skill:

            skill = self.find_exact_skill(
                user_query
            )

        if not skill:

            skill = self.find_keyword_skill(
                user_query
            )

        if not skill:

            return {

                "type": "llm",

                "repository":
                    repository_hint,

                "skill": None,

                "tool": None,

                "server": None,
            }

        if (
            skill.mcp_server
            and skill.tool
        ):

            return {

                "type": "plugin",
                "query":
                    user_query,

                "repository":
                    skill.repository,

                "skill":
                    skill.skill_id,

                "tool":
                    skill.tool,

                "mcp_tool":
                    tool_registry
                    .to_mcp_tool_name(
                        skill.tool
                    ),

                "server":
                    skill.mcp_server,
            }

        return {

            "type": "llm",

            "repository":
                repository_hint,

            "skill": None,

            "tool": None,

            "server": None,
        }


plugin_router = (
    PluginRouter()
)