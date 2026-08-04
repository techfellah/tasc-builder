from __future__ import annotations

import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_agents.prompts.interfaces import IPromptRepository, IPromptService


class PromptInterfaceTests(unittest.TestCase):
    def test_interfaces_are_abstract(self) -> None:
        self.assertTrue(inspect.isabstract(IPromptRepository))
        self.assertTrue(inspect.isabstract(IPromptService))

    def test_interfaces_cannot_be_instantiated(self) -> None:
        for interface in (IPromptRepository, IPromptService):
            with self.assertRaises(TypeError):
                interface()

    def test_repository_methods_exist(self) -> None:
        for method in ("get", "list", "exists"):
            self.assertTrue(hasattr(IPromptRepository, method))
            self.assertTrue(getattr(IPromptRepository, method).__isabstractmethod__)

    def test_service_methods_exist(self) -> None:
        self.assertTrue(hasattr(IPromptService, "render"))
        self.assertTrue(IPromptService.render.__isabstractmethod__)


if __name__ == "__main__":
    unittest.main()
