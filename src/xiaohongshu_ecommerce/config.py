"""Client configuration dataclasses and helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, MutableMapping, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .token_manager import TokenStorage, AuthCodeProvider


@dataclass(frozen=True)
class ClientConfig:
    """Immutable configuration for the Xiaohongshu API client."""

    base_url: str
    app_id: str
    app_secret: str
    version: str = "1.0"
    timeout: float = 30.0
    connect_timeout: float = 5.0
    proxies: Optional[Union[str, MutableMapping[str, str]]] = None
    headers: Dict[str, str] = field(default_factory=dict)

    # Token management configuration
    token_storage: Optional["TokenStorage"] = None
    auth_code_provider: Optional["AuthCodeProvider"] = None
    token_refresh_buffer_seconds: int = 300  # 提前5分钟刷新token

    def with_headers(self, **headers: str) -> "ClientConfig":
        merged = {**self.headers, **headers}
        return ClientConfig(
            base_url=self.base_url,
            app_id=self.app_id,
            app_secret=self.app_secret,
            version=self.version,
            timeout=self.timeout,
            connect_timeout=self.connect_timeout,
            proxies=self.proxies,
            headers=merged,
            token_storage=self.token_storage,
            auth_code_provider=self.auth_code_provider,
            token_refresh_buffer_seconds=self.token_refresh_buffer_seconds,
        )

    @property
    def proxy(self) -> Optional[str]:
        """Return a proxy string compatible with httpx.Client."""

        value = self.proxies
        if value is None or isinstance(value, str):
            return value
        if not value:
            return None
        return value.get("https") or value.get("http") or next(iter(value.values()))
