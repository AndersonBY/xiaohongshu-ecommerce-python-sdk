import json
from typing import Any, Dict

import httpx

from xiaohongshu_ecommerce.client import XhsClient
from xiaohongshu_ecommerce.config import ClientConfig
from xiaohongshu_ecommerce.models.boutique import (
    BoutiqueItemBatchInfo,
    BoutiqueMode,
    StockOperateInfo,
)


def _build_client(monkeypatch, handler):
    import time

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
    transport = httpx.MockTransport(handler)
    session = httpx.Client(transport=transport)
    client = XhsClient(config=config, session=session)

    # Set test tokens for automatic token management with future expiration
    current_time_ms = int(time.time() * 1000)
    client.set_tokens_manually(
        access_token="test_access_token",
        refresh_token="test_refresh_token",
        access_token_expires_at=current_time_ms + (3600 * 1000),  # 1 hour from now
        refresh_token_expires_at=current_time_ms + (7200 * 1000),  # 2 hours from now
        seller_id="test_seller",
        seller_name="Test Seller",
    )

    return client


def test_create_boutique_item(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "boutique.createBoutiqueItem"
        assert payload["spuId"] == "spu-1"
        assert payload["withItemDetail"] is True
        assert payload["boutiqueModes"] == [BoutiqueMode.DOMESTIC_FAST_SHIPPING.value]
        return httpx.Response(200, json={"success": True, "data": {"itemId": "item-1"}})

    client = _build_client(monkeypatch, handler)
    response = client.boutique.create_item(
        spu_id="spu-1",
        boutique_modes=[BoutiqueMode.DOMESTIC_FAST_SHIPPING],
        with_item_detail=True,
    )

    assert response.success is True
    resp_data = response.data
    assert resp_data is not None
    assert resp_data.data["itemId"] == "item-1"

    client.close()


def test_update_boutique_item(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "boutique.updateBoutiqueItem"
        assert payload["boutiqueItemBatchInfo"]["qty"] == 10
        return httpx.Response(200, json={"success": True, "data": {"name": "Updated"}})

    client = _build_client(monkeypatch, handler)
    response = client.boutique.update_item(
        item_id="item-1", boutique_item_batch_info=BoutiqueItemBatchInfo(qty=10)
    )

    assert response.success is True
    resp_data = response.data
    assert resp_data is not None
    assert resp_data.name == "Updated"

    client.close()


def test_create_boutique_sku(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "boutique.createBoutiqueSku"
        assert payload["itemId"] == "item-1"
        return httpx.Response(200, json={"success": True, "data": {"skuId": "sku-1"}})

    client = _build_client(monkeypatch, handler)
    response = client.boutique.create_sku(
        item_id="item-1", boutique_modes=[BoutiqueMode.DOMESTIC_GENERAL_SHIPPING]
    )

    assert response.success is True
    resp_data = response.data
    assert resp_data is not None
    assert resp_data.data["skuId"] == "sku-1"

    client.close()


def test_update_boutique_sku(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "boutique.updateBoutiqueSku"
        assert payload["operateInfo"]["operateType"] == 1
        return httpx.Response(200, json={"success": True, "data": {"price": 19.9}})

    client = _build_client(monkeypatch, handler)
    response = client.boutique.update_sku(
        sku_id="sku-1", operate_info=StockOperateInfo(operate_type=1)
    )

    assert response.success is True
    resp_data = response.data
    assert resp_data is not None
    assert resp_data.price == 19.9

    client.close()


def test_create_item_v2_passthrough(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "boutique.createBoutiqueItemV2"
        assert payload["custom"] == "payload"
        return httpx.Response(200, json={"success": True, "data": {"ok": True}})

    from xiaohongshu_ecommerce.models import BaseRequest

    class PayloadRequest(BaseRequest):
        def __init__(self) -> None:
            super().__init__(method="boutique.createBoutiqueItemV2")

        def extra_payload(self) -> Dict[str, Any]:
            return {"custom": "payload"}

    client = _build_client(monkeypatch, handler)
    response = client.boutique.create_item_v2(PayloadRequest())

    assert response.success is True
    resp_data = response.data
    assert resp_data is not None
    assert resp_data["ok"] is True

    client.close()
