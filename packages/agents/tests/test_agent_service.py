from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_agents.interfaces import IAgentRepository, IAGentService
from tasc_agents.models import Agent
from tasc_agents.services import AgentService


class AgentServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = Mock(spec=IAgentRepository)
        self.service = AgentService(self.repository)

    def test_create_agent_calls_repository_create(self) -> None:
        agent = Mock(spec=Agent)

        self.service.create_agent(agent)

        self.repository.create.assert_called_once_with(agent)

    def test_get_agent_calls_repository_get(self) -> None:
        agent = Mock(spec=Agent)
        self.repository.get.return_value = agent

        result = self.service.get_agent("planner")

        self.assertIs(result, agent)
        self.repository.get.assert_called_once_with("planner")

    def test_list_agents_calls_repository_list(self) -> None:
        agents = [Mock(spec=Agent)]
        self.repository.list.return_value = agents

        result = self.service.list_agents()

        self.assertIs(result, agents)
        self.repository.list.assert_called_once_with()

    def test_delete_agent_calls_repository_delete(self) -> None:
        self.service.delete_agent("planner")

        self.repository.delete.assert_called_once_with("planner")

    def test_interface_compliance(self) -> None:
        self.assertTrue(issubclass(AgentService, IAGentService))
        self.assertIsInstance(self.service, IAGentService)


if __name__ == "__main__":
    unittest.main()
