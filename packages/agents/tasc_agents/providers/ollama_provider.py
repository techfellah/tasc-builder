from __future__ import annotations

from ..interfaces import IAgentProvider
from ..models import Agent


class OllamaProvider(IAgentProvider):
    """Placeholder Ollama provider."""

    def generate(
        self,
        agent: Agent,
        prompt: str,
        context: dict[str, object],
    ) -> str:
        return "Provider execution not yet implemented."
