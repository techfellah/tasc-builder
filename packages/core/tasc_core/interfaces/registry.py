from __future__ import annotations

from abc import ABC, abstractmethod


class IRegistry(ABC):
    @abstractmethod
    def register(self, contract: type, instance: object) -> None:
        raise NotImplementedError

    @abstractmethod
    def resolve(self, contract: type) -> object:
        raise NotImplementedError

    @abstractmethod
    def contains(self, contract: type) -> bool:
        raise NotImplementedError

    @abstractmethod
    def unregister(self, contract: type) -> None:
        raise NotImplementedError
