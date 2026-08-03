from __future__ import annotations

import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_projects.interfaces import IProjectRepository, IProjectService
from tasc_projects.models import Project, ProjectConfiguration, ProjectMetadata
from tasc_projects.services import ProjectService


def project_metadata() -> ProjectMetadata:
    return ProjectMetadata(
        name="demo",
        display_name="Demo Project",
        description="A demo project.",
        version="0.1.0",
        created_at=datetime(2026, 8, 3, 12, 0, tzinfo=timezone.utc),
    )


def project_configuration() -> ProjectConfiguration:
    return ProjectConfiguration(
        language="Python",
        framework="Typer",
        runtime="Python 3.12",
        output_directory="dist",
    )


class ProjectServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = Mock(spec=IProjectRepository)
        self.service = ProjectService(self.repository)

    def test_create_project_calls_repository_create(self) -> None:
        metadata = project_metadata()
        configuration = project_configuration()

        project = self.service.create_project(metadata, configuration)

        self.assertEqual(project, Project(metadata, configuration))
        self.repository.create.assert_called_once_with(project)

    def test_get_project_calls_repository_get(self) -> None:
        project = Project(project_metadata(), project_configuration())
        self.repository.get.return_value = project

        result = self.service.get_project("demo")

        self.assertIs(result, project)
        self.repository.get.assert_called_once_with("demo")

    def test_list_projects_calls_repository_list(self) -> None:
        projects = [Project(project_metadata(), project_configuration())]
        self.repository.list.return_value = projects

        result = self.service.list_projects()

        self.assertIs(result, projects)
        self.repository.list.assert_called_once_with()

    def test_delete_project_calls_repository_delete(self) -> None:
        self.service.delete_project("demo")

        self.repository.delete.assert_called_once_with("demo")

    def test_interface_compliance(self) -> None:
        self.assertTrue(issubclass(ProjectService, IProjectService))
        self.assertIsInstance(self.service, IProjectService)


if __name__ == "__main__":
    unittest.main()
