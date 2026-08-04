from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_agents.prompts.exceptions import PromptRenderException
from tasc_agents.prompts.interfaces import IPromptService
from tasc_agents.prompts.models import (
    PromptMetadata,
    PromptRenderRequest,
    PromptTemplate,
    PromptVariable,
)
from tasc_agents.prompts.services import PromptService


def prompt_template(
    system_prompt: str = "System: {name}",
    user_prompt: str = "User: {name}",
    variables: list[PromptVariable] | None = None,
) -> PromptTemplate:
    return PromptTemplate(
        metadata=PromptMetadata(
            name="greeting",
            display_name="Greeting",
            description="Creates a greeting.",
            version="0.1.0",
            author="TASC",
            tags=[],
        ),
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        variables=variables
        if variables is not None
        else [
            PromptVariable(
                name="name",
                description="Name to greet.",
                required=True,
                default_value=None,
            )
        ],
    )


class PromptServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = PromptService()

    def test_renders_system_prompt(self) -> None:
        request = PromptRenderRequest(
            template=prompt_template(user_prompt="User prompt."),
            values={"name": "Alice"},
        )

        result = self.service.render(request)

        self.assertEqual(result.system_prompt, "System: Alice")

    def test_renders_user_prompt(self) -> None:
        request = PromptRenderRequest(
            template=prompt_template(system_prompt="System prompt."),
            values={"name": "Alice"},
        )

        result = self.service.render(request)

        self.assertEqual(result.user_prompt, "User: Alice")

    def test_renders_both_prompts(self) -> None:
        request = PromptRenderRequest(
            template=prompt_template(),
            values={"name": "Alice"},
        )

        result = self.service.render(request)

        self.assertEqual(result.system_prompt, "System: Alice")
        self.assertEqual(result.user_prompt, "User: Alice")
        self.assertEqual(result.variables, {"name": "Alice"})

    def test_required_variable_is_validated(self) -> None:
        request = PromptRenderRequest(template=prompt_template(), values={})

        with self.assertRaises(PromptRenderException):
            self.service.render(request)

    def test_rendering_failure_raises_prompt_render_exception(self) -> None:
        request = PromptRenderRequest(
            template=prompt_template(
                system_prompt="System: {missing}",
                variables=[],
            ),
            values={},
        )

        with self.assertRaises(PromptRenderException):
            self.service.render(request)

    def test_interface_compliance(self) -> None:
        self.assertTrue(issubclass(PromptService, IPromptService))
        self.assertIsInstance(self.service, IPromptService)


if __name__ == "__main__":
    unittest.main()
