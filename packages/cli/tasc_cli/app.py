"""TASC Builder CLI application."""

import typer

from tasc_cli.commands.bootstrap import bootstrap
from tasc_cli.commands.doctor import doctor
from tasc_cli.commands.init import init
from tasc_cli.commands.validate import validate

app = typer.Typer(invoke_without_command=True, no_args_is_help=False)
app.command(name="init")(init)
app.command(name="validate")(validate)
app.command(name="bootstrap")(bootstrap)
app.command(name="doctor")(doctor)
