from __future__ import annotations

import json
import sys
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_agents.generation.models import GenerationResult, GenerationUsage


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


if __name__ == "__main__":
    unittest.main()
