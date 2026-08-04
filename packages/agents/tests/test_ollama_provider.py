from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "core"))

from tasc_agents.exceptions import AgentException
from tasc_agents.generation.models import GenerationRequest
from tasc_agents.interfaces import IAgentProvider
from tasc_agents.models import AgentModel
from tasc_agents.providers import OllamaProvider
from tasc_agents.prompts.models import RenderedPrompt
from tasc_core.registry.registry import Registry


def generation_request() -> GenerationRequest:
    return GenerationRequest(
        prompt=RenderedPrompt(
            system_prompt="You are helpful.",
            user_prompt="Hello.",
            variables={},
        ),
        model=AgentModel(
            provider="ollama",
            model="llama3",
            temperature=0.2,
            max_tokens=1024,
        ),
        metadata={},
    )


class OllamaProviderTests(unittest.TestCase):
    def test_interface_compliance(self) -> None:
        self.assertTrue(issubclass(OllamaProvider, IAgentProvider))
        self.assertIsInstance(OllamaProvider(), IAgentProvider)

    @patch("tasc_agents.providers.ollama_provider.httpx.post")
    def test_generate_sends_expected_request_payload(self, post: Mock) -> None:
        response = Mock()
        response.json.return_value = {"response": "Generated content."}
        post.return_value = response

        OllamaProvider().generate(generation_request())

        post.assert_called_once_with(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": "System:\nYou are helpful.\n\nUser:\nHello.",
                "stream": False,
                "options": {"temperature": 0.2, "num_predict": 1024},
            },
            timeout=30,
        )

    @patch("tasc_agents.providers.ollama_provider.httpx.post")
    def test_generate_uses_configured_base_url(self, post: Mock) -> None:
        response = Mock()
        response.json.return_value = {"response": "Generated content."}
        post.return_value = response

        OllamaProvider("http://ollama.example:11434/").generate(generation_request())

        self.assertEqual(post.call_args.args[0], "http://ollama.example:11434/api/generate")

    @patch("tasc_agents.providers.ollama_provider.httpx.post")
    def test_generate_maps_ollama_response(self, post: Mock) -> None:
        response = Mock()
        response.json.return_value = {
            "response": "Generated content.",
            "model": "llama3",
            "done_reason": "stop",
            "prompt_eval_count": 10,
            "eval_count": 20,
            "total_duration": 2_500_000_000,
            "created_at": "2026-08-04T12:00:00Z",
            "done": True,
        }
        post.return_value = response

        result = OllamaProvider().generate(generation_request())

        self.assertEqual(result.content, "Generated content.")
        self.assertEqual(result.provider, "ollama")
        self.assertEqual(result.model, "llama3")
        self.assertEqual(result.usage.input_tokens, 10)
        self.assertEqual(result.usage.output_tokens, 20)
        self.assertEqual(result.usage.total_tokens, 30)
        self.assertEqual(result.finish_reason, "stop")
        self.assertEqual(result.duration_ms, 2500)
        self.assertEqual(
            result.metadata,
            {"created_at": "2026-08-04T12:00:00Z", "done": "True"},
        )

    @patch("tasc_agents.providers.ollama_provider.httpx.post")
    def test_timeout_raises_agent_exception(self, post: Mock) -> None:
        post.side_effect = httpx.TimeoutException("Timed out")

        with self.assertRaises(AgentException):
            OllamaProvider().generate(generation_request())

    @patch("tasc_agents.providers.ollama_provider.httpx.post")
    def test_connection_failure_raises_agent_exception(self, post: Mock) -> None:
        post.side_effect = httpx.ConnectError("Connection failed")

        with self.assertRaises(AgentException):
            OllamaProvider().generate(generation_request())

    @patch("tasc_agents.providers.ollama_provider.httpx.post")
    def test_http_failure_raises_agent_exception(self, post: Mock) -> None:
        response = Mock()
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server error",
            request=httpx.Request("POST", "http://localhost:11434/api/generate"),
            response=httpx.Response(500),
        )
        post.return_value = response

        with self.assertRaises(AgentException):
            OllamaProvider().generate(generation_request())

    @patch("tasc_agents.providers.ollama_provider.httpx.post")
    def test_malformed_json_raises_agent_exception(self, post: Mock) -> None:
        response = Mock()
        response.json.side_effect = ValueError("Invalid JSON")
        post.return_value = response

        with self.assertRaises(AgentException):
            OllamaProvider().generate(generation_request())

    def test_provider_can_be_registered_in_core_registry(self) -> None:
        registry = Registry()
        provider = OllamaProvider()

        registry.register(IAgentProvider, provider)

        self.assertIs(registry.resolve(IAgentProvider), provider)


if __name__ == "__main__":
    unittest.main()
