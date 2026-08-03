from __future__ import annotations

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_core.config.loader import ConfigurationLoader
from tasc_core.exceptions import ConfigurationException
from tasc_core.interfaces.configuration import IConfigurationLoader


class ConfigurationLoaderTests(unittest.TestCase):
    def test_successful_read(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "settings.txt"
            path.write_text("hello", encoding="utf-8")

            loader = ConfigurationLoader()
            self.assertEqual(loader.load(path), "hello")

    def test_missing_file_raises_configuration_exception(self) -> None:
        loader = ConfigurationLoader()
        missing = Path("/tmp/does-not-exist-123456789")

        with self.assertRaises(ConfigurationException) as context:
            loader.load(missing)

        self.assertEqual(context.exception.error_code, "TASC-CONFIG-0001")

    def test_directory_instead_of_file_raises_configuration_exception(self) -> None:
        loader = ConfigurationLoader()

        with TemporaryDirectory() as tmp_dir:
            with self.assertRaises(ConfigurationException) as context:
                loader.load(Path(tmp_dir))

        self.assertEqual(context.exception.error_code, "TASC-CONFIG-0002")

    def test_unreadable_file_raises_configuration_exception(self) -> None:
        loader = ConfigurationLoader()

        with TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "settings.txt"
            path.write_text("hello", encoding="utf-8")

            with patch.object(Path, "read_text", side_effect=OSError("permission denied")):
                with self.assertRaises(ConfigurationException) as context:
                    loader.load(path)

        self.assertEqual(context.exception.error_code, "TASC-CONFIG-0003")

    def test_interface_compliance(self) -> None:
        self.assertTrue(issubclass(ConfigurationLoader, IConfigurationLoader))


if __name__ == "__main__":
    unittest.main()
