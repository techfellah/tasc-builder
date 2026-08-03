from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import tasc_projects


class ProjectsPackageTests(unittest.TestCase):
    def test_package_imports(self) -> None:
        self.assertEqual(tasc_projects.__name__, "tasc_projects")

    def test_public_namespace_exists(self) -> None:
        self.assertTrue(hasattr(tasc_projects, "__all__"))


if __name__ == "__main__":
    unittest.main()
