from __future__ import annotations

import json
import sys
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasc_core.models.log_level import LogLevel
from tasc_core.models.log_record import LogRecord


class LogRecordTests(unittest.TestCase):
    def test_construction(self) -> None:
        timestamp = datetime(2026, 8, 3, 12, 30, tzinfo=timezone.utc)
        record = LogRecord(
            timestamp=timestamp,
            level=LogLevel.INFO,
            logger="core",
            message="hello",
            context={"component": "builder"},
            exception=None,
        )

        self.assertEqual(record.timestamp, timestamp)
        self.assertEqual(record.level, LogLevel.INFO)
        self.assertEqual(record.logger, "core")
        self.assertEqual(record.message, "hello")
        self.assertEqual(record.context, {"component": "builder"})
        self.assertIsNone(record.exception)

    def test_immutability(self) -> None:
        record = LogRecord(
            timestamp=datetime.now(timezone.utc),
            level=LogLevel.INFO,
            logger="core",
            message="hello",
            context={},
            exception=None,
        )

        with self.assertRaises(FrozenInstanceError):
            record.message = "changed"

    def test_equality(self) -> None:
        timestamp = datetime(2026, 8, 3, 12, 30, tzinfo=timezone.utc)
        left = LogRecord(
            timestamp=timestamp,
            level=LogLevel.INFO,
            logger="core",
            message="hello",
            context={"component": "builder"},
            exception=None,
        )
        right = LogRecord(
            timestamp=timestamp,
            level=LogLevel.INFO,
            logger="core",
            message="hello",
            context={"component": "builder"},
            exception=None,
        )

        self.assertEqual(left, right)

    def test_to_dict(self) -> None:
        timestamp = datetime(2026, 8, 3, 12, 30, tzinfo=timezone.utc)
        record = LogRecord(
            timestamp=timestamp,
            level=LogLevel.INFO,
            logger="core",
            message="hello",
            context={"component": "builder"},
            exception=None,
        )

        self.assertEqual(
            record.to_dict(),
            {
                "timestamp": "2026-08-03T12:30:00+00:00",
                "level": "INFO",
                "logger": "core",
                "message": "hello",
                "context": {"component": "builder"},
                "exception": None,
            },
        )

    def test_timestamp_serialization(self) -> None:
        timestamp = datetime(2026, 8, 3, 12, 30, tzinfo=timezone.utc)
        record = LogRecord(
            timestamp=timestamp,
            level=LogLevel.INFO,
            logger="core",
            message="hello",
            context={},
            exception=None,
        )

        self.assertEqual(record.to_dict()["timestamp"], "2026-08-03T12:30:00+00:00")

    def test_json_compatibility(self) -> None:
        timestamp = datetime(2026, 8, 3, 12, 30, tzinfo=timezone.utc)
        record = LogRecord(
            timestamp=timestamp,
            level=LogLevel.INFO,
            logger="core",
            message="hello",
            context={"component": "builder"},
            exception="ValueError: bad",
        )

        payload = json.dumps(record.to_dict())
        self.assertIn('"timestamp": "2026-08-03T12:30:00+00:00"', payload)
        self.assertIn('"exception": "ValueError: bad"', payload)


if __name__ == "__main__":
    unittest.main()
