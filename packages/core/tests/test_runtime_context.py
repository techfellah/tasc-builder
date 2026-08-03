from __future__ import annotations

import sys
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_core.context.runtime_context import RuntimeContext
from tasc_core.interfaces.runtime_context import IRuntimeContext
from tasc_core.interfaces.logger import ILoggerFactory


class RuntimeContextTests(unittest.TestCase):
    def test_construction(self) -> None:
        started_at = datetime(2026, 8, 3, 12, 0, tzinfo=timezone.utc)
        configuration = {"name": "demo"}
        logger_factory = DummyLoggerFactory()
        registry = {"service": "core"}

        context = RuntimeContext(
            configuration=configuration,
            logger_factory=logger_factory,
            registry=registry,
            environment="test",
            version="1.0.0",
            started_at=started_at,
        )

        self.assertEqual(context.configuration, configuration)
        self.assertIs(context.logger_factory, logger_factory)
        self.assertEqual(context.registry, registry)
        self.assertEqual(context.environment, "test")
        self.assertEqual(context.version, "1.0.0")
        self.assertEqual(context.started_at, started_at)

    def test_immutability(self) -> None:
        context = RuntimeContext(
            configuration={"name": "demo"},
            logger_factory=DummyLoggerFactory(),
            registry={"service": "core"},
            environment="test",
            version="1.0.0",
            started_at=datetime.now(timezone.utc),
        )

        with self.assertRaises(FrozenInstanceError):
            context.version = "2.0.0"

    def test_interface_compliance(self) -> None:
        self.assertTrue(issubclass(RuntimeContext, IRuntimeContext))

    def test_property_values(self) -> None:
        started_at = datetime(2026, 8, 3, 12, 0, tzinfo=timezone.utc)
        configuration = {"name": "demo"}
        logger_factory = DummyLoggerFactory()
        registry = {"service": "core"}

        context = RuntimeContext(
            configuration=configuration,
            logger_factory=logger_factory,
            registry=registry,
            environment="test",
            version="1.0.0",
            started_at=started_at,
        )

        self.assertEqual(context.configuration, configuration)
        self.assertEqual(context.logger_factory, logger_factory)
        self.assertEqual(context.registry, registry)
        self.assertEqual(context.environment, "test")
        self.assertEqual(context.version, "1.0.0")
        self.assertEqual(context.started_at, started_at)


class DummyLoggerFactory(ILoggerFactory):
    def create_logger(self, name: str):
        raise NotImplementedError


if __name__ == "__main__":
    unittest.main()
