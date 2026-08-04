from __future__ import annotations

from abc import ABC, abstractmethod

from ..generation.models import GenerationRequest, GenerationResult


class IAgentProvider(ABC):
    @abstractmethod
    def generate(self, request: GenerationRequest) -> GenerationResult:
        raise NotImplementedError
