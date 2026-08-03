from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "core"))

from tasc_agents.interfaces import IAgentProvider
from tasc_agents.providers import OllamaProvider
from tasc_core.registry.registry import Registry


class OllamaProviderTests(unittest.TestCase):
    def test_interface_compliance(self) -> None:
        self.assertTrue(issubclass(OllamaProvider, IAgentProvider))
        self.assertIsInstance(OllamaProvider(), IAgentProvider)

    def test_generate_returns_placeholder(self) -> None:
        result = OllamaProvider().generate(None, "prompt", {})

        self.assertEqual(result, "Provider execution not yet implemented.")

    def test_provider_can_be_registered_in_core_registry(self) -> None:
        registry = Registry()
        provider = OllamaProvider()

        registry.register(IAgentProvider, provider)

        self.assertIs(registry.resolve(IAgentProvider), provider)


if __name__ == "__main__":
    unittest.main()
