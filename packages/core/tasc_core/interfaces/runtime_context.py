from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from .logger import ILoggerFactory


class IRuntimeContext(ABC):
    @property
    @abstractmethod
    def configuration(self) -> Any:
        raise NotImplementedError

    @property
    @abstractmethod
    def logger_factory(self) -> ILoggerFactory:
        raise NotImplementedError

    @property
    @abstractmethod
    def registry(self) -> Any:
        raise NotImplementedError

    @property
    @abstractmethod
    def environment(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def version(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def started_at(self) -> datetime:
        raise NotImplementedError
