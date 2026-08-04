from __future__ import annotations

from dataclasses import dataclass

from .task_metadata import TaskMetadata


@dataclass(frozen=True)
class TaskDefinition:
    metadata: TaskMetadata
    agent: str
    prompt: str
    inputs: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "metadata": self.metadata.to_dict(),
            "agent": self.agent,
            "prompt": self.prompt,
            "inputs": list(self.inputs),
        }
