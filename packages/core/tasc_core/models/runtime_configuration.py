from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeConfiguration:
    environment: str
    version: str

    def to_dict(self) -> dict[str, object]:
        return {
            "environment": self.environment,
            "version": self.version,
        }
