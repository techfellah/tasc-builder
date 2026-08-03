from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ProjectMetadata:
    name: str
    display_name: str
    description: str
    version: str
    created_at: datetime

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
        }
