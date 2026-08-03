"""Agent interface namespace."""

from .agent_provider import IAgentProvider
from .agent_repository import IAgentRepository
from .agent_service import IAGentService

__all__ = ["IAgentProvider", "IAgentRepository", "IAGentService"]
