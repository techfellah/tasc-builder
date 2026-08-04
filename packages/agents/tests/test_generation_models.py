from __future__ import annotations

import json
import sys
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_agents.generation.models import (
    GenerationRequest,
    GenerationResult,
    GenerationUsage,
)
from tasc_agents.models import AgentModel
from tasc_agents.prompts.models import RenderedPrompt


def generation_usage() -> GenerationUsage:
    return GenerationUsage(input_tokens=120, output_tokens=80, total_tokens=200)


def generation_result() -> GenerationResult:
    return GenerationResult(
        content="Generated content.",
        provider="example-provider",
        model="example-model",
        usage=generation_usage(),
        finish_reason="stop",
        duration_ms=425,
        metadata={"request_id": "request-123"},
    )


def generation_request() -> GenerationRequest:
    return GenerationRequest(
        prompt=RenderedPrompt(
            system_prompt="You are helpful.",
            user_prompt="Hello Alice.",
            variables={"name": "Alice"},
        ),
        model=AgentModel(
            provider="example-provider",
            model="example-model",
            temperature=0.2,
            max_tokens=1024,
        ),
        metadata={"request_id": "request-123"},
    )


class GenerationModelTests(unittest.TestCase):
    def test_construction(self) -> None:
        result = generation_result()

        self.assertEqual(result.content, "Generated content.")
        self.assertEqual(result.usage.total_tokens, 200)

    def test_equality(self) -> None:
        self.assertEqual(generation_result(), generation_result())

    def test_immutability(self) -> None:
        usage = generation_usage()

        with self.assertRaises(FrozenInstanceError):
            usage.total_tokens = 100

    def test_nested_serialization(self) -> None:
        self.assertEqual(
            generation_result().to_dict(),
            {
                "content": "Generated content.",
                "provider": "example-provider",
                "model": "example-model",
                "usage": {
                    "input_tokens": 120,
                    "output_tokens": 80,
                    "total_tokens": 200,
                },
                "finish_reason": "stop",
                "duration_ms": 425,
                "metadata": {"request_id": "request-123"},
            },
        )

    def test_to_dict_is_json_compatible(self) -> None:
        self.assertIsInstance(json.dumps(generation_result().to_dict()), str)


class GenerationRequestModelTests(unittest.TestCase):
    def test_construction(self) -> None:
        request = generation_request()

        self.assertEqual(request.prompt.user_prompt, "Hello Alice.")
        self.assertEqual(request.model.model, "example-model")

    def test_equality(self) -> None:
        self.assertEqual(generation_request(), generation_request())

    def test_immutability(self) -> None:
        request = generation_request()

        with self.assertRaises(FrozenInstanceError):
            request.model = AgentModel(
                provider="other-provider",
                model="other-model",
                temperature=0.0,
                max_tokens=512,
            )

    def test_nested_serialization(self) -> None:
        self.assertEqual(
            generation_request().to_dict(),
            {
                "prompt": {
                    "system_prompt": "You are helpful.",
                    "user_prompt": "Hello Alice.",
                    "variables": {"name": "Alice"},
                },
                "model": {
                    "provider": "example-provider",
                    "model": "example-model",
                    "temperature": 0.2,
                    "max_tokens": 1024,
                },
                "metadata": {"request_id": "request-123"},
            },
        )

    def test_to_dict_is_json_compatible(self) -> None:
        self.assertIsInstance(json.dumps(generation_request().to_dict()), str)


if __name__ == "__main__":
    unittest.main()
