from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GenerationUsage:
    input_tokens: int
    output_tokens: int
    total_tokens: int

    def to_dict(self) -> dict[str, object]:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
        }
