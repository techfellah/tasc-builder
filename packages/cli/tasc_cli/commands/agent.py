"""Agent management commands."""

from datetime import datetime, timezone
from pathlib import Path

import typer

from tasc_agents.exceptions import AgentException
from tasc_agents.models import (
    Agent,
    AgentConfiguration,
    AgentMetadata,
    AgentModel,
    AgentRole,
)
from tasc_agents.repositories import FilesystemAgentRepository
from tasc_agents.services import AgentService

agent_app = typer.Typer()


@agent_app.command("create")
def create_agent(name: str) -> None:
    """Create an Agent in the current workspace."""
    agent = Agent(
        metadata=AgentMetadata(
            name=name,
            display_name=name,
            description="",
            version="0.1.0",
            author="TASC Builder",
            created_at=datetime.now(timezone.utc),
        ),
        role=AgentRole(
            role_name="assistant",
            responsibilities=[],
            system_prompt="",
        ),
        model=AgentModel(
            provider="ollama",
            model="",
            temperature=0.0,
            max_tokens=0,
        ),
        configuration=AgentConfiguration(
            tools=[],
            capabilities=[],
            environment={},
        ),
    )

    try:
        _agent_service().create_agent(agent)
    except AgentException as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from None

    typer.echo("Agent created.")


@agent_app.command("list")
def list_agents() -> None:
    """List Agents in the current workspace."""
    try:
        agents = _agent_service().list_agents()
    except AgentException as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from None

    for agent in agents:
        typer.echo(agent.metadata.name)


@agent_app.command("show")
def show_agent(name: str) -> None:
    """Show Agent information."""
    try:
        agent = _agent_service().get_agent(name)
    except AgentException as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from None

    typer.echo("Metadata")
    typer.echo(f"Name: {agent.metadata.name}")
    typer.echo(f"Display Name: {agent.metadata.display_name}")
    typer.echo(f"Description: {agent.metadata.description}")
    typer.echo(f"Version: {agent.metadata.version}")
    typer.echo(f"Author: {agent.metadata.author}")
    typer.echo(f"Created At: {agent.metadata.created_at.isoformat()}")
    typer.echo("Role")
    typer.echo(f"Role Name: {agent.role.role_name}")
    typer.echo(f"Responsibilities: {', '.join(agent.role.responsibilities)}")
    typer.echo(f"System Prompt: {agent.role.system_prompt}")
    typer.echo("Model")
    typer.echo(f"Provider: {agent.model.provider}")
    typer.echo(f"Model: {agent.model.model}")
    typer.echo(f"Temperature: {agent.model.temperature}")
    typer.echo(f"Max Tokens: {agent.model.max_tokens}")
    typer.echo("Configuration")
    typer.echo(f"Tools: {', '.join(agent.configuration.tools)}")
    typer.echo(f"Capabilities: {', '.join(agent.configuration.capabilities)}")
    typer.echo(f"Environment: {agent.configuration.environment}")


@agent_app.command("delete")
def delete_agent(name: str) -> None:
    """Delete an Agent from the current workspace."""
    try:
        _agent_service().delete_agent(name)
    except AgentException as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from None

    typer.echo("Agent deleted.")


def _agent_service() -> AgentService:
    repository = FilesystemAgentRepository(Path.cwd() / "agents")
    return AgentService(repository)
