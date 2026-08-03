"""Core bootstrap command."""

from pathlib import Path

import typer

from tasc_core.bootstrap import BootstrapEngine
from tasc_core.exceptions import BootstrapException


def bootstrap(
    config: Path = typer.Option(Path("config/core.yaml"), "--config"),
) -> None:
    """Bootstrap the TASC Core."""
    try:
        BootstrapEngine().bootstrap(config)
    except BootstrapException as exc:
        reason = exc.cause if exc.cause is not None else exc
        typer.echo("Bootstrap failed.", err=True)
        typer.echo(err=True)
        typer.echo("Reason:", err=True)
        typer.echo(err=True)
        typer.echo(str(reason), err=True)
        raise typer.Exit(code=1) from None

    typer.echo("Bootstrap completed successfully.")
