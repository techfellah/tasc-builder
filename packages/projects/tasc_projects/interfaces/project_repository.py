from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Project


class IProjectRepository(ABC):
    @abstractmethod
    def create(self, project: Project) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, name: str) -> Project:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Project]:
        raise NotImplementedError

    @abstractmethod
    def exists(self, name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, name: str) -> None:
        raise NotImplementedError
