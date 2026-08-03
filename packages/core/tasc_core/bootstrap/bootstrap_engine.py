from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from tasc_core.bootstrap.bootstrap_context import BootstrapContext
from tasc_core.config.loader import ConfigurationLoader
from tasc_core.config.parser import ConfigurationParser
from tasc_core.config.provider import ConfigurationProvider
from tasc_core.config.validator import ConfigurationValidator
from tasc_core.context.runtime_context import RuntimeContext
from tasc_core.exceptions import BootstrapException
from tasc_core.logging.factory import LoggerFactory
from tasc_core.models.core_configuration import CoreConfiguration
from tasc_core.registry.registry import Registry


class BootstrapEngine:
    """Initialize the Core services from a configuration file."""

    def bootstrap(self, configuration_path: Path) -> BootstrapContext:
        try:
            text = ConfigurationLoader().load(configuration_path)
            configuration_data = ConfigurationParser().parse(text)
            ConfigurationValidator().validate(configuration_data)
            configuration = ConfigurationProvider(
                configuration_data
            ).get_configuration()

            registry = Registry()
            logger_factory = LoggerFactory()
            runtime_context = RuntimeContext(
                configuration=configuration,
                logger_factory=logger_factory,
                registry=registry,
                environment=configuration.runtime.environment,
                version=configuration.runtime.version,
                started_at=datetime.now(timezone.utc),
            )
            registry.register(CoreConfiguration, configuration)
            registry.register(RuntimeContext, runtime_context)
            registry.register(LoggerFactory, logger_factory)

            return BootstrapContext(
                configuration=configuration,
                runtime_context=runtime_context,
                registry=registry,
                logger_factory=logger_factory,
            )
        except BootstrapException:
            raise
        except Exception as exc:
            raise BootstrapException(
                "Bootstrap failed",
                "TASC-BOOTSTRAP-0001",
                cause=exc,
            ) from exc
