from __future__ import annotations

from pathlib import Path

import yaml

from ..exceptions import PromptException
from ..interfaces import IPromptRepository
from ..models import PromptMetadata, PromptTemplate, PromptVariable


class FilesystemPromptRepository(IPromptRepository):
    """Load read-only Prompt templates from YAML files beneath a root directory."""

    def __init__(self, root: Path) -> None:
        self._root = root

    def get(self, name: str) -> PromptTemplate:
        for template_file in self._template_files():
            template = self._load_template(template_file)
            if template.metadata.name == name:
                return template

        raise PromptException(f"Prompt template not found: {name}")

    def list(self) -> list[PromptTemplate]:
        return [self._load_template(template_file) for template_file in self._template_files()]

    def exists(self, name: str) -> bool:
        for template_file in self._template_files():
            template = self._load_template(template_file)
            if template.metadata.name == name:
                return True

        return False

    def _template_files(self) -> list[Path]:
        if not self._root.is_dir():
            return []

        return sorted(self._root.rglob("*.yaml"))

    def _load_template(self, template_file: Path) -> PromptTemplate:
        try:
            data = yaml.safe_load(template_file.read_text(encoding="utf-8"))
            return self._template_from_data(data)
        except (OSError, TypeError, ValueError, KeyError, yaml.YAMLError) as exc:
            raise PromptException(f"Malformed prompt template: {template_file}") from exc

    @staticmethod
    def _template_from_data(data: object) -> PromptTemplate:
        if not isinstance(data, dict):
            raise TypeError("Prompt template data must be a mapping")

        metadata = data["metadata"]
        variables = data["variables"]
        if not isinstance(metadata, dict) or not isinstance(variables, list):
            raise TypeError("Prompt template sections have invalid types")

        tags = metadata["tags"]
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            raise TypeError("Prompt metadata tags must be a list of strings")

        prompt_variables = [
            FilesystemPromptRepository._variable_from_data(variable)
            for variable in variables
        ]

        return PromptTemplate(
            metadata=PromptMetadata(
                name=FilesystemPromptRepository._required_string(metadata, "name"),
                display_name=FilesystemPromptRepository._required_string(
                    metadata, "display_name"
                ),
                description=FilesystemPromptRepository._required_string(
                    metadata, "description"
                ),
                version=FilesystemPromptRepository._required_string(metadata, "version"),
                author=FilesystemPromptRepository._required_string(metadata, "author"),
                tags=tags,
            ),
            system_prompt=FilesystemPromptRepository._required_string(
                data, "system_prompt"
            ),
            user_prompt=FilesystemPromptRepository._required_string(data, "user_prompt"),
            variables=prompt_variables,
        )

    @staticmethod
    def _variable_from_data(data: object) -> PromptVariable:
        if not isinstance(data, dict):
            raise TypeError("Prompt variable data must be a mapping")

        required = data["required"]
        default_value = data["default_value"]
        if not isinstance(required, bool):
            raise TypeError("Prompt variable required must be a boolean")
        if default_value is not None and not isinstance(default_value, str):
            raise TypeError("Prompt variable default value must be a string or null")

        return PromptVariable(
            name=FilesystemPromptRepository._required_string(data, "name"),
            description=FilesystemPromptRepository._required_string(data, "description"),
            required=required,
            default_value=default_value,
        )

    @staticmethod
    def _required_string(data: dict[object, object], key: str) -> str:
        value = data[key]
        if not isinstance(value, str):
            raise TypeError(f"{key} must be a string")
        return value
