from __future__ import annotations

from typing import TYPE_CHECKING

from ..interfaces import IAgentExecutor, IAgentProvider
from ..models import Agent

if TYPE_CHECKING:
    from tasc_core.interfaces.registry import IRegistry


class AgentExecutor(IAgentExecutor):
    """Delegate Agent execution to the registered provider."""

    def __init__(self, registry: IRegistry) -> None:
        self._registry = registry

    def execute(
        self,
        agent: Agent,
        prompt: str,
        context: dict[str, object],
    ) -> str:
        _ = agent.model.provider
        provider = self._registry.resolve(IAgentProvider)
        return provider.generate(agent, prompt, context)
