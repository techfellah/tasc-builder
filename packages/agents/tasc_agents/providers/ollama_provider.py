from __future__ import annotations

from ..generation.models import GenerationRequest, GenerationResult, GenerationUsage
from ..interfaces import IAgentProvider


class OllamaProvider(IAgentProvider):
    """Placeholder Ollama provider."""

    def generate(self, request: GenerationRequest) -> GenerationResult:
        return GenerationResult(
            content="Provider execution not yet implemented.",
            provider=request.model.provider,
            model=request.model.model,
            usage=GenerationUsage(input_tokens=0, output_tokens=0, total_tokens=0),
            finish_reason="not_implemented",
            duration_ms=0,
            metadata={"status": "placeholder"},
        )
