"""Xiaohongshu e-commerce Python SDK (synchronous client).

This SDK provides a comprehensive interface to the Xiaohongshu (Little Red Book)
e-commerce platform APIs with automatic token management.

Basic Usage:
    >>> from xiaohongshu_ecommerce import XhsClient, ClientConfig
    >>> from xiaohongshu_ecommerce import FileTokenStorage
    >>>
    >>> # Configure client with automatic token management
    >>> config = ClientConfig(
    ...     base_url="https://openapi.xiaohongshu.com",
    ...     app_id="your_app_id",
    ...     app_secret="your_app_secret",
    ...     token_storage=FileTokenStorage("tokens.json")
    ... )
    >>> client = XhsClient.create(config)
    >>> client.set_tokens_from_auth_code("auth_code")
    >>>
    >>> # No need to pass access_token - handled automatically!
    >>> products = client.product.get_detail_sku_list(page_no=1, page_size=20)
"""

__version__ = "0.1.0"

from .client import XhsClient
from .config import ClientConfig
from .errors import OpenSdkException, OpenSdkErrorCode
from .token_manager import (
    TokenManager,
    TokenInfo,
    MemoryTokenStorage,
    FileTokenStorage,
    TokenManagerError,
)

__all__ = [
    "ClientConfig",
    "XhsClient",
    "OpenSdkException",
    "OpenSdkErrorCode",
    "TokenManager",
    "TokenInfo",
    "MemoryTokenStorage",
    "FileTokenStorage",
    "TokenManagerError",
]
