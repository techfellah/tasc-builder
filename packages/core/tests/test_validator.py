from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_core.config.validator import ConfigurationValidator
from tasc_core.exceptions import ValidationException
from tasc_core.interfaces.configuration import IConfigurationValidator


def valid_configuration() -> dict[str, object]:
    return {
        "apiVersion": "tasc.io/v1alpha1",
        "kind": "CoreConfiguration",
        "metadata": {"name": "demo"},
        "company": {"name": "Demo Company"},
        "runtime": {"environment": "development"},
        "logging": {"level": "INFO", "console": True, "file": False},
        "modules": {},
        "providers": {},
        "bootstrap": {},
    }


class ConfigurationValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = ConfigurationValidator()

    def test_valid_configuration(self) -> None:
        configuration = valid_configuration()

        self.assertIsNone(self.validator.validate(configuration))

    def test_missing_required_section_raises_validation_exception(self) -> None:
        configuration = valid_configuration()
        del configuration["bootstrap"]

        with self.assertRaises(ValidationException) as context:
            self.validator.validate(configuration)

        self.assertEqual(context.exception.error_code, "TASC-VALIDATION-0001")

    def test_unknown_section_raises_validation_exception(self) -> None:
        configuration = valid_configuration()
        configuration["unknown"] = {}

        with self.assertRaises(ValidationException) as context:
            self.validator.validate(configuration)

        self.assertEqual(context.exception.error_code, "TASC-VALIDATION-0002")

    def test_missing_nested_field_raises_validation_exception(self) -> None:
        configuration = valid_configuration()
        configuration["metadata"] = {}

        with self.assertRaises(ValidationException) as context:
            self.validator.validate(configuration)

        self.assertEqual(context.exception.error_code, "TASC-VALIDATION-0003")

    def test_invalid_mapping_type_raises_validation_exception(self) -> None:
        configuration = valid_configuration()
        configuration["providers"] = []

        with self.assertRaises(ValidationException) as context:
            self.validator.validate(configuration)

        self.assertEqual(context.exception.error_code, "TASC-VALIDATION-0004")

    def test_invalid_boolean_type_raises_validation_exception(self) -> None:
        configuration = valid_configuration()
        configuration["logging"] = {"level": "INFO", "console": "true"}

        with self.assertRaises(ValidationException) as context:
            self.validator.validate(configuration)

        self.assertEqual(context.exception.error_code, "TASC-VALIDATION-0004")

    def test_interface_compliance(self) -> None:
        self.assertTrue(issubclass(ConfigurationValidator, IConfigurationValidator))
        self.assertIsInstance(self.validator, IConfigurationValidator)


if __name__ == "__main__":
    unittest.main()
