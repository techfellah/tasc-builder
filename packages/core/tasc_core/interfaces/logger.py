from __future__ import annotations

from abc import ABC, abstractmethod


class ILogger(ABC):
    @abstractmethod
    def debug(self, message: str, **context) -> None:
        raise NotImplementedError

    @abstractmethod
    def info(self, message: str, **context) -> None:
        raise NotImplementedError

    @abstractmethod
    def warning(self, message: str, **context) -> None:
        raise NotImplementedError

    @abstractmethod
    def error(self, message: str, **context) -> None:
        raise NotImplementedError

    @abstractmethod
    def critical(self, message: str, **context) -> None:
        raise NotImplementedError

    @abstractmethod
    def exception(self, message: str, exception: Exception, **context) -> None:
        raise NotImplementedError


class ILoggerFactory(ABC):
    @abstractmethod
    def create_logger(self, name: str) -> ILogger:
        raise NotImplementedError
