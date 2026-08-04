from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "core"))

from tasc_agents.interfaces import IAgentExecutor, IAgentProvider
from tasc_agents.generation.models import GenerationResult, GenerationUsage
from tasc_agents.models import AgentModel
from tasc_agents.prompts.models import RenderedPrompt
from tasc_agents.services import AgentExecutor
from tasc_core.exceptions import RegistryException
from tasc_core.interfaces.registry import IRegistry


class AgentExecutorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = Mock(spec=IRegistry)
        self.provider = Mock(spec=IAgentProvider)
        self.executor = AgentExecutor(self.registry)
        self.agent = Mock()
        self.agent.model = AgentModel(
            provider="ollama",
            model="llama3",
            temperature=0.2,
            max_tokens=1024,
        )
        self.prompt = RenderedPrompt(
            system_prompt="You are helpful.",
            user_prompt="Hello Alice.",
            variables={"name": "Alice"},
        )

    @staticmethod
    def generation_result() -> GenerationResult:
        return GenerationResult(
            content="Generated content.",
            provider="ollama",
            model="llama3",
            usage=GenerationUsage(input_tokens=10, output_tokens=20, total_tokens=30),
            finish_reason="stop",
            duration_ms=100,
            metadata={},
        )

    def test_provider_is_resolved_from_registry(self) -> None:
        self.registry.resolve.return_value = self.provider
        self.provider.generate.return_value = self.generation_result()

        self.executor.execute(self.agent, self.prompt, {})

        self.registry.resolve.assert_called_once_with(IAgentProvider)

    def test_generation_request_is_created_and_passed_to_provider(self) -> None:
        self.registry.resolve.return_value = self.provider
        self.provider.generate.return_value = self.generation_result()
        context = {"project": "demo"}

        self.executor.execute(self.agent, self.prompt, context)

        self.provider.generate.assert_called_once()
        request = self.provider.generate.call_args.args[0]
        self.assertEqual(request.prompt, self.prompt)
        self.assertEqual(request.model, self.agent.model)
        self.assertEqual(request.metadata, context)

    def test_generation_result_is_returned_unchanged(self) -> None:
        self.registry.resolve.return_value = self.provider
        expected = self.generation_result()
        self.provider.generate.return_value = expected

        result = self.executor.execute(self.agent, self.prompt, {})

        self.assertIs(result, expected)

    def test_missing_provider_is_propagated(self) -> None:
        self.registry.resolve.side_effect = RegistryException(
            "Unknown contract",
            "TASC-REGISTRY-0001",
        )

        with self.assertRaises(RegistryException):
            self.executor.execute(self.agent, self.prompt, {})

    def test_interface_compliance(self) -> None:
        self.assertTrue(issubclass(AgentExecutor, IAgentExecutor))
        self.assertIsInstance(self.executor, IAgentExecutor)


if __name__ == "__main__":
    unittest.main()
