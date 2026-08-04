from __future__ import annotations

from dataclasses import dataclass

from ...models import AgentModel
from ...prompts.models import RenderedPrompt


@dataclass(frozen=True)
class GenerationRequest:
    prompt: RenderedPrompt
    model: AgentModel
    metadata: dict[str, str]

    def to_dict(self) -> dict[str, object]:
        return {
            "prompt": self.prompt.to_dict(),
            "model": self.model.to_dict(),
            "metadata": dict(self.metadata),
        }
