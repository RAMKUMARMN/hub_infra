from __future__ import annotations

import re


class ToolArgumentExtractor:

    _STOP_WORDS = {

        "and",
        "or",
        "with",
        "all",
        "the",
        "a",
        "an",
        "show",
        "find",
        "list",
        "display",
        "get",
    }

    def _valid_value(
        self,
        value: str,
    ) -> bool:

        return (

            value

            and

            value.lower()
            not in self._STOP_WORDS

        )

    def _extract_after_keyword(
        self,
        query: str,
        pattern: str,
    ) -> str | None:

        match = re.search(
            pattern,
            query,
        )

        if not match:

            return None

        value = (
            match.group(
                1
            )
            .strip()
            .lower()
        )

        if not self._valid_value(
            value
        ):

            return None

        return value

    def extract(
        self,
        query: str,
    ) -> dict:

        query = query.lower()

        arguments = {}

        #
        # backend models
        #
        # show backend model user
        #

        model_name = (
            self._extract_after_keyword(
                query,
                r"(?:model|models)\s+([a-zA-Z0-9_]+)",
            )
        )

        if model_name:

            arguments[
                "name"
            ] = model_name

        #
        # backend services
        #
        # show backend service rag
        #

        service_name = (
            self._extract_after_keyword(
                query,
                r"(?:service|services)\s+([a-zA-Z0-9_]+)",
            )
        )

        if service_name:

            arguments[
                "service"
            ] = service_name

        #
        # feature tracing
        #
        # trace chat feature
        #

        feature_name = (
            self._extract_after_keyword(
                query,
                r"(?:trace|feature)\s+([a-zA-Z0-9_]+)",
            )
        )

        if feature_name:

            arguments[
                "feature"
            ] = feature_name

        #
        # frontend architecture fields
        #
        # show frontend architecture purpose
        # show frontend architecture framework
        #

        architecture_field = (
            self._extract_after_keyword(
                query,
                r"architecture\s+([a-zA-Z0-9_]+)",
            )
        )

        if architecture_field:

            arguments[
                "field"
            ] = architecture_field

        #
        # frontend component lookup
        #
        # show component navbar
        #

        component_name = (
            self._extract_after_keyword(
                query,
                r"(?:component|components)\s+([a-zA-Z0-9_]+)",
            )
        )

        if component_name:

            arguments[
                "component"
            ] = component_name

        #
        # mobile widget lookup
        #
        # show widget app_shell
        #

        widget_name = (
            self._extract_after_keyword(
                query,
                r"(?:widget|widgets)\s+([a-zA-Z0-9_]+)",
            )
        )

        if widget_name:

            arguments[
                "widget"
            ] = widget_name

        #
        # mobile screen lookup
        #
        # show screen login
        #

        screen_name = (
            self._extract_after_keyword(
                query,
                r"(?:screen|screens)\s+([a-zA-Z0-9_]+)",
            )
        )

        if screen_name:

            arguments[
                "screen"
            ] = screen_name

        #
        # terraform module lookup
        #
        # show terraform module vpc
        #

        module_name = (
            self._extract_after_keyword(
                query,
                r"(?:module|modules)\s+([a-zA-Z0-9_]+)",
            )
        )

        if module_name:

            arguments[
                "module"
            ] = module_name

        return arguments


tool_argument_extractor = (
    ToolArgumentExtractor()
)