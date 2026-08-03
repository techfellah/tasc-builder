from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from tasc_core.interfaces.logger import ILoggerFactory
from tasc_core.interfaces.runtime_context import IRuntimeContext


@dataclass(frozen=True, init=False)
class RuntimeContext(IRuntimeContext):
    _configuration: Any = field(repr=False, compare=False)
    _logger_factory: ILoggerFactory = field(repr=False, compare=False)
    _registry: Any = field(repr=False, compare=False)
    _environment: str = field(repr=False, compare=False)
    _version: str = field(repr=False, compare=False)
    _started_at: datetime = field(repr=False, compare=False)

    def __init__(
        self,
        configuration: Any,
        logger_factory: ILoggerFactory,
        registry: Any,
        environment: str,
        version: str,
        started_at: datetime,
    ) -> None:
        object.__setattr__(self, "_configuration", configuration)
        object.__setattr__(self, "_logger_factory", logger_factory)
        object.__setattr__(self, "_registry", registry)
        object.__setattr__(self, "_environment", environment)
        object.__setattr__(self, "_version", version)
        object.__setattr__(self, "_started_at", started_at)

    @property
    def configuration(self) -> Any:
        return self._configuration

    @property
    def logger_factory(self) -> ILoggerFactory:
        return self._logger_factory

    @property
    def registry(self) -> Any:
        return self._registry

    @property
    def environment(self) -> str:
        return self._environment

    @property
    def version(self) -> str:
        return self._version

    @property
    def started_at(self) -> datetime:
        return self._started_at
