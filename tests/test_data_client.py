import json

import httpx

from xiaohongshu_ecommerce.client import XhsClient
from xiaohongshu_ecommerce.config import ClientConfig
from xiaohongshu_ecommerce.models.data import (
    DecryptItem,
)


def test_data_batch_decrypt(monkeypatch):
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

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "data.batchDecrypt"
        assert payload["accessToken"] == "access-token"
        assert payload["appId"] == config.app_id
        assert payload["timestamp"] == str(fixed_timestamp)
        assert payload["version"] == config.version
        assert payload["actionType"] == "test"
        assert payload["appUserId"] == "user-1"
        assert isinstance(payload["baseInfos"], list)
        assert payload["baseInfos"][0]["dataTag"] == "phone"
        assert payload["baseInfos"][0]["encryptedData"] == "abc123"

        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "dataInfoList": [
                        {
                            "dataTag": "phone",
                            "encryptedData": "abc123",
                            "decryptedData": "13000000000",
                            "errorCode": 0,
                            "errorMsg": "",
                            "virtualNumberFlag": False,
                        }
                    ]
                },
            },
        )

    transport = httpx.MockTransport(handler)
    session = httpx.Client(transport=transport)
    client = XhsClient(config=config, session=session)

    result = client.data.batch_decrypt(
        base_infos=[DecryptItem(data_tag="phone", encrypted_data="abc123")],
        action_type="test",
        app_user_id="user-1",
    )

    assert result.success is True
    assert result.data
    assert result.data.data_info_list[0].decrypted_data == "13000000000"

    client.close()


def test_data_batch_decrypt_error(monkeypatch):
    monkeypatch.setattr(
        "xiaohongshu_ecommerce.client.base.utc_timestamp",
        lambda: 1700000000,
    )

    config = ClientConfig(
        base_url="https://openapi.xiaohongshu.com",
        app_id="test-app",
        app_secret="secret-key",
        version="1.0",
    )

    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "success": False,
                "error_code": "10001",
                "error_msg": "invalid data",
            },
        )

    transport = httpx.MockTransport(handler)
    session = httpx.Client(transport=transport)
    client = XhsClient(config=config, session=session)

    result = client.data.batch_decrypt(
        base_infos=[DecryptItem(data_tag="phone", encrypted_data="abc123")],
        action_type="test",
        app_user_id="user-1",
    )

    assert result.success is False
    assert result.code == "10001"
    assert result.data is None

    client.close()
