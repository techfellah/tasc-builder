from __future__ import annotations

from pathlib import Path

from tasc_core.exceptions import ConfigurationException
from tasc_core.interfaces.configuration import IConfigurationLoader


class ConfigurationLoader(IConfigurationLoader):
    def load(self, path: Path) -> str:
        if not path.exists():
            raise ConfigurationException(
                "File not found",
                "TASC-CONFIG-0001",
                details={"path": str(path)},
            )
        if not path.is_file():
            raise ConfigurationException(
                "Invalid file path",
                "TASC-CONFIG-0002",
                details={"path": str(path)},
            )
        try:
            return path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ConfigurationException(
                "Read failure",
                "TASC-CONFIG-0003",
                details={"path": str(path)},
            ) from exc
