from __future__ import annotations

import json
import sys
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_agents.prompts.models import (
    PromptMetadata,
    PromptRenderRequest,
    PromptTemplate,
    PromptVariable,
)


def prompt_metadata() -> PromptMetadata:
    return PromptMetadata(
        name="project-plan",
        display_name="Project Plan",
        description="Creates a project plan.",
        version="0.1.0",
        author="TASC",
        tags=["planning", "project"],
    )


def prompt_variable() -> PromptVariable:
    return PromptVariable(
        name="project_name",
        description="Name of the project.",
        required=True,
        default_value=None,
    )


def prompt_template() -> PromptTemplate:
    return PromptTemplate(
        metadata=prompt_metadata(),
        system_prompt="You create project plans.",
        user_prompt="Create a plan for {{ project_name }}.",
        variables=[prompt_variable()],
    )


class PromptModelTests(unittest.TestCase):
    def test_construction(self) -> None:
        request = PromptRenderRequest(
            template=prompt_template(),
            values={"project_name": "TASC Builder"},
        )

        self.assertEqual(request.template.metadata.name, "project-plan")
        self.assertEqual(request.values["project_name"], "TASC Builder")

    def test_equality(self) -> None:
        self.assertEqual(
            PromptRenderRequest(
                template=prompt_template(),
                values={"project_name": "TASC Builder"},
            ),
            PromptRenderRequest(
                template=prompt_template(),
                values={"project_name": "TASC Builder"},
            ),
        )

    def test_immutability(self) -> None:
        metadata = prompt_metadata()

        with self.assertRaises(FrozenInstanceError):
            metadata.name = "changed"

    def test_nested_composition(self) -> None:
        template = prompt_template()

        self.assertEqual(template.metadata.tags, ["planning", "project"])
        self.assertEqual(template.variables[0].name, "project_name")

    def test_to_dict(self) -> None:
        request = PromptRenderRequest(
            template=prompt_template(),
            values={"project_name": "TASC Builder"},
        )

        self.assertEqual(
            request.to_dict(),
            {
                "template": {
                    "metadata": {
                        "name": "project-plan",
                        "display_name": "Project Plan",
                        "description": "Creates a project plan.",
                        "version": "0.1.0",
                        "author": "TASC",
                        "tags": ["planning", "project"],
                    },
                    "system_prompt": "You create project plans.",
                    "user_prompt": "Create a plan for {{ project_name }}.",
                    "variables": [
                        {
                            "name": "project_name",
                            "description": "Name of the project.",
                            "required": True,
                            "default_value": None,
                        }
                    ],
                },
                "values": {"project_name": "TASC Builder"},
            },
        )

    def test_to_dict_is_json_compatible(self) -> None:
        request = PromptRenderRequest(
            template=prompt_template(),
            values={"project_name": "TASC Builder"},
        )

        self.assertIsInstance(json.dumps(request.to_dict()), str)


if __name__ == "__main__":
    unittest.main()
