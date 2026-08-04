from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import tasc_tasks


class TasksPackageTests(unittest.TestCase):
    def test_package_imports(self) -> None:
        self.assertEqual(tasc_tasks.__name__, "tasc_tasks")

    def test_public_namespace_exists(self) -> None:
        self.assertTrue(hasattr(tasc_tasks, "__all__"))


if __name__ == "__main__":
    unittest.main()
