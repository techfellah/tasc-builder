from __future__ import annotations

from ..interfaces import IAgentRepository, IAGentService
from ..models import Agent


class AgentService(IAGentService):
    """Coordinate Agent definition operations through a repository."""

    def __init__(self, repository: IAgentRepository) -> None:
        self._repository = repository

    def create_agent(self, agent: Agent) -> None:
        self._repository.create(agent)

    def get_agent(self, name: str) -> Agent:
        return self._repository.get(name)

    def list_agents(self) -> list[Agent]:
        return self._repository.list()

    def delete_agent(self, name: str) -> None:
        self._repository.delete(name)
