from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "core"))

from tasc_agents.interfaces import IAgentExecutor, IAgentProvider
from tasc_agents.services import AgentExecutor
from tasc_core.exceptions import RegistryException
from tasc_core.interfaces.registry import IRegistry


class AgentExecutorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = Mock(spec=IRegistry)
        self.provider = Mock(spec=IAgentProvider)
        self.executor = AgentExecutor(self.registry)
        self.agent = Mock()
        self.agent.model.provider = "ollama"

    def test_provider_is_resolved_from_registry(self) -> None:
        self.registry.resolve.return_value = self.provider
        self.provider.generate.return_value = "result"

        self.executor.execute(self.agent, "prompt", {})

        self.registry.resolve.assert_called_once_with(IAgentProvider)

    def test_provider_generate_is_called_and_result_is_returned(self) -> None:
        self.registry.resolve.return_value = self.provider
        self.provider.generate.return_value = "result"
        context = {"project": "demo"}

        result = self.executor.execute(self.agent, "prompt", context)

        self.assertEqual(result, "result")
        self.provider.generate.assert_called_once_with(self.agent, "prompt", context)

    def test_missing_provider_is_propagated(self) -> None:
        self.registry.resolve.side_effect = RegistryException(
            "Unknown contract",
            "TASC-REGISTRY-0001",
        )

        with self.assertRaises(RegistryException):
            self.executor.execute(self.agent, "prompt", {})

    def test_interface_compliance(self) -> None:
        self.assertTrue(issubclass(AgentExecutor, IAgentExecutor))
        self.assertIsInstance(self.executor, IAgentExecutor)


if __name__ == "__main__":
    unittest.main()
