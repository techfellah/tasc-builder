from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BootstrapConfiguration:
    enabled: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "enabled": self.enabled,
        }
