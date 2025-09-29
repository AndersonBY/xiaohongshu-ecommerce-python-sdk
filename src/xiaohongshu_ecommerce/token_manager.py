"""Token management system for automatic OAuth token handling."""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from threading import Lock
from typing import TYPE_CHECKING, Callable, Optional, Protocol

if TYPE_CHECKING:
    from .client.oauth import OauthClient
    from .models.oauth import GetAccessTokenResponse, RefreshTokenResponse


class TokenStorage(Protocol):
    """Protocol for token storage implementations."""

    def load_tokens(self) -> Optional[TokenInfo]:
        """Load tokens from storage."""
        ...

    def save_tokens(self, tokens: TokenInfo) -> None:
        """Save tokens to storage."""
        ...

    def clear_tokens(self) -> None:
        """Clear tokens from storage."""
        ...


@dataclass
class TokenInfo:
    """Token information container."""

    access_token: str
    refresh_token: str
    access_token_expires_at: int  # 毫秒时间戳
    refresh_token_expires_at: int  # 毫秒时间戳
    seller_id: str
    seller_name: str

    @property
    def access_token_expires_in_seconds(self) -> int:
        """Get access token expiration time in seconds from now."""
        return max(0, (self.access_token_expires_at - int(time.time() * 1000)) // 1000)

    @property
    def refresh_token_expires_in_seconds(self) -> int:
        """Get refresh token expiration time in seconds from now."""
        return max(0, (self.refresh_token_expires_at - int(time.time() * 1000)) // 1000)

    @property
    def is_access_token_expired(self) -> bool:
        """Check if access token is expired."""
        return self.access_token_expires_in_seconds <= 0

    @property
    def is_refresh_token_expired(self) -> bool:
        """Check if refresh token is expired."""
        return self.refresh_token_expires_in_seconds <= 0

    def should_refresh(self, buffer_seconds: int = 300) -> bool:
        """Check if token should be refreshed (expires within buffer_seconds)."""
        return self.access_token_expires_in_seconds <= buffer_seconds

    @classmethod
    def from_access_token_response(cls, response: GetAccessTokenResponse) -> TokenInfo:
        """Create TokenInfo from GetAccessTokenResponse."""
        return cls(
            access_token=response.access_token,
            refresh_token=response.refresh_token,
            access_token_expires_at=response.access_token_expires_at,
            refresh_token_expires_at=response.refresh_token_expires_at,
            seller_id=response.seller_id,
            seller_name=response.seller_name,
        )

    @classmethod
    def from_refresh_token_response(cls, response: RefreshTokenResponse) -> TokenInfo:
        """Create TokenInfo from RefreshTokenResponse."""
        return cls(
            access_token=response.access_token,
            refresh_token=response.refresh_token,
            access_token_expires_at=response.access_token_expires_at,
            refresh_token_expires_at=response.refresh_token_expires_at,
            seller_id=response.seller_id,
            seller_name=response.seller_name,
        )


class MemoryTokenStorage:
    """In-memory token storage implementation."""

    def __init__(self) -> None:
        self._tokens: Optional[TokenInfo] = None

    def load_tokens(self) -> Optional[TokenInfo]:
        """Load tokens from memory."""
        return self._tokens

    def save_tokens(self, tokens: TokenInfo) -> None:
        """Save tokens to memory."""
        self._tokens = tokens

    def clear_tokens(self) -> None:
        """Clear tokens from memory."""
        self._tokens = None


class FileTokenStorage:
    """File-based token storage implementation."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def load_tokens(self) -> Optional[TokenInfo]:
        """Load tokens from file."""
        try:
            if not os.path.exists(self.file_path):
                return None
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return TokenInfo(**data)
        except (FileNotFoundError, json.JSONDecodeError, TypeError):
            return None

    def save_tokens(self, tokens: TokenInfo) -> None:
        """Save tokens to file."""
        from dataclasses import asdict

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(asdict(tokens), f, ensure_ascii=False, indent=2)

    def clear_tokens(self) -> None:
        """Clear tokens from file."""
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass


# Type alias for authorization code provider
AuthCodeProvider = Callable[[], str]


class TokenManager:
    """Automatic token management system."""

    def __init__(
        self,
        oauth_client: OauthClient,
        storage: TokenStorage,
        auth_code_provider: Optional[AuthCodeProvider] = None,
        refresh_buffer_seconds: int = 300,  # 提前5分钟刷新
    ) -> None:
        self._oauth_client = oauth_client
        self._storage = storage
        self._auth_code_provider = auth_code_provider
        self._refresh_buffer_seconds = refresh_buffer_seconds
        self._lock = Lock()
        self._current_tokens: Optional[TokenInfo] = None

    def get_valid_access_token(self) -> str:
        """Get a valid access token, automatically refreshing if needed."""
        with self._lock:
            # 加载当前token
            if self._current_tokens is None:
                self._current_tokens = self._storage.load_tokens()

            # 如果没有token或刷新token过期，需要重新授权
            if (
                self._current_tokens is None
                or self._current_tokens.is_refresh_token_expired
            ):
                if self._auth_code_provider is None:
                    raise TokenManagerError(
                        "No valid tokens and no auth_code_provider configured. "
                        "Please provide an auth_code_provider or manually set tokens."
                    )
                self._obtain_initial_tokens()

            # 检查是否需要刷新access token
            if self._current_tokens is not None and self._current_tokens.should_refresh(
                self._refresh_buffer_seconds
            ):
                self._refresh_tokens()

            # 确保有有效的tokens
            if self._current_tokens is None:
                raise TokenManagerError("Failed to obtain valid tokens")

            return self._current_tokens.access_token

    def set_tokens_from_auth_code(self, auth_code: str) -> TokenInfo:
        """Set tokens using authorization code."""
        with self._lock:
            response = self._oauth_client.get_access_token(code=auth_code)
            if not response.success or response.data is None:
                raise TokenManagerError(
                    f"Failed to get access token: {response.error_message}"
                )

            self._current_tokens = TokenInfo.from_access_token_response(response.data)
            self._storage.save_tokens(self._current_tokens)
            return self._current_tokens

    def set_tokens_manually(self, tokens: TokenInfo) -> None:
        """Manually set tokens."""
        with self._lock:
            self._current_tokens = tokens
            self._storage.save_tokens(tokens)

    def clear_tokens(self) -> None:
        """Clear all tokens."""
        with self._lock:
            self._current_tokens = None
            self._storage.clear_tokens()

    def get_current_tokens(self) -> Optional[TokenInfo]:
        """Get current token information."""
        with self._lock:
            if self._current_tokens is None:
                self._current_tokens = self._storage.load_tokens()
            return self._current_tokens

    def _obtain_initial_tokens(self) -> None:
        """Obtain initial tokens using auth code provider."""
        if self._auth_code_provider is None:
            raise TokenManagerError("No auth_code_provider configured")

        auth_code = self._auth_code_provider()
        response = self._oauth_client.get_access_token(code=auth_code)
        if not response.success or response.data is None:
            raise TokenManagerError(
                f"Failed to get access token: {response.error_message}"
            )

        self._current_tokens = TokenInfo.from_access_token_response(response.data)
        self._storage.save_tokens(self._current_tokens)

    def _refresh_tokens(self) -> None:
        """Refresh access token using refresh token."""
        if self._current_tokens is None:
            raise TokenManagerError("No current tokens to refresh")

        response = self._oauth_client.refresh_token(
            refresh_token=self._current_tokens.refresh_token
        )
        if not response.success or response.data is None:
            # 刷新失败，可能refresh token也过期了，清除tokens
            self.clear_tokens()
            raise TokenManagerError(
                f"Failed to refresh token: {response.error_message}"
            )

        self._current_tokens = TokenInfo.from_refresh_token_response(response.data)
        self._storage.save_tokens(self._current_tokens)


class TokenManagerError(Exception):
    """Token manager related errors."""

    pass
