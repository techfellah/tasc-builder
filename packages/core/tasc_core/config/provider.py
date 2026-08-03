from __future__ import annotations

from collections.abc import Mapping

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


class ConfigurationProvider(IConfigurationProvider):
    """Convert validated configuration mappings into Core configuration models."""

    def __init__(self, configuration: Mapping[str, object]) -> None:
        self._configuration = configuration

    def get_configuration(self) -> CoreConfiguration:
        try:
            return CoreConfiguration(
                metadata=MetadataConfiguration(**self._section("metadata")),
                company=CompanyConfiguration(**self._section("company")),
                runtime=RuntimeConfiguration(**self._section("runtime")),
                logging=LoggingConfiguration(**self._section("logging")),
                modules=ModulesConfiguration(**self._section("modules")),
                provider=ProviderConfiguration(**self._section("providers")),
                bootstrap=BootstrapConfiguration(**self._section("bootstrap")),
            )
        except (KeyError, TypeError) as exc:
            raise ConfigurationException(
                "Configuration conversion failed",
                "TASC-CONFIG-0020",
            ) from exc

    def _section(self, name: str) -> Mapping[str, object]:
        section = self._configuration[name]
        if not isinstance(section, Mapping):
            raise TypeError(f"Section must be a mapping: {name}")
        return section
