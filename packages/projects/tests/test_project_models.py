from __future__ import annotations

import json
import sys
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_projects.models import Project, ProjectConfiguration, ProjectMetadata


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


class ProjectModelTests(unittest.TestCase):
    def test_construction(self) -> None:
        metadata = project_metadata()
        configuration = project_configuration()
        project = Project(metadata=metadata, configuration=configuration)

        self.assertEqual(project.metadata, metadata)
        self.assertEqual(project.configuration, configuration)

    def test_equality(self) -> None:
        self.assertEqual(
            Project(metadata=project_metadata(), configuration=project_configuration()),
            Project(metadata=project_metadata(), configuration=project_configuration()),
        )

    def test_immutability(self) -> None:
        metadata = project_metadata()

        with self.assertRaises(FrozenInstanceError):
            metadata.name = "changed"

    def test_nested_composition(self) -> None:
        project = Project(
            metadata=project_metadata(),
            configuration=project_configuration(),
        )

        self.assertEqual(project.metadata.display_name, "Demo Project")
        self.assertEqual(project.configuration.framework, "Typer")

    def test_to_dict(self) -> None:
        project = Project(
            metadata=project_metadata(),
            configuration=project_configuration(),
        )

        self.assertEqual(
            project.to_dict(),
            {
                "metadata": {
                    "name": "demo",
                    "display_name": "Demo Project",
                    "description": "A demo project.",
                    "version": "0.1.0",
                    "created_at": "2026-08-03T12:00:00+00:00",
                },
                "configuration": {
                    "language": "Python",
                    "framework": "Typer",
                    "runtime": "Python 3.12",
                    "output_directory": "dist",
                },
            },
        )

    def test_to_dict_is_json_compatible(self) -> None:
        project = Project(
            metadata=project_metadata(),
            configuration=project_configuration(),
        )

        self.assertIsInstance(json.dumps(project.to_dict()), str)


if __name__ == "__main__":
    unittest.main()
