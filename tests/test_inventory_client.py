import json
from typing import Any, Dict

import httpx

from xiaohongshu_ecommerce.client import XhsClient
from xiaohongshu_ecommerce.config import ClientConfig


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


def test_get_item_stock(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "inventory.getItemStock"
        assert payload["itemId"] == "item-1"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "itemId": "item-1",
                    "itemStock": {
                        "available": 5,
                        "standalone": 1,
                        "reserved": 2,
                        "total": 8,
                    },
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.inventory.get_item_stock(item_id="item-1")

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.item_id == "item-1"
    assert data.item_stock.available == 5

    client.close()


def test_sync_sku_stock_v2(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload: Dict[str, Any] = json.loads(request.content.decode())
        assert payload["method"] == "inventory.syncSkuStockV2"
        assert payload["qtyWithWhcode"] == {"WH1": 10, "WH2": 5}
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "response": {"success": True, "msg": "ok", "code": 0},
                    "apiVersion": "v2",
                    "skuStockInfo": {
                        "skuId": "sku-1",
                        "skuStockInfo": {"available": 15, "total": 20},
                    },
                    "data": {
                        "WH1": {
                            "skuId": "sku-1",
                            "whcode": "WH1",
                            "skuStockInfo": {"available": 10},
                        },
                    },
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.inventory.sync_sku_stock_v2(
        sku_id="sku-1", qty_with_whcode={"WH1": 10, "WH2": 5}
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.api_version == "v2"
    assert data.sku_stock_info is not None
    assert data.sku_stock_info.sku_stock_info is not None
    assert data.sku_stock_info.sku_stock_info.available == 15
    assert "WH1" in data.data
    wh1 = data.data["WH1"]
    assert wh1.sku_stock_info is not None
    assert wh1.sku_stock_info.available == 10

    client.close()


def test_list_warehouse(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "warehouse.list"
        assert payload["pageNo"] == 2
        assert payload["name"] == "Test Warehouse"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "total": 1,
                    "warehouseList": [
                        {
                            "code": "WH1",
                            "name": "Test Warehouse",
                            "province": "Zhejiang",
                            "city": "Hangzhou",
                        }
                    ],
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.inventory.list_warehouse(page_no=2, name="Test Warehouse")

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.total == 1
    assert data.warehouse_list[0].code == "WH1"
    assert data.warehouse_list[0].city == "Hangzhou"

    client.close()


def test_set_warehouse_priority(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "warehouse.setPriority"
        assert payload["zoneCode"] == "ZJ"
        assert payload["warehousePriorityList"] == [
            {"whCode": "WH1"},
            {"whCode": "WH2"},
        ]
        return httpx.Response(200, json={"success": True, "data": "ok"})

    client = _build_client(monkeypatch, handler)
    response = client.inventory.set_warehouse_priority(
        zone_code="ZJ", warehouse_priority_list=[{"whCode": "WH1"}, {"whCode": "WH2"}]
    )

    assert response.success is True
    assert response.data == "ok"

    client.close()


def test_create_warehouse(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "warehouse.create"
        assert payload["code"] == "WH1"
        assert payload["zoneCode"] == "330100"
        return httpx.Response(200, json={"success": True, "data": "ok"})

    client = _build_client(monkeypatch, handler)
    response = client.inventory.create_warehouse(
        code="WH1",
        name="Test Warehouse",
        zone_code="330100",
        address="No.1 Road",
        contact_name="Alice",
        contact_tel="13800000000",
    )

    assert response.success is True
    assert response.data == "ok"

    client.close()
