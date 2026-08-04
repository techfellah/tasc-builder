from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import PromptRenderRequest, RenderedPrompt


class IPromptService(ABC):
    @abstractmethod
    def render(self, request: PromptRenderRequest) -> RenderedPrompt:
        raise NotImplementedError
