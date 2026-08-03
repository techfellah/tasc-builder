from __future__ import annotations

from ..interfaces import IProjectRepository, IProjectService
from ..models import Project, ProjectConfiguration, ProjectMetadata


class ProjectService(IProjectService):
    """Coordinate Project operations through a repository."""

    def __init__(self, repository: IProjectRepository) -> None:
        self._repository = repository

    def create_project(
        self,
        metadata: ProjectMetadata,
        configuration: ProjectConfiguration,
    ) -> Project:
        project = Project(metadata=metadata, configuration=configuration)
        self._repository.create(project)
        return project

    def get_project(self, name: str) -> Project:
        return self._repository.get(name)

    def list_projects(self) -> list[Project]:
        return self._repository.list()

    def delete_project(self, name: str) -> None:
        self._repository.delete(name)
