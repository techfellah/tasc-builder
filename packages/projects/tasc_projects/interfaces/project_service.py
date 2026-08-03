from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Project, ProjectConfiguration, ProjectMetadata


class IProjectService(ABC):
    @abstractmethod
    def create_project(
        self,
        metadata: ProjectMetadata,
        configuration: ProjectConfiguration,
    ) -> Project:
        raise NotImplementedError

    @abstractmethod
    def get_project(self, name: str) -> Project:
        raise NotImplementedError

    @abstractmethod
    def list_projects(self) -> list[Project]:
        raise NotImplementedError

    @abstractmethod
    def delete_project(self, name: str) -> None:
        raise NotImplementedError
