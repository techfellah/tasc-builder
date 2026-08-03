from __future__ import annotations

from dataclasses import dataclass

from .bootstrap_configuration import BootstrapConfiguration
from .company_configuration import CompanyConfiguration
from .logging_configuration import LoggingConfiguration
from .metadata_configuration import MetadataConfiguration
from .modules_configuration import ModulesConfiguration
from .provider_configuration import ProviderConfiguration
from .runtime_configuration import RuntimeConfiguration


@dataclass(frozen=True)
class CoreConfiguration:
    metadata: MetadataConfiguration
    company: CompanyConfiguration
    runtime: RuntimeConfiguration
    logging: LoggingConfiguration
    modules: ModulesConfiguration
    provider: ProviderConfiguration
    bootstrap: BootstrapConfiguration

    def to_dict(self) -> dict[str, object]:
        return {
            "metadata": self.metadata.to_dict(),
            "company": self.company.to_dict(),
            "runtime": self.runtime.to_dict(),
            "logging": self.logging.to_dict(),
            "modules": self.modules.to_dict(),
            "provider": self.provider.to_dict(),
            "bootstrap": self.bootstrap.to_dict(),
        }
