"""Error definitions aligned with the Java SDK."""

from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class BaseErrorCode:
    error_code: int
    error_msg: str


class OpenSdkErrorCode(enum.Enum):
    MISSING_PARAMS = BaseErrorCode(11, "参数缺失")
    SIGNATURE_ERROR = BaseErrorCode(12, "签名错误")
    AUTH_ERROR = BaseErrorCode(13, "认证错误")
    NETWORK_ERROR = BaseErrorCode(20, "网络请求异常")
    HTTP_ERROR = BaseErrorCode(21, "HTTP状态异常")
    SERIALIZATION_ERROR = BaseErrorCode(30, "序列化失败")
    UNKNOWN_ERROR = BaseErrorCode(99, "未知错误")

    @classmethod
    def get_by_code(cls, code: int) -> Optional["OpenSdkErrorCode"]:
        for member in cls:
            if member.value.error_code == code:
                return member
        return None


class OpenSdkException(Exception):
    """SDK level error with structured error code."""

    def __init__(
        self,
        error: OpenSdkErrorCode,
        custom_msg: Optional[str] = None,
        *,
        cause: Optional[BaseException] = None,
    ) -> None:
        self.error = error
        self.custom_msg = custom_msg
        self.__cause__ = cause
        super().__init__(self._build_message())

    def _build_message(self) -> str:
        base = self.error.value.error_msg
        if self.custom_msg:
            return f"{base}: {self.custom_msg}"
        return base

    @property
    def error_code(self) -> int:
        return self.error.value.error_code

    @property
    def error_msg(self) -> str:
        return self.error.value.error_msg

    def __str__(self) -> str:  # pragma: no cover - reps default to base class
        return self._build_message()
