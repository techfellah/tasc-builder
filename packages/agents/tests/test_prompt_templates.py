from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_agents.prompts.repositories import FilesystemPromptRepository


TEMPLATE_ROOT = (
    Path(__file__).resolve().parents[1] / "tasc_agents" / "prompts" / "templates"
)
TEMPLATE_NAMES = {
    "architecture_review",
    "bug_fix",
    "code_generation",
    "code_review",
    "documentation",
}


class PromptTemplateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = FilesystemPromptRepository(TEMPLATE_ROOT)

    def test_repository_discovers_all_templates(self) -> None:
        self.assertEqual(
            {template.metadata.name for template in self.repository.list()},
            TEMPLATE_NAMES,
        )

    def test_every_template_loads(self) -> None:
        for name in TEMPLATE_NAMES:
            self.assertEqual(self.repository.get(name).metadata.name, name)

    def test_templates_have_required_metadata(self) -> None:
        for template in self.repository.list():
            self.assertTrue(template.metadata.name)
            self.assertTrue(template.metadata.display_name)
            self.assertTrue(template.metadata.description)
            self.assertTrue(template.metadata.version)
            self.assertTrue(template.metadata.author)

    def test_templates_have_required_prompts(self) -> None:
        for template in self.repository.list():
            self.assertTrue(template.system_prompt)
            self.assertTrue(template.user_prompt)


if __name__ == "__main__":
    unittest.main()
