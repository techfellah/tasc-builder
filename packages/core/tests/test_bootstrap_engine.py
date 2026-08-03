from __future__ import annotations

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_core.bootstrap import BootstrapContext, BootstrapEngine
from tasc_core.context.runtime_context import RuntimeContext
from tasc_core.exceptions import BootstrapException, ConfigurationException
from tasc_core.logging.factory import LoggerFactory
from tasc_core.models.core_configuration import CoreConfiguration


def valid_configuration_yaml() -> str:
    return """\
apiVersion: tasc.io/v1alpha1
kind: CoreConfiguration
metadata:
  name: demo
  version: 0.1.0
company:
  name: Demo Company
runtime:
  environment: development
  version: 0.1.0
logging:
  level: INFO
modules:
  enabled:
    - core
providers:
  name: default
  kind: placeholder
bootstrap:
  enabled: true
"""


class BootstrapEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = BootstrapEngine()

    def test_successful_bootstrap_populates_context(self) -> None:
        with TemporaryDirectory() as temp_dir:
            configuration_path = Path(temp_dir) / "core.yaml"
            configuration_path.write_text(valid_configuration_yaml(), encoding="utf-8")

            context = self.engine.bootstrap(configuration_path)

        self.assertIsInstance(context, BootstrapContext)
        self.assertEqual(context.configuration.metadata.name, "demo")

    def test_registry_is_populated(self) -> None:
        with TemporaryDirectory() as temp_dir:
            configuration_path = Path(temp_dir) / "core.yaml"
            configuration_path.write_text(valid_configuration_yaml(), encoding="utf-8")

            context = self.engine.bootstrap(configuration_path)

        self.assertIs(context.registry.resolve(CoreConfiguration), context.configuration)
        self.assertIs(context.registry.resolve(RuntimeContext), context.runtime_context)
        self.assertIs(context.registry.resolve(LoggerFactory), context.logger_factory)

    def test_runtime_context_is_created(self) -> None:
        with TemporaryDirectory() as temp_dir:
            configuration_path = Path(temp_dir) / "core.yaml"
            configuration_path.write_text(valid_configuration_yaml(), encoding="utf-8")

            context = self.engine.bootstrap(configuration_path)

        self.assertIsInstance(context.runtime_context, RuntimeContext)
        self.assertIs(context.runtime_context.configuration, context.configuration)

    def test_missing_configuration_raises_bootstrap_exception(self) -> None:
        missing_path = Path("/tmp/tasc-missing-core-configuration.yaml")

        with self.assertRaises(BootstrapException) as context:
            self.engine.bootstrap(missing_path)

        self.assertEqual(context.exception.error_code, "TASC-BOOTSTRAP-0001")
        self.assertIsInstance(context.exception.cause, ConfigurationException)

    def test_invalid_configuration_raises_bootstrap_exception(self) -> None:
        with TemporaryDirectory() as temp_dir:
            configuration_path = Path(temp_dir) / "core.yaml"
            configuration_path.write_text("apiVersion: tasc.io/v1alpha1\n", encoding="utf-8")

            with self.assertRaises(BootstrapException) as context:
                self.engine.bootstrap(configuration_path)

        self.assertEqual(context.exception.error_code, "TASC-BOOTSTRAP-0001")

    def test_unexpected_failure_is_wrapped(self) -> None:
        with TemporaryDirectory() as temp_dir:
            configuration_path = Path(temp_dir) / "core.yaml"
            configuration_path.write_text(valid_configuration_yaml(), encoding="utf-8")

            with self.assertRaises(BootstrapException) as context:
                self.engine.bootstrap(configuration_path.parent)

        self.assertEqual(context.exception.error_code, "TASC-BOOTSTRAP-0001")


if __name__ == "__main__":
    unittest.main()
