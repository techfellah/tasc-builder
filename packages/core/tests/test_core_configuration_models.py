from __future__ import annotations

import sys
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_core.models.bootstrap_configuration import BootstrapConfiguration
from tasc_core.models.company_configuration import CompanyConfiguration
from tasc_core.models.core_configuration import CoreConfiguration
from tasc_core.models.logging_configuration import LoggingConfiguration
from tasc_core.models.metadata_configuration import MetadataConfiguration
from tasc_core.models.modules_configuration import ModulesConfiguration
from tasc_core.models.provider_configuration import ProviderConfiguration
from tasc_core.models.runtime_configuration import RuntimeConfiguration


class CoreConfigurationModelsTests(unittest.TestCase):
    def test_construction(self) -> None:
        metadata = MetadataConfiguration(name="Demo", version="1.0", description="demo")
        company = CompanyConfiguration(name="Acme", domain="acme.test", contact_email="ops@acme.test")
        runtime = RuntimeConfiguration(environment="test", version="1.0")
        logging = LoggingConfiguration(level="INFO", format="plain")
        modules = ModulesConfiguration(enabled=["core", "agents"])
        provider = ProviderConfiguration(name="native", kind="local")
        bootstrap = BootstrapConfiguration(enabled=True)

        config = CoreConfiguration(
            metadata=metadata,
            company=company,
            runtime=runtime,
            logging=logging,
            modules=modules,
            provider=provider,
            bootstrap=bootstrap,
        )

        self.assertEqual(config.metadata, metadata)
        self.assertEqual(config.company, company)
        self.assertEqual(config.runtime, runtime)
        self.assertEqual(config.logging, logging)
        self.assertEqual(config.modules, modules)
        self.assertEqual(config.provider, provider)
        self.assertEqual(config.bootstrap, bootstrap)

    def test_immutability(self) -> None:
        metadata = MetadataConfiguration(name="Demo", version="1.0")
        company = CompanyConfiguration(name="Acme")
        runtime = RuntimeConfiguration(environment="test", version="1.0")
        logging = LoggingConfiguration(level="INFO")
        modules = ModulesConfiguration(enabled=["core"])
        provider = ProviderConfiguration(name="native", kind="local")
        bootstrap = BootstrapConfiguration(enabled=True)
        config = CoreConfiguration(
            metadata=metadata,
            company=company,
            runtime=runtime,
            logging=logging,
            modules=modules,
            provider=provider,
            bootstrap=bootstrap,
        )

        with self.assertRaises(FrozenInstanceError):
            config.version = "2.0"

    def test_equality(self) -> None:
        left = CoreConfiguration(
            metadata=MetadataConfiguration(name="Demo", version="1.0"),
            company=CompanyConfiguration(name="Acme"),
            runtime=RuntimeConfiguration(environment="test", version="1.0"),
            logging=LoggingConfiguration(level="INFO"),
            modules=ModulesConfiguration(enabled=["core"]),
            provider=ProviderConfiguration(name="native", kind="local"),
            bootstrap=BootstrapConfiguration(enabled=True),
        )
        right = CoreConfiguration(
            metadata=MetadataConfiguration(name="Demo", version="1.0"),
            company=CompanyConfiguration(name="Acme"),
            runtime=RuntimeConfiguration(environment="test", version="1.0"),
            logging=LoggingConfiguration(level="INFO"),
            modules=ModulesConfiguration(enabled=["core"]),
            provider=ProviderConfiguration(name="native", kind="local"),
            bootstrap=BootstrapConfiguration(enabled=True),
        )

        self.assertEqual(left, right)

    def test_nested_composition(self) -> None:
        config = CoreConfiguration(
            metadata=MetadataConfiguration(name="Demo", version="1.0"),
            company=CompanyConfiguration(name="Acme"),
            runtime=RuntimeConfiguration(environment="test", version="1.0"),
            logging=LoggingConfiguration(level="INFO"),
            modules=ModulesConfiguration(enabled=["core"]),
            provider=ProviderConfiguration(name="native", kind="local"),
            bootstrap=BootstrapConfiguration(enabled=True),
        )

        self.assertEqual(config.metadata.name, "Demo")
        self.assertEqual(config.company.name, "Acme")
        self.assertEqual(config.runtime.environment, "test")
        self.assertEqual(config.logging.level, "INFO")
        self.assertEqual(config.modules.enabled, ["core"])
        self.assertEqual(config.provider.kind, "local")
        self.assertTrue(config.bootstrap.enabled)

    def test_to_dict(self) -> None:
        config = CoreConfiguration(
            metadata=MetadataConfiguration(name="Demo", version="1.0"),
            company=CompanyConfiguration(name="Acme"),
            runtime=RuntimeConfiguration(environment="test", version="1.0"),
            logging=LoggingConfiguration(level="INFO"),
            modules=ModulesConfiguration(enabled=["core"]),
            provider=ProviderConfiguration(name="native", kind="local"),
            bootstrap=BootstrapConfiguration(enabled=True),
        )

        self.assertEqual(
            config.to_dict(),
            {
                "metadata": {"name": "Demo", "version": "1.0", "description": None},
                "company": {"name": "Acme", "domain": None, "contact_email": None},
                "runtime": {"environment": "test", "version": "1.0"},
                "logging": {"level": "INFO", "format": None},
                "modules": {"enabled": ["core"]},
                "provider": {"name": "native", "kind": "local"},
                "bootstrap": {"enabled": True},
            },
        )


if __name__ == "__main__":
    unittest.main()
