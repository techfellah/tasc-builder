from __future__ import annotations

import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_projects.exceptions import ProjectException
from tasc_projects.models import Project, ProjectConfiguration, ProjectMetadata
from tasc_projects.services import FilesystemProjectRepository


def project(name: str = "demo") -> Project:
    return Project(
        metadata=ProjectMetadata(
            name=name,
            display_name="Demo Project",
            description="A demo project.",
            version="0.1.0",
            created_at=datetime(2026, 8, 3, 12, 0, tzinfo=timezone.utc),
        ),
        configuration=ProjectConfiguration(
            language="Python",
            framework="Typer",
            runtime="Python 3.12",
            output_directory="dist",
        ),
    )


class FilesystemProjectRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.workspace_path = Path(self.temporary_directory.name)
        self.repository = FilesystemProjectRepository(self.workspace_path)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_create_writes_project_yaml(self) -> None:
        self.repository.create(project())

        self.assertTrue(
            (self.workspace_path / "projects" / "demo" / "project.yaml").is_file()
        )

    def test_get_returns_project(self) -> None:
        expected = project()
        self.repository.create(expected)

        self.assertEqual(self.repository.get("demo"), expected)

    def test_list_returns_projects(self) -> None:
        first = project("first")
        second = project("second")
        self.repository.create(first)
        self.repository.create(second)

        self.assertEqual(self.repository.list(), [first, second])

    def test_exists_returns_boolean(self) -> None:
        self.assertFalse(self.repository.exists("demo"))
        self.repository.create(project())

        self.assertTrue(self.repository.exists("demo"))

    def test_delete_removes_project_directory(self) -> None:
        self.repository.create(project())

        self.repository.delete("demo")

        self.assertFalse((self.workspace_path / "projects" / "demo").exists())

    def test_duplicate_project_raises_project_exception(self) -> None:
        self.repository.create(project())

        with self.assertRaises(ProjectException):
            self.repository.create(project())

    def test_missing_project_raises_project_exception(self) -> None:
        with self.assertRaises(ProjectException):
            self.repository.get("missing")

    def test_malformed_yaml_raises_project_exception(self) -> None:
        project_directory = self.workspace_path / "projects" / "demo"
        project_directory.mkdir(parents=True)
        (project_directory / "project.yaml").write_text(
            "metadata: [",
            encoding="utf-8",
        )

        with self.assertRaises(ProjectException):
            self.repository.get("demo")


if __name__ == "__main__":
    unittest.main()
