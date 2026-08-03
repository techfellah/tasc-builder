from __future__ import annotations

from tasc_core.models.log_record import LogRecord


class LogFormatter:
    def format(self, record: LogRecord) -> str:
        return (
            f"{record.timestamp.isoformat()}\n"
            f"{record.level.value}\n"
            f"{record.logger}\n"
            f"{record.message}"
        )
