from __future__ import annotations

from datetime import datetime
from pathlib import Path

import yaml

from ..exceptions import ProjectException
from ..interfaces import IProjectRepository
from ..models import Project, ProjectConfiguration, ProjectMetadata


class FilesystemProjectRepository(IProjectRepository):
    """Persist projects as YAML files beneath a workspace."""

    def __init__(self, workspace_path: Path) -> None:
        self._workspace_path = workspace_path

    def create(self, project: Project) -> None:
        project_path = self._project_path(project.metadata.name)
        if project_path.exists():
            raise ProjectException(f"Project already exists: {project.metadata.name}")

        try:
            project_path.mkdir(parents=True)
            self._project_file(project.metadata.name).write_text(
                yaml.safe_dump(project.to_dict(), sort_keys=False),
                encoding="utf-8",
            )
        except OSError as exc:
            raise ProjectException(
                f"Unable to create project: {project.metadata.name}"
            ) from exc

    def get(self, name: str) -> Project:
        project_file = self._project_file(name)
        if not project_file.is_file():
            raise ProjectException(f"Project not found: {name}")

        try:
            data = yaml.safe_load(project_file.read_text(encoding="utf-8"))
            return self._project_from_data(data)
        except (OSError, TypeError, ValueError, KeyError, yaml.YAMLError) as exc:
            raise ProjectException(f"Malformed project file: {name}") from exc

    def list(self) -> list[Project]:
        projects_path = self._workspace_path / "projects"
        if not projects_path.is_dir():
            return []

        return [
            self.get(project_path.name)
            for project_path in sorted(projects_path.iterdir())
            if project_path.is_dir()
        ]

    def exists(self, name: str) -> bool:
        return self._project_file(name).is_file()

    def delete(self, name: str) -> None:
        project_path = self._project_path(name)
        if not project_path.is_dir():
            raise ProjectException(f"Project not found: {name}")

        try:
            for path in sorted(project_path.rglob("*"), reverse=True):
                if path.is_dir():
                    path.rmdir()
                else:
                    path.unlink()
            project_path.rmdir()
        except OSError as exc:
            raise ProjectException(f"Unable to delete project: {name}") from exc

    def _project_path(self, name: str) -> Path:
        return self._workspace_path / "projects" / name

    def _project_file(self, name: str) -> Path:
        return self._project_path(name) / "project.yaml"

    def _project_from_data(self, data: object) -> Project:
        if not isinstance(data, dict):
            raise TypeError("Project data must be a mapping")

        metadata = data["metadata"]
        configuration = data["configuration"]
        if not isinstance(metadata, dict) or not isinstance(configuration, dict):
            raise TypeError("Project sections must be mappings")

        return Project(
            metadata=ProjectMetadata(
                name=metadata["name"],
                display_name=metadata["display_name"],
                description=metadata["description"],
                version=metadata["version"],
                created_at=datetime.fromisoformat(metadata["created_at"]),
            ),
            configuration=ProjectConfiguration(
                language=configuration["language"],
                framework=configuration["framework"],
                runtime=configuration["runtime"],
                output_directory=configuration["output_directory"],
            ),
        )
