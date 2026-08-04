from __future__ import annotations

from dataclasses import dataclass

from .generation_usage import GenerationUsage


@dataclass(frozen=True)
class GenerationResult:
    content: str
    provider: str
    model: str
    usage: GenerationUsage
    finish_reason: str
    duration_ms: int
    metadata: dict[str, str]

    def to_dict(self) -> dict[str, object]:
        return {
            "content": self.content,
            "provider": self.provider,
            "model": self.model,
            "usage": self.usage.to_dict(),
            "finish_reason": self.finish_reason,
            "duration_ms": self.duration_ms,
            "metadata": dict(self.metadata),
        }
