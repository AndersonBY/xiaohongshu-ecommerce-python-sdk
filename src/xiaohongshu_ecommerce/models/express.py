"""Express domain models for Xiaohongshu e-commerce API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseRequest


# Core entity models
@dataclass
class ElectronicBillAddress:
    """Electronic bill address information."""

    city: Optional[str] = None
    detail: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    town: Optional[str] = None


@dataclass
class ElectronicBillUserInfo:
    """Electronic bill user information."""

    address: Optional[ElectronicBillAddress] = None
    mobile: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    open_address_id: Optional[str] = None


@dataclass
class ElectronicBillItem:
    """Electronic bill item information."""

    count: Optional[int] = None
    name: Optional[str] = None
    specification: Optional[str] = None


@dataclass
class ElectronicBillOrderInfo:
    """Electronic bill order information."""

    order_channels_type: Optional[str] = None
    trade_order_list: List[str] = field(default_factory=list)
    buyer_memo: List[str] = field(default_factory=list)
    seller_memo: List[str] = field(default_factory=list)
    xhs_order_id: Optional[str] = None
    xhs_order_list: List[str] = field(default_factory=list)


@dataclass
class ElectronicBillPackageInfo:
    """Electronic bill package information."""

    id: Optional[str] = None
    items: List[ElectronicBillItem] = field(default_factory=list)
    volume: Optional[int] = None
    weight: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    total_packages_count: Optional[int] = None
    packaging_description: Optional[str] = None
    goods_description: Optional[str] = None
    good_value: Optional[float] = None


@dataclass
class ElectronicBillTradeOrderInfo:
    """Electronic bill trade order information."""

    logistics_services: Optional[str] = None
    object_id: Optional[str] = None
    order_info: Optional[ElectronicBillOrderInfo] = None
    package_info: Optional[ElectronicBillPackageInfo] = None
    recipient: Optional[ElectronicBillUserInfo] = None
    returns_recipient: Optional[ElectronicBillUserInfo] = None
    template_id: Optional[int] = None
    deliver_extend_info: Optional[str] = None


# Response entity models
@dataclass
class Subscribe:
    """Subscribe information in query response."""

    cp_code: Optional[str] = None
    cp_name: Optional[str] = None
    cp_type: Optional[int] = None
    branch_code: Optional[str] = None
    branch_name: Optional[str] = None
    brand_code: Optional[str] = None
    customer_code: Optional[str] = None
    subscribe_type: Optional[str] = None
    sender_address_list: List[SenderAddress] = field(default_factory=list)
    usage: Optional[Usage] = None


@dataclass
class SenderAddress:
    """Sender address information."""

    address: Optional[ElectronicBillAddress] = None
    mobile: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None


@dataclass
class Usage:
    """Usage statistics information."""

    quantity: Optional[int] = None
    allocated_quantity: Optional[int] = None
    cancel_quantity: Optional[int] = None
    recycled_quantity: Optional[int] = None


@dataclass
class Template:
    """Template information in query response."""

    id: Optional[int] = None
    cp_code: Optional[str] = None
    brand_code: Optional[str] = None
    template_type: Optional[str] = None
    template_customer_type: Optional[int] = None
    template_name: Optional[str] = None
    template_desc: Optional[str] = None
    template_preview_url: Optional[str] = None
    standard_template_url: Optional[str] = None
    customer_template_url: Optional[str] = None
    customer_print_items: List[str] = field(default_factory=list)


# Request models
@dataclass
class QueryEbillSubscribesRequest(BaseRequest):
    """Query electronic bill subscribes request."""

    bill_version: Optional[int] = None
    cp_code: Optional[str] = None
    need_usage: Optional[bool] = None
    brand_code: Optional[str] = None


@dataclass
class QueryEbillTemplatesRequest(BaseRequest):
    """Query electronic bill templates request."""

    bill_version: Optional[int] = None
    cp_code: Optional[str] = None
    brand_code: Optional[str] = None
    type: Optional[str] = None
    template_customer_type: Optional[int] = None


@dataclass
class QueryEbillOrderRequest(BaseRequest):
    """Query electronic bill order request."""

    bill_version: Optional[int] = None
    cp_code: Optional[str] = None
    waybill_code: Optional[str] = None


@dataclass
class CreateEbillOrdersRequest(BaseRequest):
    """Create electronic bill orders request."""

    bill_version: Optional[int] = None
    cp_code: Optional[str] = None
    sender: Optional[ElectronicBillUserInfo] = None
    trade_order_info_list: List[ElectronicBillTradeOrderInfo] = field(
        default_factory=list
    )
    extra_info: Optional[str] = None
    customer_code: Optional[str] = None
    brand_code: Optional[str] = None
    product_code: Optional[str] = None
    call_door_pick_up: Optional[bool] = None
    door_pick_up_time: Optional[str] = None
    door_pick_up_end_time: Optional[str] = None
    seller_name: Optional[str] = None
    branch_code: Optional[str] = None
    pay_method: Optional[int] = None


@dataclass
class UpdateEbillOrderRequest(BaseRequest):
    """Update electronic bill order request."""

    bill_version: Optional[int] = None
    cp_code: Optional[str] = None
    waybill_code: Optional[str] = None
    sender: Optional[ElectronicBillUserInfo] = None
    trade_order_info_list: List[ElectronicBillTradeOrderInfo] = field(
        default_factory=list
    )
    extra_info: Optional[str] = None
    customer_code: Optional[str] = None
    brand_code: Optional[str] = None
    product_code: Optional[str] = None
    call_door_pick_up: Optional[bool] = None
    door_pick_up_time: Optional[str] = None
    door_pick_up_end_time: Optional[str] = None
    seller_name: Optional[str] = None
    branch_code: Optional[str] = None
    pay_method: Optional[int] = None


@dataclass
class CancelEbillOrderRequest(BaseRequest):
    """Cancel electronic bill order request."""

    bill_version: Optional[int] = None
    cp_code: Optional[str] = None
    waybill_code: Optional[str] = None
    cancel_reason: Optional[str] = None


# Instant shopping requests (based on user requirements)
@dataclass
class UpdateEbillInstantShoppingTrackRequest(BaseRequest):
    """Update electronic bill instant shopping track request."""

    waybill_code: Optional[str] = None
    track_info: Optional[str] = None
    status: Optional[int] = None
    update_time: Optional[int] = None


@dataclass
class UpdateEbillRiderLocationRequest(BaseRequest):
    """Update electronic bill rider location request."""

    waybill_code: Optional[str] = None
    rider_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_time: Optional[int] = None


# Response models
@dataclass
class QueryEbillSubscribesResponse:
    """Query electronic bill subscribes response."""

    subscribe_list: List[Subscribe] = field(default_factory=list)
    account_id: Optional[int] = None


@dataclass
class QueryEbillTemplatesResponse:
    """Query electronic bill templates response."""

    template_list: List[Template] = field(default_factory=list)


@dataclass
class QueryEbillOrderResponse:
    """Query electronic bill order response."""

    waybill_code: Optional[str] = None
    parent_waybill_code: Optional[str] = None
    print_data: Optional[str] = None
    customer_print_data: Optional[str] = None
    extra_info: Optional[str] = None


@dataclass
class CreateEbillOrdersResponse:
    """Create electronic bill orders response."""

    waybill_codes: List[str] = field(default_factory=list)
    success_count: Optional[int] = None
    failed_count: Optional[int] = None
    sub_error_code: Optional[str] = None


@dataclass
class UpdateEbillOrderResponse:
    """Update electronic bill order response."""

    waybill_code: Optional[str] = None
    success: Optional[bool] = None
    sub_error_code: Optional[str] = None


@dataclass
class CancelEbillOrderResponse:
    """Cancel electronic bill order response."""

    waybill_code: Optional[str] = None
    success: Optional[bool] = None
    sub_error_code: Optional[str] = None
