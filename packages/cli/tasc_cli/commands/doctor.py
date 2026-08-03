"""Environment diagnostics command."""

import importlib
import sys
from pathlib import Path

import typer


def doctor() -> None:
    """Report the health of the local TASC environment."""
    checks = (
        ("Python Version", sys.version_info >= (3, 12)),
        ("Workspace", Path("workspace.yaml").exists()),
        ("Core Configuration", Path("config/core.yaml").exists()),
        ("Core Package", _is_core_package_importable()),
    )

    typer.echo("TASC Doctor")
    typer.echo()
    for name, passed in checks:
        status = "PASS" if passed else "FAIL"
        typer.echo(f"[{status}] {name}")

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
