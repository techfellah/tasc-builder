from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RenderedPrompt:
    system_prompt: str
    user_prompt: str
    variables: dict[str, str]

    def to_dict(self) -> dict[str, object]:
        return {
            "system_prompt": self.system_prompt,
            "user_prompt": self.user_prompt,
            "variables": dict(self.variables),
        }
