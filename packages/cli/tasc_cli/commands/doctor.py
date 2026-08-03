"""Environment diagnostics command."""

import importlib
import sys
from pathlib import Path

import typer

from tasc_core.config.loader import ConfigurationLoader
from tasc_core.config.parser import ConfigurationParser
from tasc_core.config.validator import ConfigurationValidator
from tasc_core.exceptions import ConfigurationException, ValidationException


def doctor() -> None:
    """Report the health of the local TASC environment."""
    configuration_valid, configuration_message = _check_core_configuration()
    checks = (
        ("Python Version", sys.version_info >= (3, 12)),
        ("Workspace", Path("workspace.yaml").exists()),
        ("Core Configuration", configuration_valid),
        ("Core Package", _is_core_package_importable()),
    )

    typer.echo("TASC Doctor")
    typer.echo()
    for name, passed in checks:
        status = "PASS" if passed else "FAIL"
        typer.echo(f"[{status}] {name}")
        if name == "Core Configuration" and configuration_message is not None:
            typer.echo(configuration_message)

    healthy = all(passed for _, passed in checks)
    typer.echo()
    typer.echo("Overall Status")
    typer.echo()
    typer.echo("HEALTHY" if healthy else "UNHEALTHY")

    if not healthy:
        raise typer.Exit(code=1)


def _is_core_package_importable() -> bool:
    try:
        importlib.import_module("tasc_core")
    except Exception:
        return False
    return True


def _check_core_configuration() -> tuple[bool, str | None]:
    try:
        text = ConfigurationLoader().load(Path("config/core.yaml"))
        configuration = ConfigurationParser().parse(text)
        ConfigurationValidator().validate(configuration)
    except (ConfigurationException, ValidationException) as exc:
        return False, str(exc)
    return True, None
