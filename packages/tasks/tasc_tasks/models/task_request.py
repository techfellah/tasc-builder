from __future__ import annotations

from dataclasses import dataclass

from .task_definition import TaskDefinition


@dataclass(frozen=True)
class TaskRequest:
    definition: TaskDefinition
    values: dict[str, str]

    def to_dict(self) -> dict[str, object]:
        return {
            "definition": self.definition.to_dict(),
            "values": dict(self.values),
        }
