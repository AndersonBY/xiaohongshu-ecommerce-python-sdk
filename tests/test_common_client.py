import json

import httpx

from xiaohongshu_ecommerce.client import XhsClient
from xiaohongshu_ecommerce.config import ClientConfig
from xiaohongshu_ecommerce.models.common import (
    ZoneInfo,
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


def test_common_get_categories(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "common.getCategories"
        assert payload["categoryId"] == "123"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "sellerInCategoryGray": True,
                    "categoryV3s": [
                        {
                            "id": "123",
                            "name": "Shoes",
                            "enName": "Shoes",
                            "isLeaf": True,
                        }
                    ],
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.common.get_categories(category_id="123")

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.categories[0].name == "Shoes"
    assert data.seller_in_category_gray is True

    client.close()


def test_common_get_attribute_values(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "common.getAttributeValues"
        assert payload["attributeId"] == "attr-1"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "attributeValueV3s": [
                        {"valueId": "1", "valueName": "Red"},
                        {"valueId": "2", "valueName": "Blue"},
                    ]
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.common.get_attribute_values(attribute_id="attr-1")

    assert response.success is True
    data = response.data
    assert data is not None
    assert len(data.values) == 2

    client.close()


def test_common_get_express_company_list(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "common.getExpressCompanyList"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "expressCompanyInfos": [
                        {
                            "expressCompanyId": 1,
                            "expressCompanyCode": "SF",
                            "expressCompanyName": "顺丰",
                            "comment": "",
                        }
                    ]
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.common.get_express_company_list()

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.express_company_infos[0].code == "SF"

    client.close()


def test_common_get_seller_key_info(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "common.getSellerKeyInfo"
        return httpx.Response(
            200,
            json={"success": True, "data": {"sellerId": "seller-1", "appKey": "key"}},
        )

    client = _build_client(monkeypatch, handler)
    response = client.common.get_seller_key_info()

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.seller_id == "seller-1"

    client.close()


def test_common_get_nest_zone(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "common.getNestZone"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "provinceZoneList": [
                        {
                            "id": "p1",
                            "zones": [
                                {
                                    "id": "c1",
                                    "zones": [{"id": "z1"}],
                                }
                            ],
                        }
                    ]
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.common.get_nest_zone()

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.province_zone_list[0].zones[0].zones[0].id == "z1"

    client.close()


def test_common_category_match(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "common.categoryMatch"
        assert payload["spuName"] == "测试商品"
        assert payload["topK"] == 3
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {"categoryInfo": [{"id": "c1", "name": "分类", "score": 0.9}]},
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.common.category_match(spu_name="测试商品", top_k=3)

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.category_info[0].score == 0.9

    client.close()


def test_common_category_match_v2(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "common.categoryMatchV2"
        assert payload["name"] == "测试"
        assert payload["imageUrls"] == ["https://example.com/1.jpg"]
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "recommendCategories": [
                        {
                            "categoryId": "c1",
                            "categoryPathList": [{"name": "分类", "level": 3}],
                        }
                    ]
                },
            },
        )

    client = _build_client(
        monkeypatch,
        handler,
    )
    response = client.common.category_match_v2(
        name="测试", image_urls=["https://example.com/1.jpg"]
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.recommend_categories[0].category_id == "c1"

    client.close()


def test_common_get_logistics_list(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "common.getLogisticsList"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "logisticsPlans": [
                        {
                            "planInfoId": "plan-1",
                            "planInfoName": "Default",
                            "logisticName": "顺丰",
                            "logisticsCompanyCode": "SF",
                            "tradeMode": 1,
                        }
                    ]
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.common.get_logistics_list()

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.logistics_plans[0].logistic_name == "顺丰"

    client.close()


def test_common_get_carriage_template_list(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "common.getCarriageTemplateList"
        assert payload["pageIndex"] == 1
        assert payload["pageSize"] == 20
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "carriageTemplateList": [
                        {
                            "templateId": "tmp-1",
                            "templateName": "Default",
                            "templateType": 0,
                        }
                    ],
                    "totalCount": 1,
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.common.get_carriage_template_list(page_index=1, page_size=20)

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.total_count == 1
    assert data.carriage_template_list[0].template_name == "Default"

    client.close()


def test_common_get_carriage_template(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "common.getCarriageTemplate"
        assert payload["templateId"] == "tmp-1"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {"templateId": "tmp-1", "templateName": "Default"},
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.common.get_carriage_template(template_id="tmp-1")

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.template.template_id == "tmp-1"

    client.close()


def test_common_brand_search(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "common.brandSearch"
        assert payload["keyword"] == "nike"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "brands": [
                        {
                            "id": "1",
                            "name": "Nike",
                        }
                    ]
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.common.brand_search(category_id="", keyword="nike")

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.brands[0].name == "Nike"

    client.close()


def test_common_get_logistics_mode(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "common.getLogisticsMode"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "logisticModes": [
                        {"logisticsCode": "SF", "logisticsTranslation": "顺丰"}
                    ]
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.common.get_logistics_mode()

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.logistic_modes[0].logistics_code == "SF"

    client.close()


def test_common_get_delivery_rule(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "common.getDeliveryRule"
        assert payload["getDeliveryRuleRequests"][0]["whcode"] == "wh-1"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "deliveryRuleList": [
                        {
                            "sellerId": "seller-1",
                            "existing": [
                                {
                                    "timeType": 1,
                                    "value": 2,
                                    "desc": "48h",
                                    "isDefault": True,
                                }
                            ],
                        }
                    ]
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.common.get_delivery_rule(
        get_delivery_rule_requests=[{"whcode": "wh-1"}]
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.delivery_rule_list[0].existing[0].value == 2

    client.close()


def test_common_get_address_record(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "common.getAddressRecord"
        assert payload["pageIndex"] == 1
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "sellerAddressRecordList": [
                        {"sellerAddressRecordId": 1, "contactName": "张三"}
                    ],
                    "total": 1,
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.common.get_address_record(page_no=1, page_size=20)

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.total == 1
    assert data.seller_address_record_list[0].contact_name == "张三"

    client.close()


def test_common_get_zones(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "common.getZones"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": [{"code": "001", "name": "东城区"}],
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.common.get_zones(code="001")

    assert response.success is True
    data = response.data
    assert data is not None
    assert isinstance(data[0], ZoneInfo)
    assert data[0].code == "001"

    client.close()


def test_common_check_forbidden_keyword(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["method"] == "common.checkForbiddenKeyword"
        assert payload["text"] == "违禁词"
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {"forbiddenKeywords": ["违禁"]},
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.common.check_forbidden_keyword(text="违禁词")

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.forbidden_keywords == ["违禁"]

    client.close()
