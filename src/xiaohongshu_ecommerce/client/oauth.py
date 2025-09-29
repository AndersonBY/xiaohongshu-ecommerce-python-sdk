"""OAuth authentication client for Xiaohongshu e-commerce API."""

from __future__ import annotations

from typing import Any, Optional, Type

import httpx

from .base import SyncSubClient
from ..models.base import BaseRequest, BaseResponse
from ..models.oauth import (
    GetAccessTokenRequest,
    GetAccessTokenResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
)
from ..utils import json_dumps
from ..errors import OpenSdkErrorCode, OpenSdkException


class OauthClient(SyncSubClient):
    """授权认证和令牌管理的同步客户端。

    OAuth系统处理小红书电商API访问的认证和授权。
    此客户端管理完整的OAuth流程，包括访问令牌生成、令牌刷新和认证生命周期管理。
    """

    def get_access_token(self, code: str) -> BaseResponse[GetAccessTokenResponse]:
        """获取访问令牌 (API: oauth.getAccessToken).

        使用授权码换取访问令牌和刷新令牌。这是OAuth授权流程的最后一步，
        提供API访问所需的凭据。

        授权流程说明:
            1. Web端授权: 引导用户访问授权页面
               https://ark.xiaohongshu.com/ark/authorization?appId=xxx&redirectUri=xxx&state=xxx

            2. 移动端授权: 生成二维码供小红书千帆APP扫码授权
               https://ark.xiaohongshu.com/thor/open/authorization?fullscreen=true&appId=xxx&sellerId=xxx&redirectUri=xxx

            3. 获取授权码: 用户完成授权后，code将回调到redirectUri
               https://{回调地址}/?code=74afa4f59c404***089e9db87797d6cc&state=1234

            4. 换取令牌: 使用授权码调用此方法获取访问令牌

        Args:
            code (str): 从OAuth授权回调中获得的授权码 (必需)
                      - 有效期10分钟，过期需重新授权
                      - 短时间内多次使用同一code换取的token相同

        Returns:
            BaseResponse[GetAccessTokenResponse]: 响应包含:
                - accessToken (str): API认证访问令牌 (有效期7天)
                - accessTokenExpiresAt (int): 访问令牌过期时间戳 (毫秒)
                - refreshToken (str): 用于刷新过期访问令牌的令牌 (有效期14天)
                - refreshTokenExpiresAt (int): 刷新令牌过期时间戳 (毫秒)
                - sellerId (str): 已认证商家标识符
                - sellerName (str): 已认证商家名称

        Examples:
            >>> # Web端授权流程
            >>> # 1. 引导用户访问授权页面
            >>> auth_url = f"https://ark.xiaohongshu.com/ark/authorization?" \
            ...           f"appId={app_id}&redirectUri={redirect_uri}&state=12345"
            >>> print(f"请访问: {auth_url}")
            >>>
            >>> # 2. 用户授权后从回调地址获取code
            >>> auth_code = "code-9e28279***e6035dc686e0-7aaea***841f3b32"
            >>>
            >>> # 3. 使用授权码换取令牌
            >>> response = client.oauth.get_access_token(code=auth_code)
            >>>
            >>> if response.success:
            ...     token_info = response.data
            ...     access_token = token_info.accessToken
            ...     refresh_token = token_info.refreshToken
            ...     expires_at = token_info.accessTokenExpiresAt
            ...     seller_id = token_info.sellerId
            ...
            ...     # 安全存储令牌以备将来API调用
            ...     print(f"为商家获得访问令牌: {token_info.sellerName}")
            ...     print(f"商家ID: {seller_id}")
            ...     print(f"令牌过期时间: {expires_at}")

        Note:
            - 只允许店铺主账号授权成功，子账号无法完成授权
            - 授权码是一次性使用的，且快速过期（10分钟）
            - 访问令牌有效期7天，刷新令牌有效期14天
            - 安全存储两个令牌并实施适当的令牌轮换
            - 此操作不需要现有的访问令牌
            - 商家可在账号应用管理处查看和取消授权应用
        """
        request = GetAccessTokenRequest(code=code)
        return self._execute_oauth(request, response_model=GetAccessTokenResponse)

    def refresh_token(self, refresh_token: str) -> BaseResponse[RefreshTokenResponse]:
        """刷新访问令牌 (API: oauth.refreshToken).

        使用有效的刷新令牌获取新的访问令牌。此操作可以在不需要用户重新认证的情况下
        延长API访问权限，应在访问令牌过期前执行。

        Args:
            refresh_token (str): 有效的刷新令牌 (必需)

        Returns:
            BaseResponse[RefreshTokenResponse]: 响应包含:
                - accessToken (str): 新的API认证访问令牌
                - accessTokenExpiresAt (int): 新访问令牌过期时间戳 (Unix)
                - refreshToken (str): 新的刷新令牌 (可能相同或已轮换)
                - refreshTokenExpiresAt (int): 刷新令牌过期时间戳 (Unix)
                - sellerId (str): 已认证商家标识符
                - sellerName (str): 已认证商家名称

        Examples:
            >>> # 刷新过期的访问令牌
            >>> # 使用存储的刷新令牌
            >>> stored_refresh_token = "refresh-72df8ba***e1387407ac-944bad***94df5ae1"
            >>>
            >>> response = client.oauth.refresh_token(refresh_token=stored_refresh_token)
            >>>
            >>> if response.success:
            ...     new_tokens = response.data
            ...     new_access_token = new_tokens.accessToken
            ...     new_refresh_token = new_tokens.refreshToken
            ...     new_expires_at = new_tokens.accessTokenExpiresAt
            ...
            ...     # 更新存储的令牌
            ...     print(f"为商家刷新令牌: {new_tokens.sellerName}")
            ...     print(f"新令牌过期时间: {new_expires_at}")

            >>> # 在过期前主动刷新令牌
            >>> import time
            >>> current_time = int(time.time())
            >>>
            >>> # 检查令牌是否在下一小时内过期
            >>> if stored_token_expires_at - current_time < 3600:
            ...     response = client.oauth.refresh_token(refresh_token=stored_refresh_token)
            ...
            ...     if response.success:
            ...         # 更新存储的凭据
            ...         update_stored_tokens(response.data)

        Token刷新规则:
            - accessToken有效期为7天，refreshToken有效时间为14天
            - accessToken未过期且剩余有效时间大于30分钟时，刷新后令牌均不会变化
            - accessToken未过期且剩余有效时间小于30分钟时，会得到新的令牌，旧accessToken有效期为5分钟
            - accessToken过期后使用refreshToken刷新会得到新的令牌
            - refreshToken过期后需要用户重新授权

        Note:
            为安全起见，刷新令牌可能会轮换（提供新的刷新令牌）。
            成功刷新后始终更新访问令牌和刷新令牌。
            在访问令牌过期前实施自动令牌刷新。
            此操作不需要现有的访问令牌。
        """
        request = RefreshTokenRequest(refresh_token=refresh_token)
        return self._execute_oauth(request, response_model=RefreshTokenResponse)

    def _execute_oauth(
        self,
        request: BaseRequest,
        *,
        response_model: Optional[Type[Any]] = None,
    ) -> BaseResponse[Any]:
        """Execute OAuth request without access token requirement."""
        prepared = self._client.prepare_request(request, access_token=None)
        payload = json_dumps(prepared)
        try:
            http_response = self.session.post(self.config.base_url, content=payload)
        except httpx.RequestError as exc:
            raise OpenSdkException(OpenSdkErrorCode.NETWORK_ERROR, str(exc)) from exc
        return self._client.handle_response(
            http_response, response_model=response_model
        )
