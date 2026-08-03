"""Core bootstrap command."""

from pathlib import Path

import typer

from tasc_core.bootstrap import BootstrapEngine
from tasc_core.exceptions import BootstrapException, ConfigurationException


def bootstrap(
    config: Path = typer.Option(Path("config/core.yaml"), "--config"),
) -> None:
    """Bootstrap the TASC Core."""
    try:
        BootstrapEngine().bootstrap(config)
    except BootstrapException as exc:
        if isinstance(exc.cause, ConfigurationException) and (
            exc.cause.error_code == "TASC-CONFIG-0001"
        ):
            typer.echo(f"Configuration file not found: {config}", err=True)
        else:
            typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from None

    typer.echo("Bootstrap completed successfully.")
