from __future__ import annotations

import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_agents.exceptions import AgentException
from tasc_agents.interfaces import IAgentRepository
from tasc_agents.models import (
    Agent,
    AgentConfiguration,
    AgentMetadata,
    AgentModel,
    AgentRole,
)
from tasc_agents.repositories import FilesystemAgentRepository


def agent(name: str = "planner") -> Agent:
    return Agent(
        metadata=AgentMetadata(
            name=name,
            display_name="Planner",
            description="Plans tasks.",
            version="0.1.0",
            author="TASC",
            created_at=datetime(2026, 8, 3, 12, 0, tzinfo=timezone.utc),
        ),
        role=AgentRole(
            role_name="Planner",
            responsibilities=["Plan tasks"],
            system_prompt="Create a plan.",
        ),
        model=AgentModel(
            provider="ollama",
            model="llama3",
            temperature=0.2,
            max_tokens=1024,
        ),
        configuration=AgentConfiguration(
            tools=["search"],
            capabilities=["planning"],
            environment={"MODE": "test"},
        ),
    )


class FilesystemAgentRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.repository = FilesystemAgentRepository(self.root)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_create_writes_agent_yaml(self) -> None:
        self.repository.create(agent())

        self.assertTrue((self.root / "planner" / "agent.yaml").is_file())

    def test_get_returns_agent(self) -> None:
        expected = agent()
        self.repository.create(expected)

        self.assertEqual(self.repository.get("planner"), expected)

    def test_list_returns_agents(self) -> None:
        first = agent("first")
        second = agent("second")
        self.repository.create(first)
        self.repository.create(second)

        self.assertEqual(self.repository.list(), [first, second])

    def test_exists_returns_boolean(self) -> None:
        self.assertFalse(self.repository.exists("planner"))
        self.repository.create(agent())

        self.assertTrue(self.repository.exists("planner"))

    def test_delete_removes_agent_directory(self) -> None:
        self.repository.create(agent())

        self.repository.delete("planner")

        self.assertFalse((self.root / "planner").exists())

    def test_duplicate_create_raises_agent_exception(self) -> None:
        self.repository.create(agent())

        with self.assertRaises(AgentException):
            self.repository.create(agent())

    def test_missing_agent_raises_agent_exception(self) -> None:
        with self.assertRaises(AgentException):
            self.repository.get("missing")

    def test_malformed_file_raises_agent_exception(self) -> None:
        agent_directory = self.root / "planner"
        agent_directory.mkdir(parents=True)
        (agent_directory / "agent.yaml").write_text("metadata: [", encoding="utf-8")

        with self.assertRaises(AgentException):
            self.repository.get("planner")

    def test_interface_compliance(self) -> None:
        self.assertTrue(issubclass(FilesystemAgentRepository, IAgentRepository))
        self.assertIsInstance(self.repository, IAgentRepository)


if __name__ == "__main__":
    unittest.main()
