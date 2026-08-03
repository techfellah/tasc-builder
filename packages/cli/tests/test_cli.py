from __future__ import annotations

import sys
import unittest
from pathlib import Path

from typer.testing import CliRunner

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_cli.app import app


class CliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_cli_starts_successfully(self) -> None:
        result = self.runner.invoke(app)

        self.assertEqual(result.exit_code, 0)

    def test_help_works(self) -> None:
        result = self.runner.invoke(app, ["--help"])

        self.assertEqual(result.exit_code, 0)

    def test_commands_exist(self) -> None:
        result = self.runner.invoke(app, ["--help"])

        self.assertIn("init", result.output)
        self.assertIn("validate", result.output)
        self.assertIn("bootstrap", result.output)
        self.assertIn("doctor", result.output)

    def test_init_command(self) -> None:
        result = self.runner.invoke(app, ["init"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            result.output,
            "TASC Builder initialization is not yet implemented.\n",
        )

    def test_validate_command(self) -> None:
        result = self.runner.invoke(app, ["validate"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            result.output,
            "Configuration validation is not yet implemented.\n",
        )

    def test_bootstrap_command(self) -> None:
        result = self.runner.invoke(app, ["bootstrap"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "Bootstrap is not yet implemented.\n")

    def test_doctor_command(self) -> None:
        result = self.runner.invoke(app, ["doctor"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            result.output,
            "Environment diagnostics are not yet implemented.\n",
        )


if __name__ == "__main__":
    unittest.main()
