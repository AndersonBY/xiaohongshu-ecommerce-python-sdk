"""Base request/response dataclasses."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Generic, Optional, TypeVar


class BaseRequest:
    """Represent the common envelope for API requests."""

    def __init__(self, method: str) -> None:
        self.method = method
        self.app_id: Optional[str] = None
        self.sign: Optional[str] = None
        self.timestamp: Optional[str] = None
        self.version: Optional[str] = None
        self.access_token: Optional[str] = None

    def set_access_token(self, token: Optional[str]) -> None:
        self.access_token = token

    def to_payload(self) -> Dict[str, Any]:
        payload = {
            "method": self.method,
            "appId": self.app_id,
            "sign": self.sign,
            "timestamp": self.timestamp,
            "version": self.version,
            "accessToken": self.access_token,
        }
        payload.update(self.extra_payload())
        return {k: v for k, v in payload.items() if v is not None}

    def extra_payload(self) -> Dict[str, Any]:
        """Subclasses can override to append custom parameters."""

        return {}


T = TypeVar("T")


@dataclass
class BaseResponse(Generic[T]):
    success: bool
    code: Optional[str] = None
    data: Optional[T] = None
    msg: Optional[str] = None

    @property
    def error_message(self) -> Optional[str]:
        """Get error message from msg field."""
        return self.msg

    def as_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}
