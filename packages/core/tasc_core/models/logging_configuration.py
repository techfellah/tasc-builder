from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LoggingConfiguration:
    level: str
    format: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "level": self.level,
            "format": self.format,
        }
