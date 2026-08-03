from __future__ import annotations

from typing import TypeVar

from tasc_core.exceptions import RegistryException
from tasc_core.interfaces.registry import IRegistry

T = TypeVar("T")


class Registry(IRegistry):
    def __init__(self) -> None:
        self._store: dict[type, object] = {}

    def register(self, contract: type, instance: object) -> None:
        if contract in self._store:
            raise RegistryException(
                "Contract already registered",
                "TASC-REGISTRY-0002",
                details={"contract": contract.__name__},
            )
        self._store[contract] = instance

    def resolve(self, contract: type[T]) -> T:
        if contract not in self._store:
            raise RegistryException(
                "Unknown contract",
                "TASC-REGISTRY-0001",
                details={"contract": contract.__name__},
            )
        return self._store[contract]  # type: ignore[return-value]

    def contains(self, contract: type) -> bool:
        return contract in self._store

    def unregister(self, contract: type) -> None:
        if contract not in self._store:
            raise RegistryException(
                "Unknown contract",
                "TASC-REGISTRY-0003",
                details={"contract": contract.__name__},
            )
        del self._store[contract]
