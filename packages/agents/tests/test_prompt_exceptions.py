from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_agents.prompts.exceptions import PromptException, PromptRenderException


class PromptExceptionTests(unittest.TestCase):
    def test_inheritance(self) -> None:
        self.assertTrue(issubclass(PromptRenderException, PromptException))

    def test_isinstance(self) -> None:
        exception = PromptRenderException("Missing variable: project_name")

        self.assertIsInstance(exception, PromptRenderException)
        self.assertIsInstance(exception, PromptException)
        self.assertIsInstance(exception, Exception)

    def test_message_is_preserved(self) -> None:
        message = "Malformed template"

        self.assertEqual(str(PromptRenderException(message)), message)


if __name__ == "__main__":
    unittest.main()
