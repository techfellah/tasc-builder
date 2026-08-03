from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .log_level import LogLevel


@dataclass(frozen=True)
class LogRecord:
    timestamp: datetime
    level: LogLevel
    logger: str
    message: str
    context: dict[str, Any]
    exception: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level.value,
            "logger": self.logger,
            "message": self.message,
            "context": self.context,
            "exception": str(self.exception) if self.exception is not None else None,
        }
