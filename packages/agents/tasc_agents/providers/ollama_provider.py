from __future__ import annotations

import httpx

from ..exceptions import AgentException
from ..generation.models import GenerationRequest, GenerationResult, GenerationUsage
from ..interfaces import IAgentProvider


class OllamaProvider(IAgentProvider):
    """Generate content through the local Ollama REST API."""

    _DEFAULT_BASE_URL = "http://localhost:11434"
    _TIMEOUT_SECONDS = 30

    def __init__(self, base_url: str = _DEFAULT_BASE_URL) -> None:
        self._generate_url = f"{base_url.rstrip('/')}/api/generate"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        payload = {
            "model": request.model.model,
            "prompt": (
                f"System:\n{request.prompt.system_prompt}\n\n"
                f"User:\n{request.prompt.user_prompt}"
            ),
            "stream": False,
            "options": {
                "temperature": request.model.temperature,
                "num_predict": request.model.max_tokens,
            },
        }

        try:
            response = httpx.post(
                self._generate_url,
                json=payload,
                timeout=self._TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            data = response.json()
            return self._result_from_data(data, request)
        except (httpx.HTTPError, TypeError, ValueError, KeyError) as exc:
            raise AgentException("Ollama generation failed") from exc

    @staticmethod
    def _result_from_data(
        data: object,
        request: GenerationRequest,
    ) -> GenerationResult:
        if not isinstance(data, dict):
            raise TypeError("Ollama response must be a mapping")

        content = data["response"]
        model = data.get("model", request.model.model)
        finish_reason = data.get("done_reason", "stop")
        if not all(isinstance(value, str) for value in (content, model, finish_reason)):
            raise TypeError("Ollama response fields must be strings")

        input_tokens = OllamaProvider._integer_value(data, "prompt_eval_count")
        output_tokens = OllamaProvider._integer_value(data, "eval_count")
        total_tokens = OllamaProvider._integer_value(
            data,
            "total_tokens",
            default=input_tokens + output_tokens,
        )
        total_duration = OllamaProvider._integer_value(data, "total_duration")

        metadata: dict[str, str] = {}
        if "created_at" in data:
            metadata["created_at"] = str(data["created_at"])
        if "done" in data:
            metadata["done"] = str(data["done"])

        return GenerationResult(
            content=content,
            provider=request.model.provider,
            model=model,
            usage=GenerationUsage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
            ),
            finish_reason=finish_reason,
            duration_ms=total_duration // 1_000_000,
            metadata=metadata,
        )

    @staticmethod
    def _integer_value(data: dict[object, object], key: str, default: int = 0) -> int:
        value = data.get(key, default)
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(f"Ollama response {key} must be an integer")
        return value
