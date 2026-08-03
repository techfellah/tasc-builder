from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from tasc_core.interfaces.logger import ILogger
from tasc_core.logging.formatter import LogFormatter
from tasc_core.models.log_level import LogLevel
from tasc_core.models.log_record import LogRecord


class CoreLogger(ILogger):
    _LEVELS = {
        LogLevel.DEBUG: logging.DEBUG,
        LogLevel.INFO: logging.INFO,
        LogLevel.WARNING: logging.WARNING,
        LogLevel.ERROR: logging.ERROR,
        LogLevel.CRITICAL: logging.CRITICAL,
    }

    def __init__(self, name: str) -> None:
        self._name = name
        self._logger = logging.getLogger(name)

    def debug(self, message: str, **context: Any) -> None:
        self._emit(LogLevel.DEBUG, message, context)

    def info(self, message: str, **context: Any) -> None:
        self._emit(LogLevel.INFO, message, context)

    def warning(self, message: str, **context: Any) -> None:
        self._emit(LogLevel.WARNING, message, context)

    def error(self, message: str, **context: Any) -> None:
        self._emit(LogLevel.ERROR, message, context)

    def critical(self, message: str, **context: Any) -> None:
        self._emit(LogLevel.CRITICAL, message, context)

    def exception(self, message: str, exception: Exception, **context: Any) -> None:
        self._emit(LogLevel.ERROR, message, context, exception=str(exception))

    def _emit(
        self,
        level: LogLevel,
        message: str,
        context: dict[str, Any],
        exception: str | None = None,
    ) -> None:
        record = LogRecord(
            timestamp=datetime.now(timezone.utc),
            level=level,
            logger=self._name,
            message=message,
            context=context,
            exception=exception,
        )
        output = LogFormatter().format(record)
        self._logger.log(self._LEVELS[level], output)
