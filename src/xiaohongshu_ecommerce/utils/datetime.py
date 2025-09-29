"""Datetime helpers mirroring Java DateUtils essentials."""

from __future__ import annotations

from datetime import datetime, timezone


def utc_timestamp() -> int:
    """Return current UTC timestamp in seconds."""

    return int(datetime.now(tz=timezone.utc).timestamp())


def utc_millis() -> int:
    """Return current UTC timestamp in milliseconds."""

    return int(datetime.now(tz=timezone.utc).timestamp() * 1000)


def format_datetime(dt: datetime, pattern: str = "%Y-%m-%d %H:%M:%S") -> str:
    return dt.astimezone(timezone.utc).strftime(pattern)


def parse_datetime(value: str, pattern: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    dt = datetime.strptime(value, pattern)
    return dt.replace(tzinfo=timezone.utc)
