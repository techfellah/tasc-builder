from __future__ import annotations

import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_core.interfaces.logger import ILogger, ILoggerFactory


class LoggingInterfaceTests(unittest.TestCase):
    def test_interfaces_are_abstract(self) -> None:
        self.assertTrue(inspect.isabstract(ILogger))
        self.assertTrue(inspect.isabstract(ILoggerFactory))

    def test_interfaces_cannot_instantiate(self) -> None:
        with self.assertRaises(TypeError):
            ILogger()

        with self.assertRaises(TypeError):
            ILoggerFactory()

    def test_method_signatures_exist(self) -> None:
        self.assertTrue(hasattr(ILogger, "debug"))
        self.assertTrue(hasattr(ILogger, "info"))
        self.assertTrue(hasattr(ILogger, "warning"))
        self.assertTrue(hasattr(ILogger, "error"))
        self.assertTrue(hasattr(ILogger, "critical"))
        self.assertTrue(hasattr(ILogger, "exception"))
        self.assertTrue(hasattr(ILoggerFactory, "create_logger"))

        self.assertEqual(
            list(inspect.signature(ILogger.debug).parameters.keys()),
            ["self", "message", "context"],
        )
        self.assertEqual(
            list(inspect.signature(ILogger.info).parameters.keys()),
            ["self", "message", "context"],
        )
        self.assertEqual(
            list(inspect.signature(ILogger.warning).parameters.keys()),
            ["self", "message", "context"],
        )
        self.assertEqual(
            list(inspect.signature(ILogger.error).parameters.keys()),
            ["self", "message", "context"],
        )
        self.assertEqual(
            list(inspect.signature(ILogger.critical).parameters.keys()),
            ["self", "message", "context"],
        )
        self.assertEqual(
            list(inspect.signature(ILogger.exception).parameters.keys()),
            ["self", "message", "exception", "context"],
        )
        self.assertEqual(
            list(inspect.signature(ILoggerFactory.create_logger).parameters.keys()),
            ["self", "name"],
        )


if __name__ == "__main__":
    unittest.main()
