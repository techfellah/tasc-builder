from __future__ import annotations

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_agents.prompts.exceptions import PromptException
from tasc_agents.prompts.interfaces import IPromptRepository
from tasc_agents.prompts.models import PromptMetadata, PromptTemplate, PromptVariable
from tasc_agents.prompts.repositories import FilesystemPromptRepository


def prompt_template(name: str) -> PromptTemplate:
    return PromptTemplate(
        metadata=PromptMetadata(
            name=name,
            display_name=name.title(),
            description=f"{name} prompt.",
            version="0.1.0",
            author="TASC",
            tags=["test"],
        ),
        system_prompt="You are helpful.",
        user_prompt="Hello {name}.",
        variables=[
            PromptVariable(
                name="name",
                description="Name to greet.",
                required=True,
                default_value=None,
            )
        ],
    )


class FilesystemPromptRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.repository = FilesystemPromptRepository(self.root)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_discovers_yaml_templates_beneath_root(self) -> None:
        expected = prompt_template("greeting")
        self._write_template(self.root / "nested" / "greeting.yaml", expected)

        self.assertEqual(self.repository.list(), [expected])

    def test_get_returns_prompt_template(self) -> None:
        expected = prompt_template("greeting")
        self._write_template(self.root / "greeting.yaml", expected)

        self.assertEqual(self.repository.get("greeting"), expected)

    def test_list_returns_discovered_templates(self) -> None:
        first = prompt_template("first")
        second = prompt_template("second")
        self._write_template(self.root / "first.yaml", first)
        self._write_template(self.root / "second.yaml", second)

        self.assertEqual(self.repository.list(), [first, second])

    def test_exists_returns_boolean(self) -> None:
        self.assertFalse(self.repository.exists("greeting"))
        self._write_template(self.root / "greeting.yaml", prompt_template("greeting"))

        self.assertTrue(self.repository.exists("greeting"))

    def test_malformed_yaml_raises_prompt_exception(self) -> None:
        malformed_file = self.root / "greeting.yaml"
        malformed_file.write_text("metadata: [", encoding="utf-8")

        with self.assertRaises(PromptException):
            self.repository.get("greeting")

    def test_missing_template_raises_prompt_exception(self) -> None:
        with self.assertRaises(PromptException):
            self.repository.get("missing")

    def test_interface_compliance(self) -> None:
        self.assertTrue(issubclass(FilesystemPromptRepository, IPromptRepository))
        self.assertIsInstance(self.repository, IPromptRepository)

    @staticmethod
    def _write_template(path: Path, template: PromptTemplate) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(template.to_dict(), sort_keys=False), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
