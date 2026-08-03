from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from pathlib import Path


class IConfigurationLoader(ABC):
    @abstractmethod
    def load(self, path: Path) -> str:
        raise NotImplementedError


class IConfigurationParser(ABC):
    @abstractmethod
    def parse(self, text: str) -> Mapping[str, object]:
        raise NotImplementedError


class IConfigurationValidator(ABC):
    @abstractmethod
    def validate(self, data: Mapping[str, object]) -> None:
        raise NotImplementedError


class IConfigurationProvider(ABC):
    @abstractmethod
    def get_configuration(self) -> object:
        raise NotImplementedError
