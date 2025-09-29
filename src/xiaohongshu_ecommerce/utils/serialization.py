"""JSON serialization helpers."""

from __future__ import annotations

import dataclasses
import json
from typing import Any, Mapping, MutableMapping, Optional, Sequence, Type, TypeVar

from ..errors import OpenSdkErrorCode, OpenSdkException

T = TypeVar("T")


def json_dumps(data: Any) -> str:
    try:
        return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    except (TypeError, ValueError) as exc:  # pragma: no cover - rare branch
        raise OpenSdkException(OpenSdkErrorCode.SERIALIZATION_ERROR, str(exc)) from exc


def json_loads(data: str) -> Any:
    try:
        return json.loads(data)
    except (TypeError, ValueError) as exc:
        raise OpenSdkException(OpenSdkErrorCode.SERIALIZATION_ERROR, str(exc)) from exc


def coerce_type(raw: Any, target: Optional[Type[T]]) -> Any:
    if target is None or raw is None:
        return raw

    if isinstance(raw, target):
        return raw

    if hasattr(target, "from_dict"):
        if isinstance(raw, Mapping):
            return target.from_dict(raw)  # type: ignore[attr-defined]
        raise OpenSdkException(OpenSdkErrorCode.SERIALIZATION_ERROR, "数据格式不匹配")

    if dataclasses.is_dataclass(target):
        if isinstance(raw, Mapping):
            return target(**raw)  # type: ignore[arg-type]
        raise OpenSdkException(OpenSdkErrorCode.SERIALIZATION_ERROR, "数据格式不匹配")

    if _is_generic_sequence(target) and isinstance(raw, Sequence):
        return list(raw)

    if _is_generic_mapping(target) and isinstance(raw, (Mapping, MutableMapping)):
        return dict(raw)

    try:
        return target(raw)  # type: ignore[arg-type]
    except Exception as exc:  # pragma: no cover - fallback path
        raise OpenSdkException(OpenSdkErrorCode.SERIALIZATION_ERROR, str(exc)) from exc


def _is_generic_sequence(tp: Type[Any]) -> bool:
    return getattr(tp, "__origin__", None) in (list, tuple)


def _is_generic_mapping(tp: Type[Any]) -> bool:
    return getattr(tp, "__origin__", None) is dict
