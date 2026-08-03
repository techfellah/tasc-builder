from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderConfiguration:
    name: str
    kind: str

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "kind": self.kind,
        }
