from __future__ import annotations

from dataclasses import dataclass

from .prompt_metadata import PromptMetadata
from .prompt_variable import PromptVariable


@dataclass(frozen=True)
class PromptTemplate:
    metadata: PromptMetadata
    system_prompt: str
    user_prompt: str
    variables: list[PromptVariable]

    def to_dict(self) -> dict[str, object]:
        return {
            "metadata": self.metadata.to_dict(),
            "system_prompt": self.system_prompt,
            "user_prompt": self.user_prompt,
            "variables": [variable.to_dict() for variable in self.variables],
        }
