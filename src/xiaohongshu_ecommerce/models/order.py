"""Order domain models for Xiaohongshu e-commerce API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from .base import BaseRequest


class CustomsStatusEnum(Enum):
    """Customs status enumeration."""

    PENDING = "pending"
    DECLARED = "declared"
    PASSED = "passed"
    FAILED = "failed"
    ABNORMAL = "abnormal"


class CustomFailReasonEnum(Enum):
    """Custom failure reason enumeration."""

    CUSTOMS_CODE_ERROR = "customs_code_error"
    PRODUCT_INFO_ERROR = "product_info_error"
    RECEIVER_INFO_ERROR = "receiver_info_error"
    OTHER = "other"


class CustomAbnormalReasonEnum(Enum):
    """Custom abnormal reason enumeration."""

    TIMEOUT = "timeout"
    SYSTEM_ERROR = "system_error"
    REVIEW_REQUIRED = "review_required"
    OTHER = "other"


@dataclass
class CustomsStatusInfo:
    """Customs status information."""

    status: Optional[CustomsStatusEnum] = None
    fail_reason: Optional[CustomFailReasonEnum] = None
    abnormal_reason: Optional[CustomAbnormalReasonEnum] = None
    description: Optional[str] = None


@dataclass
class CustomsItem:
    """Customs item information."""

    hs_code: Optional[str] = None
    product_name: Optional[str] = None
    product_name_en: Optional[str] = None
    unit_price: Optional[float] = None
    quantity: Optional[int] = None
    total_price: Optional[float] = None
    weight: Optional[float] = None
    brand: Optional[str] = None
    brand_en: Optional[str] = None
    country_of_origin: Optional[str] = None
    material: Optional[str] = None
    material_en: Optional[str] = None


@dataclass
class SkuIdentifyCodeInfo:
    """SKU identify code information."""

    sku_id: Optional[str] = None
    identify_code: Optional[str] = None
    quantity: Optional[int] = None


@dataclass
class OrderSimpleDetail:
    """Simple order detail."""

    order_id: Optional[str] = None
    order_no: Optional[str] = None
    order_status: Optional[int] = None
    order_type: Optional[int] = None
    create_time: Optional[int] = None
    update_time: Optional[int] = None
    total_amount: Optional[float] = None
    actual_amount: Optional[float] = None
    buyer_id: Optional[str] = None
    seller_id: Optional[str] = None


@dataclass
class OrderDetailInfo:
    """Detailed order information."""

    order_id: Optional[str] = None
    order_no: Optional[str] = None
    order_status: Optional[int] = None
    order_type: Optional[int] = None
    create_time: Optional[int] = None
    update_time: Optional[int] = None
    total_amount: Optional[float] = None
    actual_amount: Optional[float] = None
    buyer_id: Optional[str] = None
    seller_id: Optional[str] = None
    receiver_name: Optional[str] = None
    receiver_phone: Optional[str] = None
    receiver_address: Optional[str] = None
    express_company: Optional[str] = None
    express_no: Optional[str] = None
    order_items: List[dict] = field(default_factory=list)
    customs_info: Optional[CustomsStatusInfo] = None


@dataclass
class ReceiverInfo:
    """Order receiver information."""

    name: Optional[str] = None
    phone: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    id_card: Optional[str] = None


@dataclass
class TrackingInfo:
    """Order tracking information."""

    express_company: Optional[str] = None
    express_no: Optional[str] = None
    tracking_details: List[dict] = field(default_factory=list)


@dataclass
class DeclareInfo:
    """Order declare information."""

    declare_no: Optional[str] = None
    declare_status: Optional[int] = None
    customs_code: Optional[str] = None
    port_code: Optional[str] = None
    declare_items: List[CustomsItem] = field(default_factory=list)


@dataclass
class SupportedPort:
    """Supported port information."""

    port_code: Optional[str] = None
    port_name: Optional[str] = None
    customs_code: Optional[str] = None


@dataclass
class TransferBatch:
    """Transfer batch information."""

    batch_id: Optional[str] = None
    batch_no: Optional[str] = None
    status: Optional[int] = None
    create_time: Optional[int] = None


@dataclass
class KosData:
    """KOS data information."""

    data_type: Optional[str] = None
    data_content: Optional[str] = None
    timestamp: Optional[int] = None


@dataclass
class GetOrderListRequest(BaseRequest):
    """Get order list request."""

    start_time: Optional[int] = None
    end_time: Optional[int] = None
    time_type: Optional[int] = None
    order_type: Optional[int] = None
    order_status: Optional[int] = None
    page_no: Optional[int] = None
    page_size: Optional[int] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        payload = {}
        if self.start_time is not None:
            payload["startTime"] = self.start_time
        if self.end_time is not None:
            payload["endTime"] = self.end_time
        if self.time_type is not None:
            payload["timeType"] = self.time_type
        if self.order_type is not None:
            payload["orderType"] = self.order_type
        if self.order_status is not None:
            payload["orderStatus"] = self.order_status
        if self.page_no is not None:
            payload["pageNo"] = self.page_no
        if self.page_size is not None:
            payload["pageSize"] = self.page_size
        return payload


@dataclass
class GetOrderDetailRequest(BaseRequest):
    """Get order detail request."""

    order_id: Optional[str] = None
    order_no: Optional[str] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        payload = {}
        if self.order_id is not None:
            payload["orderId"] = self.order_id
        if self.order_no is not None:
            payload["orderNo"] = self.order_no
        return payload


@dataclass
class GetOrderDeclareRequest(BaseRequest):
    """Get order declare request."""

    order_id: Optional[str] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        payload = {}
        if self.order_id is not None:
            payload["orderId"] = self.order_id
        return payload


@dataclass
class GetSupportedPortListRequest(BaseRequest):
    """Get supported port list request."""

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        return {}


@dataclass
class BatchBindOrderSkuIdentifyCodeInfoRequest(BaseRequest):
    """Batch bind order SKU identify code info request."""

    order_sku_identify_code_info_list: List[dict] = field(default_factory=list)

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        return {"orderSkuIdentifyCodeInfoList": self.order_sku_identify_code_info_list}


@dataclass
class BondedPaymentRecordRequest(BaseRequest):
    """Bonded payment record request."""

    order_id: Optional[str] = None
    customs_type: Optional[str] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        payload = {}
        if self.order_id is not None:
            payload["orderId"] = self.order_id
        if self.customs_type is not None:
            payload["customsType"] = self.customs_type
        return payload


@dataclass
class SyncCustomsInfoRequest(BaseRequest):
    """Sync customs info request."""

    item_id: Optional[str] = None
    barcode: Optional[str] = None
    customs_info: Optional[dict] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        payload = {}
        if self.item_id is not None:
            payload["itemId"] = self.item_id
        if self.barcode is not None:
            payload["barcode"] = self.barcode
        if self.customs_info is not None:
            payload["customsInfo"] = self.customs_info
        return payload


@dataclass
class GetCustomInfoRequest(BaseRequest):
    """Get customs info request."""

    barcode: Optional[str] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        payload = {}
        if self.barcode is not None:
            payload["barcode"] = self.barcode
        return payload


@dataclass
class GetOrderReceiverInfoRequest(BaseRequest):
    """Get order receiver info request."""

    receiver_queries: List[dict] = field(default_factory=list)
    is_return: Optional[bool] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        payload = {}
        if self.receiver_queries:
            payload["receiverQueries"] = self.receiver_queries
        if self.is_return is not None:
            payload["isReturn"] = self.is_return
        return payload


@dataclass
class ModifyOrderExpressRequest(BaseRequest):
    """Modify order express request."""

    order_id: Optional[str] = None
    express_no: Optional[str] = None
    express_company_code: Optional[str] = None
    express_company_name: Optional[str] = None
    delivery_order_index: Optional[int] = None
    old_express_no: Optional[str] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        payload = {}
        if self.order_id is not None:
            payload["orderId"] = self.order_id
        if self.express_no is not None:
            payload["expressNo"] = self.express_no
        if self.express_company_code is not None:
            payload["expressCompanyCode"] = self.express_company_code
        if self.express_company_name is not None:
            payload["expressCompanyName"] = self.express_company_name
        if self.delivery_order_index is not None:
            payload["deliveryOrderIndex"] = self.delivery_order_index
        if self.old_express_no is not None:
            payload["oldExpressNo"] = self.old_express_no
        return payload


@dataclass
class OrderDeliverRequest(BaseRequest):
    """Order deliver request."""

    order_id: Optional[str] = None
    express_no: Optional[str] = None
    express_company_code: Optional[str] = None
    express_company_name: Optional[str] = None
    delivering_time: Optional[int] = None
    unpack: Optional[bool] = None
    sku_id_list: Optional[List[str]] = None
    return_address_id: Optional[str] = None
    sku_identify_code_info: Optional[dict] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        payload = {}
        if self.order_id is not None:
            payload["orderId"] = self.order_id
        if self.express_no is not None:
            payload["expressNo"] = self.express_no
        if self.express_company_code is not None:
            payload["expressCompanyCode"] = self.express_company_code
        if self.express_company_name is not None:
            payload["expressCompanyName"] = self.express_company_name
        if self.delivering_time is not None:
            payload["deliveringTime"] = self.delivering_time
        if self.unpack is not None:
            payload["unpack"] = self.unpack
        if self.sku_id_list is not None:
            payload["skuIdList"] = self.sku_id_list
        if self.return_address_id is not None:
            payload["returnAddressId"] = self.return_address_id
        if self.sku_identify_code_info is not None:
            payload["skuIdentifyCodeInfo"] = self.sku_identify_code_info
        return payload


@dataclass
class ModifySellerMarkRequest(BaseRequest):
    """Modify seller mark request."""

    order_id: Optional[str] = None
    seller_mark_note: Optional[str] = None
    operator: Optional[str] = None
    seller_mark_priority: Optional[int] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        payload = {}
        if self.order_id is not None:
            payload["orderId"] = self.order_id
        if self.seller_mark_note is not None:
            payload["sellerMarkNote"] = self.seller_mark_note
        if self.operator is not None:
            payload["operator"] = self.operator
        if self.seller_mark_priority is not None:
            payload["sellerMarkPriority"] = self.seller_mark_priority
        return payload


@dataclass
class GetOrderTrackRequest(BaseRequest):
    """Get order tracking request."""

    order_id: Optional[str] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        payload = {}
        if self.order_id is not None:
            payload["orderId"] = self.order_id
        return payload


@dataclass
class CreateTransferBatchRequest(BaseRequest):
    """Create transfer batch request."""

    orders: List[dict] = field(default_factory=list)
    plan_info_id: Optional[str] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        payload = {}
        if self.orders:
            payload["orders"] = self.orders
        if self.plan_info_id is not None:
            payload["planInfoId"] = self.plan_info_id
        return payload


@dataclass
class GetKosDataRequest(BaseRequest):
    """Get KOS data request."""

    start_date: Optional[str] = None
    end_date: Optional[str] = None
    page_no: Optional[int] = None
    page_size: Optional[int] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        payload = {}
        if self.start_date is not None:
            payload["startDate"] = self.start_date
        if self.end_date is not None:
            payload["endDate"] = self.end_date
        if self.page_no is not None:
            payload["pageNo"] = self.page_no
        if self.page_size is not None:
            payload["pageSize"] = self.page_size
        return payload


@dataclass
class ModifyCustomsStatusRequest(BaseRequest):
    """Modify customs status request."""

    order_id: Optional[str] = None
    customs_status: Optional[str] = None
    customs_remark: Optional[str] = None
    operator_id: Optional[str] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        payload = {}
        if self.order_id is not None:
            payload["orderId"] = self.order_id
        if self.customs_status is not None:
            payload["customsStatus"] = self.customs_status
        if self.customs_remark is not None:
            payload["customsRemark"] = self.customs_remark
        if self.operator_id is not None:
            payload["operatorId"] = self.operator_id
        return payload


@dataclass
class BatchApproveSubscribeOrdersRequest(BaseRequest):
    """Batch approve subscribe orders request."""

    order_ids: List[str] = field(default_factory=list)
    approval_reason: Optional[str] = None
    operator_id: Optional[str] = None
    approval_notes: Optional[str] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> dict:
        payload = {}
        if self.order_ids:
            payload["orderIds"] = self.order_ids
        if self.approval_reason is not None:
            payload["approvalReason"] = self.approval_reason
        if self.operator_id is not None:
            payload["operatorId"] = self.operator_id
        if self.approval_notes is not None:
            payload["approvalNotes"] = self.approval_notes
        return payload


# Response models
@dataclass
class GetOrderListResponse:
    """Get order list response."""

    total: int = 0
    page_no: int = 0
    page_size: int = 0
    max_page_no: int = 0
    order_list: List[OrderSimpleDetail] = field(default_factory=list)


@dataclass
class GetOrderDetailResponse:
    """Get order detail response."""

    order_detail: Optional[OrderDetailInfo] = None


@dataclass
class BatchBindOrderSkuIdentifyCodeInfoResponse:
    """Batch bind order SKU identify code info response."""

    success_count: int = 0
    failed_count: int = 0
    failed_orders: List[str] = field(default_factory=list)


@dataclass
class GetCustomsInfoResponse:
    """Get customs info response."""

    order_id: Optional[str] = None
    customs_status: Optional[CustomsStatusInfo] = None
    customs_items: List[CustomsItem] = field(default_factory=list)


@dataclass
class GetOrderReceiverInfoResponse:
    """Get order receiver info response."""

    receiver_info: Optional[ReceiverInfo] = None


@dataclass
class GetOrderTrackingResponse:
    """Get order tracking response."""

    tracking_info: Optional[TrackingInfo] = None


@dataclass
class GetOrderDeclareInfoResponse:
    """Get order declare info response."""

    declare_info: Optional[DeclareInfo] = None


@dataclass
class GetSupportedPortListResponse:
    """Get supported port list response."""

    ports: List[SupportedPort] = field(default_factory=list)


@dataclass
class CreateTransferBatchResponse:
    """Create transfer batch response."""

    transfer_batch: Optional[TransferBatch] = None


@dataclass
class GetKosDataResponse:
    """Get KOS data response."""

    kos_data: List[KosData] = field(default_factory=list)
