from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentConfiguration:
    tools: list[str]
    capabilities: list[str]
    environment: dict[str, str]

    def to_dict(self) -> dict[str, object]:
        return {
            "tools": list(self.tools),
            "capabilities": list(self.capabilities),
            "environment": dict(self.environment),
        }
