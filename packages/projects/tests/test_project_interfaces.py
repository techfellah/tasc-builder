from __future__ import annotations

import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_projects.interfaces import IProjectRepository, IProjectService


class ProjectInterfaceTests(unittest.TestCase):
    def test_interfaces_are_abstract(self) -> None:
        self.assertTrue(inspect.isabstract(IProjectRepository))
        self.assertTrue(inspect.isabstract(IProjectService))

    def test_interfaces_cannot_be_instantiated(self) -> None:
        with self.assertRaises(TypeError):
            IProjectRepository()

        with self.assertRaises(TypeError):
            IProjectService()

    def test_repository_methods_exist(self) -> None:
        for method in ("create", "get", "list", "exists", "delete"):
            self.assertTrue(hasattr(IProjectRepository, method))
            self.assertTrue(getattr(IProjectRepository, method).__isabstractmethod__)

    def test_service_methods_exist(self) -> None:
        for method in (
            "create_project",
            "get_project",
            "list_projects",
            "delete_project",
        ):
            self.assertTrue(hasattr(IProjectService, method))
            self.assertTrue(getattr(IProjectService, method).__isabstractmethod__)


if __name__ == "__main__":
    unittest.main()
