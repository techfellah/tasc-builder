from __future__ import annotations

from typing import TYPE_CHECKING

from ..generation.models import GenerationRequest, GenerationResult
from ..interfaces import IAgentExecutor, IAgentProvider
from ..models import Agent
from ..prompts.models import RenderedPrompt

if TYPE_CHECKING:
    from tasc_core.interfaces.registry import IRegistry


class AgentExecutor(IAgentExecutor):
    """Delegate Agent execution to the registered provider."""

    def __init__(self, registry: IRegistry) -> None:
        self._registry = registry

    def execute(
        self,
        agent: Agent,
        prompt: RenderedPrompt,
        context: dict[str, str],
    ) -> GenerationResult:
        _ = agent.model.provider
        provider = self._registry.resolve(IAgentProvider)
        request = GenerationRequest(
            prompt=prompt,
            model=agent.model,
            metadata=dict(context),
        )
        return provider.generate(request)
