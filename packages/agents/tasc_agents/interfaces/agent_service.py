from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Agent


class IAGentService(ABC):
    @abstractmethod
    def create_agent(self, agent: Agent) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_agent(self, name: str) -> Agent:
        raise NotImplementedError

    @abstractmethod
    def list_agents(self) -> list[Agent]:
        raise NotImplementedError

    @abstractmethod
    def delete_agent(self, name: str) -> None:
        raise NotImplementedError
