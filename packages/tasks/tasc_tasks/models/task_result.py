from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from tasc_agents.generation.models import GenerationResult

from .task_definition import TaskDefinition


@dataclass(frozen=True)
class TaskResult:
    task: TaskDefinition
    generation: GenerationResult
    status: str
    started_at: datetime
    completed_at: datetime

    def to_dict(self) -> dict[str, object]:
        return {
            "task": self.task.to_dict(),
            "generation": self.generation.to_dict(),
            "status": self.status,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat(),
        }
