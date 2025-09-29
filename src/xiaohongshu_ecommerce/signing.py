"""Signature calculation helpers."""

from __future__ import annotations

import hashlib

from .errors import OpenSdkErrorCode, OpenSdkException


def build_signature(
    *,
    method: str,
    app_id: str,
    timestamp: str,
    version: str,
    app_secret: str,
) -> str:
    if not all([method, app_id, timestamp, version, app_secret]):
        raise OpenSdkException(OpenSdkErrorCode.MISSING_PARAMS, "签名参数缺失")

    params = [f"appId={app_id}", f"timestamp={timestamp}", f"version={version}"]
    query = "&".join(sorted(params, key=_lower_key))
    origin = f"{method}?{query}{app_secret}"
    md5 = hashlib.md5()
    md5.update(origin.encode("utf-8"))
    return md5.hexdigest()


def _lower_key(value: str) -> str:
    return value.lower()
