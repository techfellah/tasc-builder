from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MetadataConfiguration:
    name: str
    version: str
    description: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
        }
