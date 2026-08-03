from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_core.exceptions import RegistryException
from tasc_core.interfaces.registry import IRegistry
from tasc_core.registry.registry import Registry


class RegistryTests(unittest.TestCase):
    def test_register_and_resolve(self) -> None:
        registry = Registry()
        service = object()

        registry.register(type(service), service)

        self.assertTrue(registry.contains(type(service)))
        self.assertIs(registry.resolve(type(service)), service)

    def test_unregister(self) -> None:
        registry = Registry()
        contract = str
        instance = "value"

        registry.register(contract, instance)
        registry.unregister(contract)

        self.assertFalse(registry.contains(contract))

    def test_duplicate_registration_raises_registry_exception(self) -> None:
        registry = Registry()
        contract = int

        registry.register(contract, 1)

        with self.assertRaises(RegistryException):
            registry.register(contract, 2)

    def test_missing_registration_raises_registry_exception(self) -> None:
        registry = Registry()

        with self.assertRaises(RegistryException):
            registry.resolve(str)

        with self.assertRaises(RegistryException):
            registry.unregister(str)

    def test_interface_compliance(self) -> None:
        self.assertTrue(issubclass(Registry, IRegistry))

    def test_type_inference_where_practical(self) -> None:
        registry = Registry()
        contract = int
        instance = 9

        registry.register(contract, instance)
        resolved = registry.resolve(contract)

        self.assertIsInstance(resolved, contract)


if __name__ == "__main__":
    unittest.main()
