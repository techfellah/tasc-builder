from __future__ import annotations

from dataclasses import dataclass

from .prompt_template import PromptTemplate


@dataclass(frozen=True)
class PromptRenderRequest:
    template: PromptTemplate
    values: dict[str, str]

    def to_dict(self) -> dict[str, object]:
        return {
            "template": self.template.to_dict(),
            "values": dict(self.values),
        }
