"""HTTP session management helpers."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

import httpx

from .config import ClientConfig


@contextmanager
def create_session(config: ClientConfig) -> Iterator[httpx.Client]:
    timeout = httpx.Timeout(timeout=config.timeout, connect=config.connect_timeout)
    with httpx.Client(
        timeout=timeout, proxy=config.proxy, headers=config.headers
    ) as client:
        client.headers.setdefault("Content-Type", "application/json; charset=utf-8")
        yield client
