from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PromptMetadata:
    name: str
    display_name: str
    description: str
    version: str
    author: str
    tags: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "tags": list(self.tags),
        }
