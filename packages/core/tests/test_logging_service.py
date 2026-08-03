from __future__ import annotations

import inspect
import logging
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_core.logging import CoreLogger, LogFormatter, LoggerFactory
from tasc_core.logging.logger import CoreLogger as LoggerClass
from tasc_core.models.log_level import LogLevel
from tasc_core.models.log_record import LogRecord


class LoggingServiceTests(unittest.TestCase):
    def test_logger_factory_creates_loggers(self) -> None:
        factory = LoggerFactory()
        logger = factory.create_logger("core")

        self.assertIsInstance(logger, CoreLogger)
        self.assertTrue(isinstance(logger, LoggerClass))

    def test_all_log_levels_work(self) -> None:
        logger = LoggerFactory().create_logger("core")

        logger.debug("debug message")
        logger.info("info message")
        logger.warning("warning message")
        logger.error("error message")
        logger.critical("critical message")

    def test_exception_creates_a_log_record(self) -> None:
        logger = LoggerFactory().create_logger("core")
        logger.exception("failure", ValueError("boom"), component="builder")

    def test_formatter_output(self) -> None:
        timestamp = datetime(2026, 8, 3, 11, 35, 12, tzinfo=timezone.utc)
        record = LogRecord(
            timestamp=timestamp,
            level=LogLevel.INFO,
            logger="Core",
            message="Configuration loaded",
            context={},
            exception=None,
        )

        formatted = LogFormatter().format(record)
        self.assertIn("2026-08-03T11:35:12+00:00", formatted)
        self.assertIn("INFO", formatted)
        self.assertIn("Core", formatted)
        self.assertIn("Configuration loaded", formatted)

    def test_log_level_enum(self) -> None:
        self.assertEqual(LogLevel.DEBUG.value, "DEBUG")
        self.assertEqual(LogLevel.INFO.value, "INFO")
        self.assertEqual(LogLevel.WARNING.value, "WARNING")
        self.assertEqual(LogLevel.ERROR.value, "ERROR")
        self.assertEqual(LogLevel.CRITICAL.value, "CRITICAL")

    def test_updated_log_record_level_is_log_level(self) -> None:
        timestamp = datetime(2026, 8, 3, 11, 35, 12, tzinfo=timezone.utc)
        record = LogRecord(
            timestamp=timestamp,
            level=LogLevel.INFO,
            logger="Core",
            message="Configuration loaded",
            context={},
            exception=None,
        )

        self.assertIsInstance(record.level, LogLevel)
        self.assertEqual(record.to_dict()["level"], "INFO")


if __name__ == "__main__":
    unittest.main()
