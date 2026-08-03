from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_core.exceptions import (
    BootstrapException,
    ConfigurationException,
    ContextException,
    CoreException,
    EventException,
    RegistryException,
    TASCException,
    ValidationException,
)


class TASCExceptionTests(unittest.TestCase):
    def test_inheritance_hierarchy(self) -> None:
        self.assertTrue(issubclass(CoreException, TASCException))
        self.assertTrue(issubclass(BootstrapException, CoreException))
        self.assertTrue(issubclass(ConfigurationException, CoreException))
        self.assertTrue(issubclass(RegistryException, CoreException))
        self.assertTrue(issubclass(ValidationException, CoreException))
        self.assertTrue(issubclass(ContextException, CoreException))
        self.assertTrue(issubclass(EventException, CoreException))

    def test_constructor_and_public_fields(self) -> None:
        details = {"field": "enabled"}
        cause = ValueError("root cause")
        error = ConfigurationException(
            "Invalid configuration",
            "TASC-CONFIG-0001",
            details=details,
            cause=cause,
        )

        self.assertEqual(error.message, "Invalid configuration")
        self.assertEqual(error.error_code, "TASC-CONFIG-0001")
        self.assertEqual(error.details, details)
        self.assertIs(error.cause, cause)

    def test_error_code_required(self) -> None:
        with self.assertRaises(TypeError):
            ConfigurationException("Invalid configuration")

    def test_message_and_details_preserved(self) -> None:
        details = {"scope": "core"}
        error = ValidationException("Invalid payload", "TASC-VALIDATION-0001", details=details)

        self.assertEqual(error.message, "Invalid payload")
        self.assertEqual(error.details, details)

    def test_cause_preserved(self) -> None:
        cause = RuntimeError("nested")
        error = RegistryException("Registry error", "TASC-REGISTRY-0001", cause=cause)

        self.assertIs(error.cause, cause)

    def test_to_dict_contract(self) -> None:
        error = ConfigurationException(
            "Invalid configuration",
            "TASC-CONFIG-0001",
            details={"section": "app"},
            cause=ValueError("root cause"),
        )

        self.assertEqual(
            error.to_dict(),
            {
                "error_code": "TASC-CONFIG-0001",
                "message": "Invalid configuration",
                "details": {"section": "app"},
                "cause": "root cause",
                "exception": "ConfigurationException",
            },
        )

    def test_str_contract(self) -> None:
        error = ConfigurationException("Invalid configuration", "TASC-CONFIG-0001")

        self.assertEqual(str(error), "[TASC-CONFIG-0001] Invalid configuration")

    def test_repr_contract(self) -> None:
        error = ConfigurationException("Invalid configuration", "TASC-CONFIG-0001")

        self.assertEqual(
            repr(error),
            "ConfigurationException(error_code='TASC-CONFIG-0001', message='Invalid configuration')",
        )

    def test_object_is_immutable(self) -> None:
        error = EventException("Event rejected", "TASC-EVENT-0001")

        with self.assertRaises(AttributeError):
            error.message = "changed"


if __name__ == "__main__":
    unittest.main()
