from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Agent


class IAgentRepository(ABC):
    @abstractmethod
    def create(self, agent: Agent) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, name: str) -> Agent:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Agent]:
        raise NotImplementedError

    @abstractmethod
    def exists(self, name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, name: str) -> None:
        raise NotImplementedError
