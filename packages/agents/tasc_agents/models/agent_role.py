from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentRole:
    role_name: str
    responsibilities: list[str]
    system_prompt: str

    def to_dict(self) -> dict[str, object]:
        return {
            "role_name": self.role_name,
            "responsibilities": list(self.responsibilities),
            "system_prompt": self.system_prompt,
        }
