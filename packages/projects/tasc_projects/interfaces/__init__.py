"""Project interface namespace."""

from .project_repository import IProjectRepository
from .project_service import IProjectService

__all__ = ["IProjectRepository", "IProjectService"]
