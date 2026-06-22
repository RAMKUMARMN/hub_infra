from app.registry.skill_registry import (
    skill_registry,
)

from app.router.skill_keywords import (
    SKILL_KEYWORDS,
)


class MultiSkillResolver:

    def resolve(
        self,
        repository: str,
        query: str,
    ):

        query = query.lower()

        repository_skills = (
            skill_registry
            .get_repository_skills(
                repository
            )
        )

        scored_matches = []

        for skill in (
            repository_skills
        ):

            keywords = (
                SKILL_KEYWORDS.get(
                    skill.skill_id,
                    [],
                )
            )

            score = 0

            for keyword in keywords:

                if (
                    keyword.lower()
                    in query
                ):

                    score += len(
                        keyword.split()
                    )

            if (
                score > 0
            ):

                scored_matches.append(
                    (
                        score,
                        skill,
                    )
                )

        if not scored_matches:

            return []

        highest_score = max(
            score
            for score, _
            in scored_matches
        )

        return [

            skill

            for score, skill
            in scored_matches

            if (
                score
                == highest_score
            )
        ]


multi_skill_resolver = (
    MultiSkillResolver()
)