from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PromptVariable:
    name: str
    description: str
    required: bool
    default_value: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "description": self.description,
            "required": self.required,
            "default_value": self.default_value,
        }
