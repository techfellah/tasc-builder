"""Project management commands."""

from datetime import datetime, timezone
from pathlib import Path

import typer

from tasc_projects.exceptions import ProjectException
from tasc_projects.models import ProjectConfiguration, ProjectMetadata
from tasc_projects.repositories import FilesystemProjectRepository
from tasc_projects.services import ProjectService

project_app = typer.Typer()


@project_app.command("create")
def create_project(name: str) -> None:
    """Create a project in the current workspace."""
    metadata = ProjectMetadata(
        name=name,
        display_name=name,
        description="",
        version="0.1.0",
        created_at=datetime.now(timezone.utc),
    )
    configuration = ProjectConfiguration(
        language="python",
        framework="none",
        runtime="python",
        output_directory="output",
    )

    try:
        _project_service().create_project(metadata, configuration)
    except ProjectException as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from None

    typer.echo("Project created.")


@project_app.command("list")
def list_projects() -> None:
    """List projects in the current workspace."""
    try:
        projects = _project_service().list_projects()
    except ProjectException as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from None

    for project in projects:
        typer.echo(project.metadata.name)


@project_app.command("show")
def show_project(name: str) -> None:
    """Show project information."""
    try:
        project = _project_service().get_project(name)
    except ProjectException as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from None

    typer.echo(f"Name: {project.metadata.name}")
    typer.echo(f"Display Name: {project.metadata.display_name}")
    typer.echo(f"Description: {project.metadata.description}")
    typer.echo(f"Version: {project.metadata.version}")
    typer.echo(f"Created At: {project.metadata.created_at.isoformat()}")
    typer.echo(f"Language: {project.configuration.language}")
    typer.echo(f"Framework: {project.configuration.framework}")
    typer.echo(f"Runtime: {project.configuration.runtime}")
    typer.echo(f"Output Directory: {project.configuration.output_directory}")


@project_app.command("delete")
def delete_project(name: str) -> None:
    """Delete a project from the current workspace."""
    try:
        _project_service().delete_project(name)
    except ProjectException as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from None

    typer.echo("Project deleted.")


def _project_service() -> ProjectService:
    repository = FilesystemProjectRepository(Path.cwd())
    return ProjectService(repository)
