from __future__ import annotations

import json
import sys
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_agents.models import (
    Agent,
    AgentConfiguration,
    AgentMetadata,
    AgentModel,
    AgentRole,
)


def agent_metadata() -> AgentMetadata:
    return AgentMetadata(
        name="planner",
        display_name="Planner",
        description="Plans work.",
        version="0.1.0",
        author="TASC",
        created_at=datetime(2026, 8, 3, 12, 0, tzinfo=timezone.utc),
    )


def agent_role() -> AgentRole:
    return AgentRole(
        role_name="planner",
        responsibilities=["plan", "coordinate"],
        system_prompt="Plan the requested work.",
    )


def agent_model() -> AgentModel:
    return AgentModel(
        provider="openai",
        model="gpt-5",
        temperature=0.2,
        max_tokens=4096,
    )


def agent_configuration() -> AgentConfiguration:
    return AgentConfiguration(
        tools=["filesystem"],
        capabilities=["planning"],
        environment={"MODE": "test"},
    )


class AgentModelTests(unittest.TestCase):
    def test_construction(self) -> None:
        agent = Agent(
            metadata=agent_metadata(),
            role=agent_role(),
            model=agent_model(),
            configuration=agent_configuration(),
        )

        self.assertEqual(agent.metadata.name, "planner")
        self.assertEqual(agent.model.provider, "openai")

    def test_equality(self) -> None:
        self.assertEqual(
            Agent(
                metadata=agent_metadata(),
                role=agent_role(),
                model=agent_model(),
                configuration=agent_configuration(),
            ),
            Agent(
                metadata=agent_metadata(),
                role=agent_role(),
                model=agent_model(),
                configuration=agent_configuration(),
            ),
        )

    def test_immutability(self) -> None:
        metadata = agent_metadata()

        with self.assertRaises(FrozenInstanceError):
            metadata.name = "changed"

    def test_nested_composition(self) -> None:
        agent = Agent(
            metadata=agent_metadata(),
            role=agent_role(),
            model=agent_model(),
            configuration=agent_configuration(),
        )

        self.assertEqual(agent.role.responsibilities, ["plan", "coordinate"])
        self.assertEqual(agent.configuration.environment, {"MODE": "test"})

    def test_to_dict(self) -> None:
        agent = Agent(
            metadata=agent_metadata(),
            role=agent_role(),
            model=agent_model(),
            configuration=agent_configuration(),
        )

        self.assertEqual(
            agent.to_dict(),
            {
                "metadata": {
                    "name": "planner",
                    "display_name": "Planner",
                    "description": "Plans work.",
                    "version": "0.1.0",
                    "author": "TASC",
                    "created_at": "2026-08-03T12:00:00+00:00",
                },
                "role": {
                    "role_name": "planner",
                    "responsibilities": ["plan", "coordinate"],
                    "system_prompt": "Plan the requested work.",
                },
                "model": {
                    "provider": "openai",
                    "model": "gpt-5",
                    "temperature": 0.2,
                    "max_tokens": 4096,
                },
                "configuration": {
                    "tools": ["filesystem"],
                    "capabilities": ["planning"],
                    "environment": {"MODE": "test"},
                },
            },
        )

    def test_to_dict_is_json_compatible(self) -> None:
        agent = Agent(
            metadata=agent_metadata(),
            role=agent_role(),
            model=agent_model(),
            configuration=agent_configuration(),
        )

        self.assertIsInstance(json.dumps(agent.to_dict()), str)


if __name__ == "__main__":
    unittest.main()
