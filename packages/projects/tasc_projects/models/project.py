from __future__ import annotations

from dataclasses import dataclass

from .project_configuration import ProjectConfiguration
from .project_metadata import ProjectMetadata


@dataclass(frozen=True)
class Project:
    metadata: ProjectMetadata
    configuration: ProjectConfiguration

    def to_dict(self) -> dict[str, object]:
        return {
            "metadata": self.metadata.to_dict(),
            "configuration": self.configuration.to_dict(),
        }
