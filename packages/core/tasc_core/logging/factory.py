from __future__ import annotations

from tasc_core.interfaces.logger import ILoggerFactory
from tasc_core.logging.logger import CoreLogger


class LoggerFactory(ILoggerFactory):
    def create_logger(self, name: str) -> CoreLogger:
        return CoreLogger(name)
