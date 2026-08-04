from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import PromptTemplate


class IPromptRepository(ABC):
    @abstractmethod
    def get(self, name: str) -> PromptTemplate:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[PromptTemplate]:
        raise NotImplementedError

    @abstractmethod
    def exists(self, name: str) -> bool:
        raise NotImplementedError
