from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModulesConfiguration:
    enabled: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "enabled": list(self.enabled),
        }
