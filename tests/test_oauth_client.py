import json

import httpx

from xiaohongshu_ecommerce.client import XhsClient
from xiaohongshu_ecommerce.config import ClientConfig
from xiaohongshu_ecommerce.models.oauth import (
    TokenResponse,
)
from xiaohongshu_ecommerce.signing import build_signature


def test_oauth_get_access_token(monkeypatch):
    fixed_timestamp = 1700000000
    monkeypatch.setattr(
        "xiaohongshu_ecommerce.client.base.utc_timestamp",
        lambda: fixed_timestamp,
    )

    config = ClientConfig(
        base_url="https://openapi.xiaohongshu.com",
        app_id="test-app",
        app_secret="secret-key",
        version="1.0",
    )

    expected_signature = build_signature(
        method="oauth.getAccessToken",
        app_id=config.app_id,
        timestamp=str(fixed_timestamp),
        version=config.version,
        app_secret=config.app_secret,
    )

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "oauth.getAccessToken"
        assert payload["code"] == "auth-code"
        assert payload["appId"] == config.app_id
        assert payload["timestamp"] == str(fixed_timestamp)
        assert payload["version"] == config.version
        assert payload["sign"] == expected_signature

        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "accessToken": "token-1",
                    "accessTokenExpiresAt": 7200,
                    "refreshToken": "refresh-1",
                    "refreshTokenExpiresAt": 86400,
                    "sellerId": "seller-123",
                    "sellerName": "示例商家",
                },
            },
        )

    transport = httpx.MockTransport(handler)
    session = httpx.Client(transport=transport)
    client = XhsClient(config=config, session=session)

    response = client.oauth.get_access_token(code="auth-code")

    assert response.success is True
    assert isinstance(response.data, TokenResponse)
    assert response.data.access_token == "token-1"
    assert response.data.refresh_token == "refresh-1"
    assert response.data.seller_id == "seller-123"

    client.close()
