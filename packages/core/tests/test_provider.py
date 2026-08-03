from __future__ import annotations

import sys
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_core.config.provider import ConfigurationProvider
from tasc_core.exceptions import ConfigurationException
from tasc_core.interfaces.configuration import IConfigurationProvider
from tasc_core.models.bootstrap_configuration import BootstrapConfiguration
from tasc_core.models.company_configuration import CompanyConfiguration
from tasc_core.models.core_configuration import CoreConfiguration
from tasc_core.models.logging_configuration import LoggingConfiguration
from tasc_core.models.metadata_configuration import MetadataConfiguration
from tasc_core.models.modules_configuration import ModulesConfiguration
from tasc_core.models.provider_configuration import ProviderConfiguration
from tasc_core.models.runtime_configuration import RuntimeConfiguration


def valid_configuration() -> dict[str, object]:
    return {
        "apiVersion": "tasc.io/v1alpha1",
        "kind": "CoreConfiguration",
        "metadata": {
            "name": "demo",
            "version": "0.1.0",
            "description": "Demo configuration",
        },
        "company": {
            "name": "Demo Company",
            "domain": "example.com",
            "contact_email": "ops@example.com",
        },
        "runtime": {"environment": "development", "version": "0.1.0"},
        "logging": {"level": "INFO", "format": "plain"},
        "modules": {"enabled": ["core"]},
        "providers": {"name": "default", "kind": "placeholder"},
        "bootstrap": {"enabled": True},
    }


class ConfigurationProviderTests(unittest.TestCase):
    def test_valid_configuration_returns_core_configuration(self) -> None:
        configuration = ConfigurationProvider(valid_configuration()).get_configuration()

        self.assertIsInstance(configuration, CoreConfiguration)

    def test_nested_dataclasses_are_created(self) -> None:
        configuration = ConfigurationProvider(valid_configuration()).get_configuration()

        self.assertIsInstance(configuration.metadata, MetadataConfiguration)
        self.assertIsInstance(configuration.company, CompanyConfiguration)
        self.assertIsInstance(configuration.runtime, RuntimeConfiguration)
        self.assertIsInstance(configuration.logging, LoggingConfiguration)
        self.assertIsInstance(configuration.modules, ModulesConfiguration)
        self.assertIsInstance(configuration.provider, ProviderConfiguration)
        self.assertIsInstance(configuration.bootstrap, BootstrapConfiguration)

    def test_values_are_mapped_correctly(self) -> None:
        configuration = ConfigurationProvider(valid_configuration()).get_configuration()

        self.assertEqual(configuration.metadata.name, "demo")
        self.assertEqual(configuration.company.domain, "example.com")
        self.assertEqual(configuration.runtime.environment, "development")
        self.assertEqual(configuration.logging.level, "INFO")
        self.assertEqual(configuration.modules.enabled, ["core"])
        self.assertEqual(configuration.provider.kind, "placeholder")
        self.assertTrue(configuration.bootstrap.enabled)

    def test_returned_configuration_is_immutable(self) -> None:
        configuration = ConfigurationProvider(valid_configuration()).get_configuration()

        with self.assertRaises(FrozenInstanceError):
            configuration.metadata.name = "changed"

    def test_missing_section_raises_configuration_exception(self) -> None:
        configuration = valid_configuration()
        del configuration["providers"]

        with self.assertRaises(ConfigurationException) as context:
            ConfigurationProvider(configuration).get_configuration()

        self.assertEqual(context.exception.error_code, "TASC-CONFIG-0020")

    def test_interface_compliance(self) -> None:
        self.assertTrue(issubclass(ConfigurationProvider, IConfigurationProvider))
        self.assertIsInstance(
            ConfigurationProvider(valid_configuration()),
            IConfigurationProvider,
        )


if __name__ == "__main__":
    unittest.main()
