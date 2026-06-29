from __future__ import annotations


class RepositoryResolver:

    def resolve(
        self,
        query: str,
    ):

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

            "terraform":
                "hub_infra",

            "infrastructure":
                "hub_infra",
        }

        repositories = []

        for alias, repo in (
            aliases.items()
        ):

            if alias in query:

                repositories.append(
                    repo
                )

        return list(
            dict.fromkeys(
                repositories
            )
        )

    def first(
        self,
        query: str,
    ):

        repositories = (
            self.resolve(
                query
            )
        )

        if repositories:

            return repositories[0]

        return None


repository_resolver = (
    RepositoryResolver()
)