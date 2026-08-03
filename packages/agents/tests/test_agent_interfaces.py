from __future__ import annotations

import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_agents.interfaces import (
    IAgentExecutor,
    IAgentProvider,
    IAgentRepository,
    IAGentService,
)


class AgentInterfaceTests(unittest.TestCase):
    def test_interfaces_are_abstract(self) -> None:
        self.assertTrue(inspect.isabstract(IAgentRepository))
        self.assertTrue(inspect.isabstract(IAgentProvider))
        self.assertTrue(inspect.isabstract(IAgentExecutor))
        self.assertTrue(inspect.isabstract(IAGentService))

    def test_interfaces_cannot_be_instantiated(self) -> None:
        for interface in (
            IAgentRepository,
            IAgentProvider,
            IAgentExecutor,
            IAGentService,
        ):
            with self.assertRaises(TypeError):
                interface()

    def test_repository_methods_exist(self) -> None:
        for method in ("create", "get", "list", "exists", "delete"):
            self.assertTrue(hasattr(IAgentRepository, method))
            self.assertTrue(getattr(IAgentRepository, method).__isabstractmethod__)

    def test_provider_methods_exist(self) -> None:
        self.assertTrue(hasattr(IAgentProvider, "generate"))
        self.assertTrue(IAgentProvider.generate.__isabstractmethod__)

    def test_executor_methods_exist(self) -> None:
        self.assertTrue(hasattr(IAgentExecutor, "execute"))
        self.assertTrue(IAgentExecutor.execute.__isabstractmethod__)

    def test_service_methods_exist(self) -> None:
        for method in (
            "create_agent",
            "get_agent",
            "list_agents",
            "delete_agent",
            "execute",
        ):
            self.assertTrue(hasattr(IAGentService, method))
            self.assertTrue(getattr(IAGentService, method).__isabstractmethod__)


if __name__ == "__main__":
    unittest.main()
