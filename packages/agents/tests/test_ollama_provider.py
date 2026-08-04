from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "core"))

from tasc_agents.interfaces import IAgentProvider
from tasc_agents.generation.models import GenerationRequest
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

    def test_generate_returns_generation_result_placeholder(self) -> None:
        result = OllamaProvider().generate(generation_request())

        self.assertEqual(result.content, "Provider execution not yet implemented.")
        self.assertEqual(result.provider, "ollama")
        self.assertEqual(result.model, "llama3")
        self.assertEqual(result.usage.input_tokens, 0)
        self.assertEqual(result.usage.output_tokens, 0)
        self.assertEqual(result.usage.total_tokens, 0)

    def test_provider_can_be_registered_in_core_registry(self) -> None:
        registry = Registry()
        provider = OllamaProvider()

        registry.register(IAgentProvider, provider)

        self.assertIs(registry.resolve(IAgentProvider), provider)


if __name__ == "__main__":
    unittest.main()
