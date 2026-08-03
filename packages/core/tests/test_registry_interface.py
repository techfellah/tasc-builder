from __future__ import annotations

import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_core.interfaces.registry import IRegistry


class RegistryInterfaceTests(unittest.TestCase):
    def test_registry_interface_is_abstract(self) -> None:
        self.assertTrue(inspect.isabstract(IRegistry))

    def test_registry_interface_cannot_instantiate(self) -> None:
        with self.assertRaises(TypeError):
            IRegistry()

    def test_all_methods_exist(self) -> None:
        self.assertTrue(hasattr(IRegistry, "register"))
        self.assertTrue(hasattr(IRegistry, "resolve"))
        self.assertTrue(hasattr(IRegistry, "contains"))
        self.assertTrue(hasattr(IRegistry, "unregister"))

        self.assertTrue(IRegistry.register.__isabstractmethod__)
        self.assertTrue(IRegistry.resolve.__isabstractmethod__)
        self.assertTrue(IRegistry.contains.__isabstractmethod__)
        self.assertTrue(IRegistry.unregister.__isabstractmethod__)


if __name__ == "__main__":
    unittest.main()
