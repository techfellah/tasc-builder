"""Configuration validation command."""

from pathlib import Path

import typer

from tasc_core.config.loader import ConfigurationLoader
from tasc_core.config.parser import ConfigurationParser
from tasc_core.config.validator import ConfigurationValidator
from tasc_core.exceptions import ConfigurationException, ValidationException


def validate(
    config: Path = typer.Option(Path("config/core.yaml"), "--config"),
) -> None:
    """Validate a Core configuration file."""
    try:
        text = ConfigurationLoader().load(config)
        configuration = ConfigurationParser().parse(text)
        ConfigurationValidator().validate(configuration)
    except ConfigurationException as exc:
        if exc.error_code == "TASC-CONFIG-0001":
            typer.echo(f"Configuration file not found: {config}", err=True)
        else:
            typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from None
    except ValidationException as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from None

    typer.echo("Configuration is valid.")
