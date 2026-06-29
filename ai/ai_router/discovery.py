import asyncio

from app.router.plugin_router import (
    plugin_router,
)
from app.context.context_builder import (
    context_builder,
)
from app.context.explanation_service import(
        explanation_service,
)
from app.router.execution_planner import (
    execution_planner,
)
from app.router.repository_resolver import(
        repository_resolver,
)
from app.mcp.mcp_tool_runner import (
    mcp_tool_runner,
)

from app.formatter.result_formatter import(
    result_formatter,
)
async def main():

        route = plugin_router.route(
            "trace chat implementation"
        )
        print(
            repository_resolver.resolve(
                "trace chat implementation"
            )
        )

        print(route)

        plan = execution_planner.create_plan(
            route
        )

        print(plan)

        result = await mcp_tool_runner.run(
            plan
        )
        context = (
            context_builder.build(
                result
            )
        )

        print(context)

        explanation = await (
            explanation_service.explain(
                "explain chat feature",
                context,
            )
        )
        print(explanation)

asyncio.run(
    main()
)