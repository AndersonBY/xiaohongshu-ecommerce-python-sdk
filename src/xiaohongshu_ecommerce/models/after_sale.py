"""After-sale module requests and responses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional

from .base import BaseRequest


def _opt_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    return str(value)


def _opt_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _opt_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    return bool(value)


def _opt_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _coerce_list(raw: Any) -> List[Any]:
    if raw is None:
        return []
    if isinstance(raw, list):
        return raw
    return [raw]


class ListAfterSaleInfosRequest(BaseRequest):
    def __init__(
        self,
        *,
        order_id: Optional[str] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        time_type: Optional[int] = None,
        return_types: Optional[List[int]] = None,
        statuses: Optional[List[int]] = None,
    ) -> None:
        super().__init__(method="afterSale.listAfterSaleInfos")
        self.order_id = order_id
        self.page_no = page_no
        self.page_size = page_size
        self.start_time = start_time
        self.end_time = end_time
        self.time_type = time_type
        self.return_types = return_types or []
        self.statuses = statuses or []

    def extra_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {}
        if self.order_id is not None:
            payload["orderId"] = self.order_id
        if self.page_no is not None:
            payload["pageNo"] = self.page_no
        if self.page_size is not None:
            payload["pageSize"] = self.page_size
        if self.start_time is not None:
            payload["startTime"] = self.start_time
        if self.end_time is not None:
            payload["endTime"] = self.end_time
        if self.time_type is not None:
            payload["timeType"] = self.time_type
        if self.return_types:
            payload["returnTypes"] = self.return_types
        if self.statuses:
            payload["statuses"] = self.statuses
        return payload


class GetAfterSaleInfoRequest(BaseRequest):
    def __init__(
        self, returns_id: str, *, need_negotiate_record: Optional[bool] = None
    ) -> None:
        super().__init__(method="afterSale.getAfterSaleInfo")
        self.returns_id = returns_id
        self.need_negotiate_record = need_negotiate_record

    def extra_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"returnsId": self.returns_id}
        if self.need_negotiate_record is not None:
            payload["needNegotiateRecord"] = self.need_negotiate_record
        return payload


class ListReturnRejectReasonRequest(BaseRequest):
    def __init__(
        self, returns_id: str, *, reject_reason_type: Optional[int] = None
    ) -> None:
        super().__init__(method="afterSale.rejectReasons")
        self.returns_id = returns_id
        self.reject_reason_type = reject_reason_type

    def extra_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"returnsId": self.returns_id}
        if self.reject_reason_type is not None:
            payload["rejectReasonType"] = self.reject_reason_type
        return payload


class GetAfterSaleListRequest(BaseRequest):
    def __init__(
        self,
        *,
        status: Optional[int] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        time_type: Optional[int] = None,
        use_has_next: Optional[bool] = None,
        reason_id: Optional[int] = None,
        return_type: Optional[int] = None,
    ) -> None:
        super().__init__(method="afterSale.listAfterSaleApi")
        self.status = status
        self.page_no = page_no
        self.page_size = page_size
        self.start_time = start_time
        self.end_time = end_time
        self.time_type = time_type
        self.use_has_next = use_has_next
        self.reason_id = reason_id
        self.return_type = return_type

    def extra_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {}
        if self.status is not None:
            payload["status"] = self.status
        if self.page_no is not None:
            payload["pageNo"] = self.page_no
        if self.page_size is not None:
            payload["pageSize"] = self.page_size
        if self.start_time is not None:
            payload["startTime"] = self.start_time
        if self.end_time is not None:
            payload["endTime"] = self.end_time
        if self.time_type is not None:
            payload["timeType"] = self.time_type
        if self.use_has_next is not None:
            payload["useHasNext"] = self.use_has_next
        if self.reason_id is not None:
            payload["reasonId"] = self.reason_id
        if self.return_type is not None:
            payload["returnType"] = self.return_type
        return payload


class ConfirmReceiveRequest(BaseRequest):
    def __init__(
        self,
        returns_id: str,
        *,
        action: Optional[int] = None,
        reason: Optional[int] = None,
        description: Optional[str] = None,
    ) -> None:
        super().__init__(method="afterSale.confirmReceive")
        self.returns_id = returns_id
        self.action = action
        self.reason = reason
        self.description = description

    def extra_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"returnsId": self.returns_id}
        if self.action is not None:
            payload["action"] = self.action
        if self.reason is not None:
            payload["reason"] = self.reason
        if self.description is not None:
            payload["description"] = self.description
        return payload


@dataclass
class AuditReturnsReceiverInfo:
    code: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    district: Optional[str] = None
    street: Optional[str] = None
    receiver_name: Optional[str] = None
    receiver_phone: Optional[str] = None
    seller_address_record_id: Optional[int] = None
    seller_address_record_version: Optional[int] = None

    def to_payload(self) -> Dict[str, Any]:
        return {
            key: value
            for key, value in {
                "code": self.code,
                "country": self.country,
                "city": self.city,
                "province": self.province,
                "district": self.district,
                "street": self.street,
                "receiverName": self.receiver_name,
                "receiverPhone": self.receiver_phone,
                "sellerAddressRecordId": self.seller_address_record_id,
                "sellerAddressRecordVersion": self.seller_address_record_version,
            }.items()
            if value is not None
        }


class AuditReturnsRequest(BaseRequest):
    def __init__(
        self,
        returns_id: str,
        *,
        action: Optional[int] = None,
        reason: Optional[int] = None,
        description: Optional[str] = None,
        message: Optional[str] = None,
        receiver_info: Optional[AuditReturnsReceiverInfo] = None,
    ) -> None:
        super().__init__(method="afterSale.auditReturns")
        self.returns_id = returns_id
        self.action = action
        self.reason = reason
        self.description = description
        self.message = message
        self.receiver_info = receiver_info

    def extra_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"returnsId": self.returns_id}
        if self.action is not None:
            payload["action"] = self.action
        if self.reason is not None:
            payload["reason"] = self.reason
        if self.description is not None:
            payload["description"] = self.description
        if self.message is not None:
            payload["message"] = self.message
        if self.receiver_info is not None:
            payload["receiverInfo"] = self.receiver_info.to_payload()
        return payload


class GetAfterSaleDetailRequest(BaseRequest):
    def __init__(self, after_sale_id: str) -> None:
        super().__init__(method="afterSale.getAfterSaleDetail")
        self.after_sale_id = after_sale_id

    def extra_payload(self) -> Dict[str, Any]:
        return {"afterSaleId": self.after_sale_id}


class ReturnsAbnormalRequest(BaseRequest):
    def __init__(
        self,
        returns_id: str,
        *,
        abnormal_type: Optional[int] = None,
        abnormal_note: Optional[str] = None,
    ) -> None:
        super().__init__(method="afterSale.setReturnsAbnormal")
        self.returns_id = returns_id
        self.abnormal_type = abnormal_type
        self.abnormal_note = abnormal_note

    def extra_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"returnsId": self.returns_id}
        if self.abnormal_type is not None:
            payload["abnormalType"] = self.abnormal_type
        if self.abnormal_note is not None:
            payload["abnormalNote"] = self.abnormal_note
        return payload


class ReceiveAndShipRequest(BaseRequest):
    def __init__(
        self,
        returns_id: str,
        *,
        express_company_code: Optional[str] = None,
        express_no: Optional[str] = None,
    ) -> None:
        super().__init__(method="afterSale.receiveAndShip")
        self.returns_id = returns_id
        self.express_company_code = express_company_code
        self.express_no = express_no

    def extra_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"returnsId": self.returns_id}
        if self.express_company_code is not None:
            payload["expressCompanyCode"] = self.express_company_code
        if self.express_no is not None:
            payload["expressNo"] = self.express_no
        return payload


@dataclass
class AfterSaleBasicInfo:
    returns_id: Optional[str]
    status: Optional[int]
    user_id: Optional[str]
    order_id: Optional[str]
    raw: Mapping[str, Any] = field(repr=False)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "AfterSaleBasicInfo":
        return cls(
            returns_id=_opt_str(data.get("returnsId")),
            status=_opt_int(data.get("status")),
            user_id=_opt_str(data.get("userId")),
            order_id=_opt_str(data.get("orderId")),
            raw=data,
        )


@dataclass
class ListAfterSaleInfosResponse:
    after_sale_basic_infos: List[AfterSaleBasicInfo]
    total_count: Optional[int]
    page_no: Optional[int]
    page_size: Optional[int]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ListAfterSaleInfosResponse":
        infos = [
            _coerce_after_sale_basic(item)
            for item in data.get("afterSaleBasicInfos", [])
        ]
        return cls(
            after_sale_basic_infos=infos,
            total_count=_opt_int(data.get("totalCount")),
            page_no=_opt_int(data.get("pageNo")),
            page_size=_opt_int(data.get("pageSize")),
        )


def _coerce_after_sale_basic(raw: Any) -> AfterSaleBasicInfo:
    if isinstance(raw, Mapping):
        return AfterSaleBasicInfo.from_dict(raw)
    return AfterSaleBasicInfo.from_dict({})


@dataclass
class SimpleAfterSale:
    returns_id: Optional[str]
    status: Optional[int]
    raw: Mapping[str, Any] = field(repr=False)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SimpleAfterSale":
        return cls(
            returns_id=_opt_str(data.get("returnsId")),
            status=_opt_int(data.get("status")),
            raw=data,
        )


@dataclass
class GetAfterSaleListResponse:
    total: Optional[int]
    page_no: Optional[int]
    page_size: Optional[int]
    has_next: Optional[bool]
    simple_after_sale_list: List[SimpleAfterSale]
    max_page_no: Optional[int]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "GetAfterSaleListResponse":
        items = [
            SimpleAfterSale.from_dict(item)
            for item in data.get("simpleAfterSaleList", [])
            if isinstance(item, Mapping)
        ]
        return cls(
            total=_opt_int(data.get("total")),
            page_no=_opt_int(data.get("pageNo")),
            page_size=_opt_int(data.get("pageSize")),
            has_next=_opt_bool(data.get("haxNext")),
            simple_after_sale_list=items,
            max_page_no=_opt_int(data.get("maxPageNo")),
        )


@dataclass
class RejectReason:
    reason_type: Optional[int]
    reason_id: Optional[int]
    reason_name: Optional[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "RejectReason":
        return cls(
            reason_type=_opt_int(data.get("reasonType")),
            reason_id=_opt_int(data.get("reasonId")),
            reason_name=_opt_str(data.get("reasonName")),
        )


@dataclass
class ListReturnRejectReasonResponse:
    reject_reasons: List[RejectReason]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ListReturnRejectReasonResponse":
        return cls(
            reject_reasons=[
                RejectReason.from_dict(item)
                for item in data.get("rejectReasons", [])
                if isinstance(item, Mapping)
            ]
        )


@dataclass
class GetAfterSaleInfoResponse:
    after_sale_info: Mapping[str, Any]
    logistics_info: Optional[Mapping[str, Any]]
    negotiate_records: List[Mapping[str, Any]]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "GetAfterSaleInfoResponse":
        return cls(
            after_sale_info=data.get("afterSaleInfo") or {},
            logistics_info=data.get("logisticsInfo"),
            negotiate_records=list(data.get("negotiateRecords") or []),
        )


@dataclass
class GetAfterSaleDetailResponse:
    detail: Mapping[str, Any]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "GetAfterSaleDetailResponse":
        return cls(detail=data)


__all__ = [
    "ListAfterSaleInfosRequest",
    "GetAfterSaleInfoRequest",
    "ListReturnRejectReasonRequest",
    "GetAfterSaleListRequest",
    "ConfirmReceiveRequest",
    "AuditReturnsReceiverInfo",
    "AuditReturnsRequest",
    "GetAfterSaleDetailRequest",
    "ReturnsAbnormalRequest",
    "ReceiveAndShipRequest",
    "AfterSaleBasicInfo",
    "ListAfterSaleInfosResponse",
    "SimpleAfterSale",
    "GetAfterSaleListResponse",
    "RejectReason",
    "ListReturnRejectReasonResponse",
    "GetAfterSaleInfoResponse",
    "GetAfterSaleDetailResponse",
]
