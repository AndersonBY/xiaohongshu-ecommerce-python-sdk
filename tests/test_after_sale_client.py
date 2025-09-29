import json

import httpx

from xiaohongshu_ecommerce.client import XhsClient
from xiaohongshu_ecommerce.config import ClientConfig
from xiaohongshu_ecommerce.models.after_sale import (
    AuditReturnsReceiverInfo,
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


def test_list_after_sale_infos(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "afterSale.listAfterSaleInfos"
        assert payload["orderId"] == "order-1"
        assert payload["returnTypes"] == [1, 2]
        assert payload["statuses"] == [10]
        assert payload["pageNo"] == 1
        assert payload["pageSize"] == 20
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "afterSaleBasicInfos": [
                        {
                            "returnsId": "ret-1",
                            "status": 100,
                            "userId": "user-1",
                        }
                    ],
                    "totalCount": 1,
                    "pageNo": 1,
                    "pageSize": 20,
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.after_sale.list_after_sale_infos(
        page_no=1, page_size=20, order_id="order-1", return_types=[1, 2], statuses=[10]
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.after_sale_basic_infos[0].returns_id == "ret-1"

    client.close()


def test_get_after_sale_info(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "afterSale.getAfterSaleInfo"
        assert payload["returnsId"] == "ret-1"
        assert payload["needNegotiateRecord"] is True
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "afterSaleInfo": {"returnsId": "ret-1"},
                    "logisticsInfo": {"expressNo": "EXP001"},
                    "negotiateRecords": [{"message": "hi"}],
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.after_sale.get_after_sale_info(
        returns_id="ret-1", need_negotiate_record=True
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.after_sale_info["returnsId"] == "ret-1"

    client.close()


def test_list_return_reject_reasons(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "afterSale.rejectReasons"
        assert payload["returnsId"] == "ret-1"
        assert payload["rejectReasonType"] == 1
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {"rejectReasons": [{"reasonId": 1, "reasonName": "缺件"}]},
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.after_sale.list_return_reject_reasons(
        returns_id="ret-1", reject_reason_type=1
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.reject_reasons[0].reason_name == "缺件"

    client.close()


def test_list_after_sale(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "afterSale.listAfterSaleApi"
        assert payload["status"] == 1
        assert payload["startTime"] == 1617724800000
        assert payload["endTime"] == 1617811200000
        assert payload["timeType"] == 1
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "total": 1,
                    "simpleAfterSaleList": [{"returnsId": "ret-1", "status": 10}],
                },
            },
        )

    client = _build_client(monkeypatch, handler)
    response = client.after_sale.list_after_sale(
        start_time=1617724800000, end_time=1617811200000, time_type=1, status=1
    )

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.simple_after_sale_list[0].returns_id == "ret-1"

    client.close()


def test_confirm_receive(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "afterSale.confirmReceive"
        assert payload["action"] == 1
        return httpx.Response(
            200,
            json={"success": True, "data": "确认收货成功"},
        )

    client = _build_client(monkeypatch, handler)
    response = client.after_sale.confirm_receive(returns_id="ret-1", action=1)

    assert response.success is True
    assert response.data == "确认收货成功"

    client.close()


def test_audit_returns(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "afterSale.auditReturns"
        assert payload["receiverInfo"]["receiverName"] == "张三"
        return httpx.Response(
            200,
            json={"success": True, "data": "审核成功"},
        )

    client = _build_client(monkeypatch, handler)
    receiver_info = AuditReturnsReceiverInfo(receiver_name="张三")
    response = client.after_sale.audit_returns(
        returns_id="ret-1", action=1, receiver_info=receiver_info
    )

    assert response.success is True
    assert response.data == "审核成功"

    client.close()


def test_get_after_sale_detail(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "afterSale.getAfterSaleDetail"
        assert payload["afterSaleId"] == "asd-1"
        return httpx.Response(
            200,
            json={"success": True, "data": {"returnsId": "ret-1"}},
        )

    client = _build_client(monkeypatch, handler)
    response = client.after_sale.get_after_sale_detail(after_sale_id="asd-1")

    assert response.success is True
    data = response.data
    assert data is not None
    assert data.detail["returnsId"] == "ret-1"

    client.close()


def test_set_returns_abnormal(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "afterSale.setReturnsAbnormal"
        assert payload["abnormalType"] == 2
        return httpx.Response(
            200,
            json={"success": True, "data": "拒绝售后确认收货完成"},
        )

    client = _build_client(monkeypatch, handler)
    response = client.after_sale.set_returns_abnormal(
        returns_id="ret-1", abnormal_type=2
    )

    assert response.success is True

    client.close()


def test_receive_and_ship(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        assert payload["method"] == "afterSale.receiveAndShip"
        assert payload["expressCompanyCode"] == "SF"
        assert payload["expressNo"] == "SF123456"
        return httpx.Response(
            200,
            json={"success": True, "data": "售后换货成功"},
        )

    client = _build_client(monkeypatch, handler)
    response = client.after_sale.receive_and_ship(
        returns_id="ret-1", express_company_code="SF", express_no="SF123456"
    )

    assert response.success is True

    client.close()
