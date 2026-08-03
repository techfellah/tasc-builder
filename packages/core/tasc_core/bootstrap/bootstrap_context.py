from __future__ import annotations

from dataclasses import dataclass

from tasc_core.context.runtime_context import RuntimeContext
from tasc_core.logging.factory import LoggerFactory
from tasc_core.models.core_configuration import CoreConfiguration
from tasc_core.registry.registry import Registry


@dataclass(frozen=True)
class BootstrapContext:
    """Core services initialized during bootstrap."""

    configuration: CoreConfiguration
    runtime_context: RuntimeContext
    registry: Registry
    logger_factory: LoggerFactory
