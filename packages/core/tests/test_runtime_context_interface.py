from __future__ import annotations

import inspect
import sys
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_core.interfaces.runtime_context import IRuntimeContext


class RuntimeContextInterfaceTests(unittest.TestCase):
    def test_runtime_context_cannot_instantiate(self) -> None:
        with self.assertRaises(TypeError):
            IRuntimeContext()

    def test_required_properties_exist(self) -> None:
        self.assertTrue(hasattr(IRuntimeContext, "configuration"))
        self.assertTrue(hasattr(IRuntimeContext, "logger_factory"))
        self.assertTrue(hasattr(IRuntimeContext, "registry"))
        self.assertTrue(hasattr(IRuntimeContext, "environment"))
        self.assertTrue(hasattr(IRuntimeContext, "version"))
        self.assertTrue(hasattr(IRuntimeContext, "started_at"))

    def test_all_properties_are_abstract(self) -> None:
        self.assertTrue(inspect.isabstract(IRuntimeContext))
        self.assertTrue(hasattr(IRuntimeContext.configuration, "fget"))
        self.assertTrue(hasattr(IRuntimeContext.logger_factory, "fget"))
        self.assertTrue(hasattr(IRuntimeContext.registry, "fget"))
        self.assertTrue(hasattr(IRuntimeContext.environment, "fget"))
        self.assertTrue(hasattr(IRuntimeContext.version, "fget"))
        self.assertTrue(hasattr(IRuntimeContext.started_at, "fget"))
        self.assertTrue(IRuntimeContext.configuration.fget.__isabstractmethod__)
        self.assertTrue(IRuntimeContext.logger_factory.fget.__isabstractmethod__)
        self.assertTrue(IRuntimeContext.registry.fget.__isabstractmethod__)
        self.assertTrue(IRuntimeContext.environment.fget.__isabstractmethod__)
        self.assertTrue(IRuntimeContext.version.fget.__isabstractmethod__)
        self.assertTrue(IRuntimeContext.started_at.fget.__isabstractmethod__)


if __name__ == "__main__":
    unittest.main()
