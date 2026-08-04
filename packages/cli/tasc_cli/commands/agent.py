"""Agent management commands."""

from datetime import datetime, timezone
from pathlib import Path

import typer

from tasc_agents.exceptions import AgentException
from tasc_agents.interfaces import IAgentProvider
from tasc_agents.models import (
    Agent,
    AgentConfiguration,
    AgentMetadata,
    AgentModel,
    AgentRole,
)
from tasc_agents.prompts import templates as prompt_templates
from tasc_agents.prompts.exceptions import PromptException
from tasc_agents.prompts.models import PromptRenderRequest
from tasc_agents.prompts.repositories import FilesystemPromptRepository
from tasc_agents.prompts.services import PromptService
from tasc_agents.providers import OllamaProvider
from tasc_agents.repositories import FilesystemAgentRepository
from tasc_agents.services import AgentExecutor, AgentService
from tasc_core.registry.registry import Registry

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


@agent_app.command("run")
def run_agent(
    agent_name: str,
    template_name: str = typer.Option(..., "--template"),
    variables: list[str] = typer.Option([], "--var"),
) -> None:
    """Run an Agent with a built-in prompt template."""
    try:
        values = _parse_variables(variables)
        agent = _agent_service().get_agent(agent_name)
        template = _prompt_repository().get(template_name)
        prompt = PromptService().render(
            PromptRenderRequest(template=template, values=values)
        )

        registry = Registry()
        registry.register(IAgentProvider, OllamaProvider())
        result = AgentExecutor(registry).execute(
            agent,
            prompt,
            {"agent_name": agent_name, "template_name": template_name},
        )
    except (AgentException, PromptException) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from None

    typer.echo(f"Provider: {result.provider}")
    typer.echo(f"Model: {result.model}")
    typer.echo(f"Duration: {result.duration_ms} ms")
    typer.echo()
    typer.echo(result.content)


def _agent_service() -> AgentService:
    repository = FilesystemAgentRepository(Path.cwd() / "agents")
    return AgentService(repository)


def _prompt_repository() -> FilesystemPromptRepository:
    return FilesystemPromptRepository(Path(prompt_templates.__file__).parent)


def _parse_variables(variables: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for variable in variables:
        if "=" not in variable:
            raise PromptException(f"Invalid variable: {variable}")
        key, value = variable.split("=", maxsplit=1)
        if not key:
            raise PromptException(f"Invalid variable: {variable}")
        values[key] = value
    return values
