"""OAuth request and response models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping

from .base import BaseRequest


class GetAccessTokenRequest(BaseRequest):
    def __init__(self, code: str) -> None:
        super().__init__(method="oauth.getAccessToken")
        self.code = code

    def extra_payload(self) -> Dict[str, str]:
        return {"code": self.code}


class RefreshTokenRequest(BaseRequest):
    def __init__(self, refresh_token: str) -> None:
        super().__init__(method="oauth.refreshToken")
        self.refresh_token = refresh_token

    def extra_payload(self) -> Dict[str, str]:
        return {"refreshToken": self.refresh_token}


@dataclass
class TokenResponse:
    access_token: str
    access_token_expires_at: int
    refresh_token: str
    refresh_token_expires_at: int
    seller_id: str
    seller_name: str

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "TokenResponse":
        return cls(
            access_token=str(data.get("accessToken", "")),
            access_token_expires_at=_int(data.get("accessTokenExpiresAt")),
            refresh_token=str(data.get("refreshToken", "")),
            refresh_token_expires_at=_int(data.get("refreshTokenExpiresAt")),
            seller_id=str(data.get("sellerId", "")),
            seller_name=str(data.get("sellerName", "")),
        )


def _int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


GetAccessTokenResponse = TokenResponse
RefreshTokenResponse = TokenResponse

__all__ = [
    "GetAccessTokenRequest",
    "RefreshTokenRequest",
    "GetAccessTokenResponse",
    "RefreshTokenResponse",
]
