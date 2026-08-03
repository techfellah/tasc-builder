from __future__ import annotations

import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_core.interfaces.configuration import (
    IConfigurationLoader,
    IConfigurationParser,
    IConfigurationProvider,
    IConfigurationValidator,
)


class ConfigurationInterfaceTests(unittest.TestCase):
    def test_interfaces_are_abstract(self) -> None:
        self.assertTrue(inspect.isabstract(IConfigurationLoader))
        self.assertTrue(inspect.isabstract(IConfigurationParser))
        self.assertTrue(inspect.isabstract(IConfigurationValidator))
        self.assertTrue(inspect.isabstract(IConfigurationProvider))

    def test_interfaces_cannot_instantiate(self) -> None:
        with self.assertRaises(TypeError):
            IConfigurationLoader()

        with self.assertRaises(TypeError):
            IConfigurationParser()

        with self.assertRaises(TypeError):
            IConfigurationValidator()

        with self.assertRaises(TypeError):
            IConfigurationProvider()

    def test_methods_exist(self) -> None:
        self.assertTrue(hasattr(IConfigurationLoader, "load"))
        self.assertTrue(hasattr(IConfigurationParser, "parse"))
        self.assertTrue(hasattr(IConfigurationValidator, "validate"))
        self.assertTrue(hasattr(IConfigurationProvider, "get_configuration"))

        self.assertTrue(IConfigurationLoader.load.__isabstractmethod__)
        self.assertTrue(IConfigurationParser.parse.__isabstractmethod__)
        self.assertTrue(IConfigurationValidator.validate.__isabstractmethod__)
        self.assertTrue(IConfigurationProvider.get_configuration.__isabstractmethod__)


if __name__ == "__main__":
    unittest.main()
