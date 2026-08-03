from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentModel:
    provider: str
    model: str
    temperature: float
    max_tokens: int

    def to_dict(self) -> dict[str, object]:
        return {
            "provider": self.provider,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
