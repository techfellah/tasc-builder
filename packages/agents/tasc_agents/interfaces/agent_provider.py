from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Agent


class IAgentProvider(ABC):
    @abstractmethod
    def generate(
        self,
        agent: Agent,
        prompt: str,
        context: dict[str, object],
    ) -> str:
        raise NotImplementedError
