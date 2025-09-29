import json
from typing import Any, Dict

import httpx

from xiaohongshu_ecommerce.client import XhsClient
from xiaohongshu_ecommerce.config import ClientConfig
from xiaohongshu_ecommerce.models.product import (
    ItemDetailV3,
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


def test_get_basic_item_list(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.getBasicItemList"
        assert payload["pageNo"] == 2
        assert payload["pageSize"] == 20
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "currentPage": 2,
                    "pageSize": 20,
                    "total": 40,
                    "hits": [
                        {
                            "itemId": "item-1",
                            "name": "测试商品",
                            "spuId": "spu-1",
                            "price": 129.9,
                            "stock": 10,
                            "status": 1,
                        }
                    ],
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.get_basic_item_list(
        page_no=2,
        page_size=20,
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.page.current_page == 2
    assert data.hits[0].item_id == "item-1"

    client.close()


def test_get_detail_item_list(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.getDetailItemList"
        assert payload["itemIds"] == ["item-1"]
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "currentPage": 1,
                    "pageSize": 10,
                    "total": 1,
                    "data": [
                        {
                            "spuData": {"id": "spu-1", "name": "SPU"},
                            "itemData": {"itemId": "item-1", "name": "Item"},
                        }
                    ],
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.get_detail_item_list(
        item_ids=["item-1"],
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.items[0].item is not None
    assert data.items[0].item.item_id == "item-1"

    client.close()


def test_get_detail_sku_list(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.getDetailSkuList"
        assert payload["pageNo"] == 1
        return httpx.Response(200, json={"success": True, "data": {"pageNO": 1}})

    client = _build_client(monkeypatch, handler)
    response = client.product.get_detail_sku_list(
        page_no=1,
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data["pageNO"] == 1

    client.close()


def test_get_spu_info(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.getSpuInfo"
        assert payload["spuId"] == "spu-1"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {"id": "spu-1", "name": "SPU"},
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.get_spu_info("spu-1")

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.spu.spu_id == "spu-1"

    client.close()


def test_get_item_info(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.getItemInfo"
        assert payload["itemId"] == "item-1"
        return httpx.Response(
            200, json={"success": True, "data": {"itemInfo": {"id": "item-1"}}}
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.get_item_info(
        item_id="item-1",
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data["itemInfo"]["id"] == "item-1"

    client.close()


def test_search_item_list(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.searchItemList"
        assert payload["searchParam"]["keyword"] == "test"
        return httpx.Response(200, json={"success": True, "data": {"total": 1}})

    client = _build_client(monkeypatch, handler)
    response = client.product.search_item_list(
        search_param={"keyword": "test"},
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data["total"] == 1

    client.close()


def test_update_logistics_plan(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload: Dict[str, Any] = json.loads(request.content.decode())
        assert payload["method"] == "product.updateLogisticsPlan"
        assert payload["itemId"] == "item-1"
        assert payload["logisticsPlanId"] == "plan-1"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {"itemId": "item-1", "logisticsPlanId": "plan-1"},
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.update_logistics_plan(
        "item-1",
        "plan-1",
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.logistics_plan_id == "plan-1"

    client.close()


def test_update_availability(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.updateAvailability"
        assert payload["available"] is False
        return httpx.Response(
            200,
            json={"success": True, "data": {"itemId": "item-1", "available": False}},
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.update_availability(
        "item-1",
        False,
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.available is False

    client.close()


def test_create_spu(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.createSpu"
        assert payload["spu"]["name"] == "SPU"
        return httpx.Response(
            200,
            json={"success": True, "data": {"spuId": "spu-1"}},
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.create_spu(
        {"name": "SPU", "brandId": "brand-1"},
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.spu_id == "spu-1"

    client.close()


def test_update_spu(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.updateSpu"
        assert payload["spuId"] == "spu-1"
        assert payload["name"] == "Updated"
        return httpx.Response(
            200,
            json={"success": True, "data": {"spuId": "spu-1"}},
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.update_spu(
        "spu-1",
        {"name": "Updated"},
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.spu_id == "spu-1"

    client.close()


def test_delete_spu(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.deleteSpu"
        assert payload["spuIds"] == ["spu-1"]
        return httpx.Response(
            200,
            json={"success": True, "data": {"deleted": ["spu-1"]}},
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.delete_spu(
        ["spu-1"],
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.deleted == ["spu-1"]

    client.close()


def test_create_item(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.createItem"
        assert payload["spuId"] == "spu-1"
        assert payload["price"] == 199.0
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "spuData": {"id": "spu-1"},
                    "itemData": {"itemId": "item-99"},
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.create_item(
        "spu-1",
        price=199.0,
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.item is not None
    assert data.item.item_id == "item-99"

    client.close()


def test_update_item(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.updateItem"
        assert payload["id"] == "item-1"
        assert payload["price"] == 109.0
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "spuData": {"id": "spu-1"},
                    "itemData": {"itemId": "item-1", "price": 109.0},
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.update_item(
        "item-1",
        extra={"price": 109.0},
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.item is not None
    assert data.item.price == 109.0

    client.close()


def test_delete_item(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.deleteItem"
        assert payload["id"] == "item-1"
        return httpx.Response(200, json={"success": True, "data": "ok"})

    client = _build_client(monkeypatch, handler)
    response = client.product.delete_item(
        "item-1",
    )

    assert response.success is True
    assert response.data == "ok"

    client.close()


def test_get_basic_spu(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.getBasicSpu"
        assert payload["pageNo"] == 1
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "currentPage": 1,
                    "pageSize": 10,
                    "total": 1,
                    "spuBasicInfos": [
                        {
                            "id": "spu-1",
                            "name": "SPU",
                            "minPrice": 10.0,
                            "maxPrice": 20.0,
                            "buyable": True,
                        }
                    ],
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.get_basic_spu(
        page_no=1,
        page_size=10,
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.page.current_page == 1
    assert data.spus[0].buyable is True

    client.close()


def test_update_item_price(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload: Dict[str, Any] = json.loads(request.content.decode())
        assert payload["method"] == "product.updateItemPrice"
        assert payload["itemId"] == "item-1"
        assert payload["price"][0]["itemId"] == "item-1"
        return httpx.Response(200, json={"success": True, "data": "updated"})

    client = _build_client(monkeypatch, handler)
    response = client.product.update_item_price(
        "item-1",
        price=[{"itemId": "item-1", "price": 99.9}],
    )

    assert response.success is True
    assert response.data == "updated"

    client.close()


def test_update_sku_logistics_plan(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.updateSkuLogisticsPlan"
        assert payload["skuId"] == "sku-1"
        assert payload["logisticsPlanId"] == "plan-1"
        return httpx.Response(200, json={"success": True, "data": {"ok": True}})

    client = _build_client(monkeypatch, handler)
    response = client.product.update_sku_logistics_plan(
        "sku-1",
        "plan-1",
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data["ok"] is True

    client.close()


def test_update_sku_price(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.updateSkuPrice"
        assert payload["price"][0]["skuId"] == "sku-1"
        return httpx.Response(200, json={"success": True, "data": "done"})

    client = _build_client(monkeypatch, handler)
    response = client.product.update_sku_price(
        "sku-1",
        [{"skuId": "sku-1", "price": 100}],
    )

    assert response.success is True
    assert response.data == "done"

    client.close()


def test_update_sku_available(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.updateSkuAvailable"
        assert payload["available"] is True
        return httpx.Response(200, json={"success": True, "data": "ok"})

    client = _build_client(monkeypatch, handler)
    response = client.product.update_sku_available(
        "sku-1",
        True,
    )

    assert response.success is True
    assert response.data == "ok"

    client.close()


def test_update_item_image(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.updateItemImage"
        assert payload["materialType"] == 1
        assert payload["materialUrls"] == ["https://img"]
        return httpx.Response(200, json={"success": True, "data": "image"})

    client = _build_client(monkeypatch, handler)
    response = client.product.update_item_image(
        "item-1",
        1,
        ["https://img"],
    )

    assert response.success is True
    assert response.data == "image"

    client.close()


def test_update_spu_image(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.updateSpuImage"
        assert payload["spuId"] == "spu-1"
        assert payload["materialUrls"] == ["https://img"]
        return httpx.Response(200, json={"success": True, "data": "spu"})

    client = _build_client(monkeypatch, handler)
    response = client.product.update_spu_image(
        "spu-1",
        image_urls=["https://img"],
    )

    assert response.success is True
    assert response.data == "spu"

    client.close()


def test_update_variant_image(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.updateVariantImage"
        assert payload["variantId"] == "var-1"
        assert payload["materialUrl"] == "https://img"
        return httpx.Response(200, json={"success": True, "data": "variant"})

    client = _build_client(monkeypatch, handler)
    response = client.product.update_variant_image(
        "var-1",
        image_url="https://img",
    )

    assert response.success is True
    assert response.data == "variant"

    client.close()


def test_create_item_v3(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.createItemV2"
        assert payload["name"] == "新品"
        assert payload["attributes"][0]["propertyId"] == "prop-1"
        assert payload["faq"][0]["question"] == "Q"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "id": "item-v3",
                    "createTime": 1700000001,
                    "updateTime": 1700000100,
                    "name": "新品",
                    "ename": "new-item",
                    "brandId": 123,
                    "categoryId": "cat-1",
                    "attributes": [
                        {
                            "propertyId": "prop-1",
                            "name": "颜色",
                            "value": "红",
                            "valueId": "val-1",
                            "valueList": [
                                {"valueId": "val-1", "value": "红"},
                            ],
                        }
                    ],
                    "shippingTemplateId": "ship-1",
                    "shippingGrossWeight": 500,
                    "variantIds": ["var-1"],
                    "images": ["https://img"],
                    "standardImages": ["https://std"],
                    "longImages": ["https://long"],
                    "videoUrl": "https://video",
                    "articleNo": "art-1",
                    "imageDescriptions": ["https://desc"],
                    "transparentImage": "https://transparent",
                    "description": "desc",
                    "faq": [{"question": "Q", "answer": "A"}],
                    "isChannel": True,
                    "deliveryMode": 1,
                    "freeReturn": 7,
                    "unionType": 2,
                    "imageBindItem": True,
                    "imagesDescBindItem": False,
                    "enableMultiWarehouse": True,
                    "itemShortTitle": "短标题",
                    "enableStepPresale": False,
                    "enableMainSpecImage": True,
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.create_item_v2(
        name="新品",
        brand_id=123,
        category_id="cat-1",
        attributes=[
            {
                "propertyId": "prop-1",
                "name": "颜色",
                "value": "红",
                "valueList": [{"valueId": "val-1", "value": "红"}],
            }
        ],
        images=["https://img"],
        image_descriptions=["https://desc"],
        shipping_template_id="ship-1",
        faq=[{"question": "Q", "answer": "A"}],
    )

    assert response.success is True
    detail = response.data
    assert isinstance(detail, ItemDetailV3)
    assert detail.item_id == "item-v3"
    assert detail.create_time == 1700000001
    assert detail.attributes[0].value_list[0].value == "红"
    assert detail.enable_multi_warehouse is True
    assert detail.union_type == 2

    client.close()


def test_update_item_v3(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.updateItemV2"
        assert payload["id"] == "item-v3"
        assert payload["updatedFields"] == ["name"]
        assert payload["name"] == "更新后"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "id": "item-v3",
                    "createTime": 1700000200,
                    "updateTime": 1700000300,
                    "name": "更新后",
                    "ename": "updated",
                    "brandId": 456,
                    "categoryId": "cat-2",
                    "attributes": [],
                    "shippingTemplateId": "ship-2",
                    "shippingGrossWeight": 600,
                    "variantIds": ["var-1", "var-2"],
                    "images": ["https://img1"],
                    "standardImages": [],
                    "longImages": [],
                    "videoUrl": None,
                    "articleNo": "art-2",
                    "imageDescriptions": [],
                    "transparentImage": None,
                    "description": "updated",
                    "faq": [],
                    "isChannel": False,
                    "deliveryMode": 2,
                    "freeReturn": 3,
                    "unionType": 1,
                    "imageBindItem": False,
                    "imagesDescBindItem": True,
                    "enableMultiWarehouse": False,
                    "itemShortTitle": None,
                    "enableStepPresale": True,
                    "enableMainSpecImage": False,
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.update_item_v2(
        "item-v3",
        name="更新后",
    )

    assert response.success is True
    detail = response.data
    assert isinstance(detail, ItemDetailV3)
    assert detail.name == "更新后"
    assert detail.variant_ids == ["var-1", "var-2"]
    assert detail.enable_step_presale is True
    assert detail.images_desc_bind_item is True

    client.close()


def test_create_item_and_sku(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload: Dict[str, Any] = json.loads(request.content.decode())
        assert payload["method"] == "product.createItemAndSku"
        assert payload["createSkuList"][0]["variants"][0]["id"] == "v1"
        assert payload["imageDescriptions"][0]["link"] == "https://img"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "itemId": "item-sku",
                    "name": "组合商品",
                    "brandId": 123,
                    "categoryId": "cat-1",
                    "attributes": [
                        {
                            "propertyId": "prop-1",
                            "name": "颜色",
                            "value": "红",
                            "valueId": "val-1",
                            "valueList": [
                                {"valueId": "val-1", "value": "红"},
                            ],
                        }
                    ],
                    "shippingTemplateId": "ship-1",
                    "shippingGrossWeight": 600,
                    "variantIds": ["var-1"],
                    "images": [{"link": "https://img"}],
                    "standardImages": [{"link": "https://std"}],
                    "longImages": [],
                    "videos": [{"link": "https://video"}],
                    "articleNo": "art-1",
                    "imageDescriptions": [{"link": "https://desc"}],
                    "transparentImage": "https://transparent",
                    "description": "desc",
                    "deliveryMode": 1,
                    "freeReturn": 7,
                    "enableMultiWarehouse": True,
                    "sizeTableImage": [{"link": "https://size"}],
                    "recommendSizeTableImage": [],
                    "modelTryOnSizeTableImage": [],
                    "enableMainSpecImage": 1,
                    "enableStepPresale": False,
                    "itemShortTitle": "短标题",
                    "skuList": [
                        {
                            "skuId": "sku-1",
                            "price": 299,
                            "stock": 10,
                            "logisticsPlanId": "plan-1",
                            "includeTax": True,
                            "erpCode": "erp-1",
                            "specImage": "https://spec",
                            "barcode": "code-1",
                            "deliveryFlag": 1,
                            "variants": [
                                {
                                    "id": "v1",
                                    "name": "颜色",
                                    "value": "红",
                                    "valueId": "val-1",
                                }
                            ],
                            "deliveryTime": {"time": "2天", "type": 1},
                        }
                    ],
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.create_item_and_sku(
        name="组合商品",
        brand_id=123,
        category_id="cat-1",
        attributes=[
            {
                "propertyId": "prop-1",
                "name": "颜色",
                "value": "红",
                "valueList": [{"valueId": "val-1", "value": "红"}],
            }
        ],
        images=["https://img"],
        image_descriptions=["https://img"],
        shipping_template_id="ship-1",
        price=299,
        stock=10,
        logistics_plan_id="plan-1",
        variants=[{"id": "v1", "name": "颜色", "value": "红"}],
        delivery_time={"time": "2天", "type": 1},
    )

    assert response.success is True
    detail = response.data
    assert detail.item_id == "item-sku"
    assert detail.images[0].link == "https://img"
    assert detail.sku_list[0].sku_id == "sku-1"
    assert detail.sku_list[0].delivery_time is not None
    assert detail.sku_list[0].variants[0].value == "红"

    client.close()


def test_update_item_and_sku(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload: Dict[str, Any] = json.loads(request.content.decode())
        assert payload["method"] == "product.updateItemAndSku"
        assert payload["itemId"] == "item-sku"
        # Since only price=188 is passed, we expect it to update the SKU price
        # The exact structure depends on implementation
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "itemId": "item-sku",
                    "images": [{"link": "https://img"}],
                    "imageDescriptions": [{"link": "https://desc"}],
                    "enableMainSpecImage": 0,
                    "skuList": [
                        {
                            "skuId": "sku-1",
                            "price": 188,
                            "stock": 5,
                            "variants": [
                                {
                                    "id": "v1",
                                    "name": "颜色",
                                    "value": "红",
                                }
                            ],
                        }
                    ],
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.update_item_and_sku(
        "item-sku",
        "sku-1",
        price=188,
    )

    assert response.success is True
    detail = response.data
    assert detail.sku_list[0].price == 188
    assert detail.image_descriptions[0].link == "https://desc"

    client.close()


def test_create_sku_v3(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.createSkuV2"
        assert payload["itemId"] == "item-1"
        assert payload["price"] == 120
        assert payload["variants"][0]["id"] == "v1"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "id": "sku-1",
                    "scSkucode": "sc-1",
                    "buyable": True,
                    "createTime": 1700000400,
                    "updateTime": 1700000405,
                    "name": "默认",
                    "isGift": False,
                    "itemId": "item-1",
                    "ipq": 1,
                    "originalPrice": 150,
                    "price": 120,
                    "stock": 20,
                    "logisticsPlanId": "plan-1",
                    "whcode": "WH1",
                    "priceType": 1,
                    "erpCode": "erp-1",
                    "variants": [
                        {
                            "id": "v1",
                            "name": "颜色",
                            "value": "黑",
                            "valueId": "val-1",
                        }
                    ],
                    "deliveryTime": {"time": "2天", "type": 1},
                    "specImage": "https://spec",
                    "barcode": "code-1",
                    "originSkuId": "origin-1",
                    "boutiqueMode": "SELF",
                    "freeReturn": 7,
                    "rowNumber": 1,
                    "deliveryFlag": 2,
                    "unionItemDetails": [
                        {
                            "id": "union-1",
                            "name": "组合",
                            "scSkuCode": "sc-1",
                            "barcode": "code-1",
                            "ipq": 1,
                            "erpCode": "erp-1",
                        }
                    ],
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.create_sku_v2(
        "item-1",
        120,
        20,
        "plan-1",
        [{"id": "v1", "name": "颜色", "value": "黑"}],
        {"time": "2天", "type": 1},
    )

    assert response.success is True
    detail = response.data
    assert detail.sku_id == "sku-1"
    assert detail.delivery_time is not None
    assert detail.delivery_time.time == "2天"
    assert detail.variants[0].value == "黑"
    assert detail.union_item_details[0].item_id == "union-1"

    client.close()


def test_update_sku_v3(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.updateSkuV2"
        assert payload["id"] == "sku-1"
        assert payload["updatedFields"] == ["price"]
        assert payload["price"] == 130
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "id": "sku-1",
                    "price": 130,
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.product.update_sku_v2(
        sku_id="sku-1",
        item_id="item-1",
        price=130,
    )

    assert response.success is True
    detail = response.data
    assert detail is not None
    assert detail.price == 130

    client.close()


def test_delete_item_v3(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.deleteItemV2"
        assert payload["itemIds"] == ["item-1"]
        return httpx.Response(200, json={"success": True, "data": "ok"})

    client = _build_client(monkeypatch, handler)
    response = client.product.delete_item_v2(
        "item-1",
    )

    assert response.success is True
    assert response.data == "ok"

    client.close()


def test_delete_sku_v3(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "product.deleteSkuV2"
        assert payload["skuIds"] == ["sku-1"]
        return httpx.Response(200, json={"success": True, "data": "ok"})

    client = _build_client(monkeypatch, handler)
    response = client.product.delete_sku_v2(
        "sku-1",
    )

    assert response.success is True
    assert response.data == "ok"

    client.close()
