from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_core.config.parser import ConfigurationParser
from tasc_core.exceptions import ConfigurationException
from tasc_core.interfaces.configuration import IConfigurationParser


class ConfigurationParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = ConfigurationParser()

    def test_parses_valid_yaml(self) -> None:
        data = self.parser.parse("name: Tāsc\nenabled: true\n")

        self.assertEqual(data, {"name": "Tāsc", "enabled": True})

    def test_invalid_yaml_raises_configuration_exception(self) -> None:
        with self.assertRaises(ConfigurationException) as context:
            self.parser.parse("name: [unclosed")

        self.assertEqual(context.exception.error_code, "TASC-CONFIG-0010")

    def test_non_mapping_root_raises_configuration_exception(self) -> None:
        with self.assertRaises(ConfigurationException) as context:
            self.parser.parse("- first\n- second\n")

        self.assertEqual(context.exception.error_code, "TASC-CONFIG-0011")

    def test_parses_nested_mappings(self) -> None:
        data = self.parser.parse("service:\n  logging:\n    level: INFO\n")

        self.assertEqual(data, {"service": {"logging": {"level": "INFO"}}})

    def test_interface_compliance(self) -> None:
        self.assertTrue(issubclass(ConfigurationParser, IConfigurationParser))


if __name__ == "__main__":
    unittest.main()
