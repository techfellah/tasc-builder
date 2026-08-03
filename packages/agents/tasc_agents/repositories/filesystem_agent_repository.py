from __future__ import annotations

from datetime import datetime
from pathlib import Path

import yaml

from ..exceptions import AgentException
from ..interfaces import IAgentRepository
from ..models import Agent, AgentConfiguration, AgentMetadata, AgentModel, AgentRole


class FilesystemAgentRepository(IAgentRepository):
    """Persist Agent definitions as YAML files beneath a root directory."""

    def __init__(self, root: Path) -> None:
        self._root = root

    def create(self, agent: Agent) -> None:
        agent_path = self._agent_path(agent.metadata.name)
        if agent_path.exists():
            raise AgentException(f"Agent already exists: {agent.metadata.name}")

        try:
            agent_path.mkdir(parents=True)
            self._agent_file(agent.metadata.name).write_text(
                yaml.safe_dump(agent.to_dict(), sort_keys=False),
                encoding="utf-8",
            )
        except OSError as exc:
            raise AgentException(f"Unable to create agent: {agent.metadata.name}") from exc

    def get(self, name: str) -> Agent:
        agent_file = self._agent_file(name)
        if not agent_file.is_file():
            raise AgentException(f"Agent not found: {name}")

        try:
            data = yaml.safe_load(agent_file.read_text(encoding="utf-8"))
            return self._agent_from_data(data)
        except (OSError, TypeError, ValueError, KeyError, yaml.YAMLError) as exc:
            raise AgentException(f"Malformed agent file: {name}") from exc

    def list(self) -> list[Agent]:
        if not self._root.is_dir():
            return []

        return [
            self.get(agent_path.name)
            for agent_path in sorted(self._root.iterdir())
            if agent_path.is_dir()
        ]

    def exists(self, name: str) -> bool:
        return self._agent_file(name).is_file()

    def delete(self, name: str) -> None:
        agent_path = self._agent_path(name)
        if not agent_path.is_dir():
            raise AgentException(f"Agent not found: {name}")

        try:
            for path in sorted(agent_path.rglob("*"), reverse=True):
                if path.is_dir():
                    path.rmdir()
                else:
                    path.unlink()
            agent_path.rmdir()
        except OSError as exc:
            raise AgentException(f"Unable to delete agent: {name}") from exc

    def _agent_path(self, name: str) -> Path:
        return self._root / name

    def _agent_file(self, name: str) -> Path:
        return self._agent_path(name) / "agent.yaml"

    def _agent_from_data(self, data: object) -> Agent:
        if not isinstance(data, dict):
            raise TypeError("Agent data must be a mapping")

        metadata = data["metadata"]
        role = data["role"]
        model = data["model"]
        configuration = data["configuration"]
        if not all(
            isinstance(section, dict)
            for section in (metadata, role, model, configuration)
        ):
            raise TypeError("Agent sections must be mappings")

        return Agent(
            metadata=AgentMetadata(
                name=metadata["name"],
                display_name=metadata["display_name"],
                description=metadata["description"],
                version=metadata["version"],
                author=metadata["author"],
                created_at=datetime.fromisoformat(metadata["created_at"]),
            ),
            role=AgentRole(
                role_name=role["role_name"],
                responsibilities=role["responsibilities"],
                system_prompt=role["system_prompt"],
            ),
            model=AgentModel(
                provider=model["provider"],
                model=model["model"],
                temperature=model["temperature"],
                max_tokens=model["max_tokens"],
            ),
            configuration=AgentConfiguration(
                tools=configuration["tools"],
                capabilities=configuration["capabilities"],
                environment=configuration["environment"],
            ),
        )
