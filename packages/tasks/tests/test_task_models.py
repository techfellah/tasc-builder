from __future__ import annotations

import json
import sys
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "agents"))

from tasc_agents.generation.models import GenerationResult, GenerationUsage
from tasc_tasks.models import TaskDefinition, TaskMetadata, TaskRequest, TaskResult


def task_metadata() -> TaskMetadata:
    return TaskMetadata(
        name="generate-api",
        display_name="Generate API",
        description="Generate an API implementation.",
        version="0.1.0",
        tags=["code", "api"],
    )


def task_definition() -> TaskDefinition:
    return TaskDefinition(
        metadata=task_metadata(),
        agent="architect",
        prompt="code_generation",
        inputs=["language", "requirements"],
    )


def generation_result() -> GenerationResult:
    return GenerationResult(
        content="Generated API implementation.",
        provider="ollama",
        model="llama3",
        usage=GenerationUsage(input_tokens=10, output_tokens=20, total_tokens=30),
        finish_reason="stop",
        duration_ms=125,
        metadata={},
    )


class TaskModelTests(unittest.TestCase):
    def test_construction(self) -> None:
        request = TaskRequest(
            definition=task_definition(),
            values={"language": "python", "requirements": "Create an API."},
        )

        self.assertEqual(request.definition.agent, "architect")
        self.assertEqual(request.values["language"], "python")

    def test_equality(self) -> None:
        self.assertEqual(task_definition(), task_definition())

    def test_immutability(self) -> None:
        metadata = task_metadata()

        with self.assertRaises(FrozenInstanceError):
            metadata.name = "changed"

    def test_nested_serialization(self) -> None:
        result = TaskResult(
            task=task_definition(),
            generation=generation_result(),
            status="completed",
            started_at=datetime(2026, 8, 4, 12, 0, tzinfo=timezone.utc),
            completed_at=datetime(2026, 8, 4, 12, 0, 1, tzinfo=timezone.utc),
        )

        self.assertEqual(
            result.to_dict(),
            {
                "task": {
                    "metadata": {
                        "name": "generate-api",
                        "display_name": "Generate API",
                        "description": "Generate an API implementation.",
                        "version": "0.1.0",
                        "tags": ["code", "api"],
                    },
                    "agent": "architect",
                    "prompt": "code_generation",
                    "inputs": ["language", "requirements"],
                },
                "generation": {
                    "content": "Generated API implementation.",
                    "provider": "ollama",
                    "model": "llama3",
                    "usage": {
                        "input_tokens": 10,
                        "output_tokens": 20,
                        "total_tokens": 30,
                    },
                    "finish_reason": "stop",
                    "duration_ms": 125,
                    "metadata": {},
                },
                "status": "completed",
                "started_at": "2026-08-04T12:00:00+00:00",
                "completed_at": "2026-08-04T12:00:01+00:00",
            },
        )

    def test_to_dict_is_json_compatible(self) -> None:
        result = TaskResult(
            task=task_definition(),
            generation=generation_result(),
            status="completed",
            started_at=datetime(2026, 8, 4, 12, 0, tzinfo=timezone.utc),
            completed_at=datetime(2026, 8, 4, 12, 0, 1, tzinfo=timezone.utc),
        )

        self.assertIsInstance(json.dumps(result.to_dict()), str)


if __name__ == "__main__":
    unittest.main()
