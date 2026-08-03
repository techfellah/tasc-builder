from __future__ import annotations

from collections.abc import Mapping

import yaml

from tasc_core.exceptions import ConfigurationException
from tasc_core.interfaces.configuration import IConfigurationParser


class ConfigurationParser(IConfigurationParser):
    """Parse YAML configuration documents into mappings."""

    def parse(self, text: str) -> Mapping[str, object]:
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise ConfigurationException(
                "Invalid YAML",
                "TASC-CONFIG-0010",
            ) from exc

        if not isinstance(data, Mapping):
            raise ConfigurationException(
                "Root document must be a mapping",
                "TASC-CONFIG-0011",
            )

        return data
