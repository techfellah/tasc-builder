from __future__ import annotations

from collections.abc import Mapping

from tasc_core.exceptions import ValidationException
from tasc_core.interfaces.configuration import IConfigurationValidator


class ConfigurationValidator(IConfigurationValidator):
    """Validate the top-level structure of a TASC configuration."""

    _required_sections = frozenset(
        {
            "apiVersion",
            "kind",
            "metadata",
            "company",
            "runtime",
            "logging",
            "modules",
            "providers",
            "bootstrap",
        }
    )
    _mapping_sections = frozenset(
        {
            "metadata",
            "company",
            "runtime",
            "logging",
            "modules",
            "providers",
            "bootstrap",
        }
    )
    _required_fields = {
        "metadata": "name",
        "company": "name",
        "runtime": "environment",
        "logging": "level",
    }

    def validate(self, configuration: Mapping[str, object]) -> None:
        missing_sections = self._required_sections.difference(configuration)
        if missing_sections:
            section = sorted(missing_sections)[0]
            raise ValidationException(
                f"Missing required section: {section}",
                "TASC-VALIDATION-0001",
                details={"section": section},
            )

        unknown_sections = set(configuration).difference(self._required_sections)
        if unknown_sections:
            section = sorted(unknown_sections)[0]
            raise ValidationException(
                f"Unknown top-level section: {section}",
                "TASC-VALIDATION-0002",
                details={"section": section},
            )

        for section in self._mapping_sections:
            if not isinstance(configuration[section], Mapping):
                raise ValidationException(
                    f"Section must be a mapping: {section}",
                    "TASC-VALIDATION-0004",
                    details={"section": section},
                )

        for section, field in self._required_fields.items():
            section_data = configuration[section]
            if field not in section_data:
                raise ValidationException(
                    f"Missing required field: {section}.{field}",
                    "TASC-VALIDATION-0003",
                    details={"section": section, "field": field},
                )

        logging_data = configuration["logging"]
        for field in ("console", "file"):
            if field in logging_data and not isinstance(logging_data[field], bool):
                raise ValidationException(
                    f"Field must be a boolean: logging.{field}",
                    "TASC-VALIDATION-0004",
                    details={"section": "logging", "field": field},
                )
