from __future__ import annotations

from dataclasses import dataclass

from .agent_configuration import AgentConfiguration
from .agent_metadata import AgentMetadata
from .agent_model import AgentModel
from .agent_role import AgentRole


@dataclass(frozen=True)
class Agent:
    metadata: AgentMetadata
    role: AgentRole
    model: AgentModel
    configuration: AgentConfiguration

    def to_dict(self) -> dict[str, object]:
        return {
            "metadata": self.metadata.to_dict(),
            "role": self.role.to_dict(),
            "model": self.model.to_dict(),
            "configuration": self.configuration.to_dict(),
        }
