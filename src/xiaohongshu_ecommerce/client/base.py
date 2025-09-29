"""Base synchronous client implementations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, Optional, Type, cast

import httpx

from ..config import ClientConfig
from ..errors import OpenSdkErrorCode, OpenSdkException
from ..models import BaseRequest, BaseResponse
from ..utils import json_dumps
from ..utils.serialization import coerce_type
from ..utils.datetime import utc_timestamp
from ..signing import build_signature

if TYPE_CHECKING:  # pragma: no cover - type checking only
    from .after_sale import AfterSaleClient
    from .boutique import BoutiqueClient
    from .common import CommonClient
    from .data import DataClient
    from .delivery_voucher import DeliveryVoucherClient
    from .express import ExpressClient
    from .finance import FinanceClient
    from .instant_shopping import InstantShoppingClient
    from .inventory import InventoryClient
    from .invoice import InvoiceClient
    from .material import MaterialClient
    from .oauth import OauthClient
    from .order import OrderClient
    from .package import PackageClient
    from .product import ProductClient
    from ..token_manager import TokenManager, TokenInfo


class SyncSubClient:
    """Base class for concrete synchronous API clients."""

    def __init__(self, client: "XhsClient") -> None:
        self._client = client

    @property
    def config(self) -> ClientConfig:
        return self._client.config

    @property
    def session(self) -> httpx.Client:
        return self._client.session

    def _execute(
        self,
        request: BaseRequest,
        *,
        response_model: Optional[Type[Any]] = None,
    ) -> BaseResponse[Any]:
        """Execute API request with automatic token management.

        Args:
            request: The API request object
            response_model: Expected response model type

        Returns:
            API response

        Raises:
            OpenSdkException: If token cannot be obtained
        """
        try:
            access_token = self._client.token_manager.get_valid_access_token()
        except Exception as e:
            raise OpenSdkException(
                OpenSdkErrorCode.AUTH_ERROR, f"Failed to get valid access token: {e}"
            ) from e

        prepared = self._client.prepare_request(request, access_token)
        payload = json_dumps(prepared)
        try:
            http_response = self.session.post(self.config.base_url, content=payload)
        except httpx.RequestError as exc:
            raise OpenSdkException(OpenSdkErrorCode.NETWORK_ERROR, str(exc)) from exc
        return self._client.handle_response(
            http_response, response_model=response_model
        )


@dataclass
class XhsClient:
    """Entry point for synchronous Xiaohongshu API usage."""

    config: ClientConfig
    session: httpx.Client
    _subclients: Dict[str, SyncSubClient] = field(default_factory=dict, init=False)
    token_manager: "TokenManager" = field(init=False)

    def __post_init__(self) -> None:
        self.session.headers.update({"Content-Type": "application/json; charset=utf-8"})
        self.session.headers.update(self.config.headers)

        # 初始化TokenManager（始终启用）
        self._initialize_token_manager()

    def _initialize_token_manager(self) -> None:
        """Initialize token manager."""
        from ..token_manager import TokenManager, MemoryTokenStorage

        # 使用提供的storage或默认的内存storage
        storage = self.config.token_storage
        if storage is None:
            storage = MemoryTokenStorage()

        self.token_manager = TokenManager(
            oauth_client=self.oauth,
            storage=storage,
            auth_code_provider=self.config.auth_code_provider,
            refresh_buffer_seconds=self.config.token_refresh_buffer_seconds,
        )

    @classmethod
    def create(cls, config: ClientConfig) -> "XhsClient":
        timeout = httpx.Timeout(
            timeout=config.timeout,
            connect=config.connect_timeout,
        )
        session = httpx.Client(
            timeout=timeout,
            proxy=config.proxy,
            headers=config.headers,
        )
        return cls(config=config, session=session)

    def prepare_request(
        self,
        request: BaseRequest,
        access_token: Optional[str],
    ) -> Dict[str, Any]:
        request.app_id = self.config.app_id
        request.timestamp = str(utc_timestamp())
        request.version = self.config.version
        request.set_access_token(access_token)
        request.sign = build_signature(
            method=request.method,
            app_id=request.app_id,
            timestamp=request.timestamp,
            version=request.version,
            app_secret=self.config.app_secret,
        )
        return request.to_payload()

    def handle_response(
        self,
        response: httpx.Response,
        *,
        response_model: Optional[Type[Any]] = None,
    ) -> BaseResponse[Any]:
        if response.is_error:
            raise OpenSdkException(
                OpenSdkErrorCode.HTTP_ERROR,
                f"HTTP {response.status_code}: {response.text}",
            )

        body = response.json()
        if not isinstance(body, dict):
            raise OpenSdkException(OpenSdkErrorCode.SERIALIZATION_ERROR, "响应格式错误")

        success = bool(body.get("success"))
        code = body.get("code") or body.get("error_code")
        msg = body.get("msg") or body.get("error_msg")
        data = body.get("data")

        if success:
            deserialized = coerce_type(data, response_model) if response_model else data
            return BaseResponse(success=True, data=deserialized, code=code, msg=msg)

        return BaseResponse(success=False, data=None, code=code, msg=msg)

    def close(self) -> None:
        self.session.close()

    # Sub-client factories will be attached later (e.g., oauth, order, ...)
    @property
    def oauth(self) -> "OauthClient":
        client = self._subclients.get("oauth")
        if client is None:
            from .oauth import OauthClient

            client = OauthClient(self)
            self._subclients["oauth"] = client
        return cast("OauthClient", client)

    @property
    def data(self) -> "DataClient":
        client = self._subclients.get("data")
        if client is None:
            from .data import DataClient

            client = DataClient(self)
            self._subclients["data"] = client
        return cast("DataClient", client)

    @property
    def common(self) -> "CommonClient":
        client = self._subclients.get("common")
        if client is None:
            from .common import CommonClient

            client = CommonClient(self)
            self._subclients["common"] = client
        return cast("CommonClient", client)

    @property
    def inventory(self) -> "InventoryClient":
        client = self._subclients.get("inventory")
        if client is None:
            from .inventory import InventoryClient

            client = InventoryClient(self)
            self._subclients["inventory"] = client
        return cast("InventoryClient", client)

    @property
    def after_sale(self) -> "AfterSaleClient":
        client = self._subclients.get("after_sale")
        if client is None:
            from .after_sale import AfterSaleClient

            client = AfterSaleClient(self)
            self._subclients["after_sale"] = client
        return cast("AfterSaleClient", client)

    @property
    def boutique(self) -> "BoutiqueClient":
        client = self._subclients.get("boutique")
        if client is None:
            from .boutique import BoutiqueClient

            client = BoutiqueClient(self)
            self._subclients["boutique"] = client
        return cast("BoutiqueClient", client)

    @property
    def product(self) -> "ProductClient":
        client = self._subclients.get("product")
        if client is None:
            from .product import ProductClient

            client = ProductClient(self)
            self._subclients["product"] = client
        return cast("ProductClient", client)

    @property
    def order(self) -> "OrderClient":
        client = self._subclients.get("order")
        if client is None:
            from .order import OrderClient

            client = OrderClient(self)
            self._subclients["order"] = client
        return cast("OrderClient", client)

    @property
    def package(self) -> "PackageClient":
        client = self._subclients.get("package")
        if client is None:
            from .package import PackageClient

            client = PackageClient(self)
            self._subclients["package"] = client
        return cast("PackageClient", client)

    @property
    def express(self) -> "ExpressClient":
        client = self._subclients.get("express")
        if client is None:
            from .express import ExpressClient

            client = ExpressClient(self)
            self._subclients["express"] = client
        return cast("ExpressClient", client)

    @property
    def finance(self) -> "FinanceClient":
        client = self._subclients.get("finance")
        if client is None:
            from .finance import FinanceClient

            client = FinanceClient(self)
            self._subclients["finance"] = client
        return cast("FinanceClient", client)

    @property
    def invoice(self) -> "InvoiceClient":
        client = self._subclients.get("invoice")
        if client is None:
            from .invoice import InvoiceClient

            client = InvoiceClient(self)
            self._subclients["invoice"] = client
        return cast("InvoiceClient", client)

    @property
    def material(self) -> "MaterialClient":
        client = self._subclients.get("material")
        if client is None:
            from .material import MaterialClient

            client = MaterialClient(self)
            self._subclients["material"] = client
        return cast("MaterialClient", client)

    @property
    def delivery_voucher(self) -> "DeliveryVoucherClient":
        client = self._subclients.get("delivery_voucher")
        if client is None:
            from .delivery_voucher import DeliveryVoucherClient

            client = DeliveryVoucherClient(self)
            self._subclients["delivery_voucher"] = client
        return cast("DeliveryVoucherClient", client)

    @property
    def instant_shopping(self) -> "InstantShoppingClient":
        client = self._subclients.get("instant_shopping")
        if client is None:
            from .instant_shopping import InstantShoppingClient

            client = InstantShoppingClient(self)
            self._subclients["instant_shopping"] = client
        return cast("InstantShoppingClient", client)

    # Token management convenience methods
    def set_tokens_from_auth_code(self, auth_code: str) -> "TokenInfo":
        """Set tokens using authorization code.

        Args:
            auth_code: Authorization code from OAuth flow

        Returns:
            Token information

        Raises:
            TokenManagerError: If setting tokens fails
        """
        return self.token_manager.set_tokens_from_auth_code(auth_code)

    def set_tokens_manually(
        self,
        access_token: str,
        refresh_token: str,
        access_token_expires_at: int,
        refresh_token_expires_at: int,
        seller_id: str,
        seller_name: str,
    ) -> None:
        """Manually set tokens.

        Args:
            access_token: Access token
            refresh_token: Refresh token
            access_token_expires_at: Access token expiration timestamp (milliseconds)
            refresh_token_expires_at: Refresh token expiration timestamp (milliseconds)
            seller_id: Seller ID
            seller_name: Seller name
        """
        from ..token_manager import TokenInfo

        tokens = TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires_at=access_token_expires_at,
            refresh_token_expires_at=refresh_token_expires_at,
            seller_id=seller_id,
            seller_name=seller_name,
        )
        self.token_manager.set_tokens_manually(tokens)

    def get_current_tokens(self) -> Optional["TokenInfo"]:
        """Get current token information.

        Returns:
            Current token information if available
        """
        return self.token_manager.get_current_tokens()

    def clear_tokens(self) -> None:
        """Clear all stored tokens."""
        self.token_manager.clear_tokens()

    def is_token_valid(self) -> bool:
        """Check if current token is valid and not expired.

        Returns:
            True if token is valid, False otherwise
        """
        tokens = self.token_manager.get_current_tokens()
        if tokens is None:
            return False
        return not tokens.is_access_token_expired
