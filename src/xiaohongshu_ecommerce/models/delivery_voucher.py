"""Delivery voucher models for Xiaohongshu e-commerce API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseRequest


@dataclass
class DeliveryVoucherDTO:
    """Delivery voucher DTO."""

    id: Optional[str] = None
    no: Optional[str] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None


@dataclass
class DeliveryVoucherInfoDTO:
    """Delivery voucher info DTO."""

    sku_id: Optional[str] = None
    delivery_vouchers: List[DeliveryVoucherDTO] = field(default_factory=list)


# Request models
@dataclass
class BindOrderDeliveryVoucherRequest(BaseRequest):
    """Bind order delivery voucher request."""

    action_time: Optional[int] = None
    trace_id: Optional[str] = None
    order_id: Optional[str] = None
    voucher_infos: List[DeliveryVoucherInfoDTO] = field(default_factory=list)
    feature: Optional[str] = None


@dataclass
class DeliveryVoucherActionRequest(BaseRequest):
    """Delivery voucher action request."""

    order_id: Optional[str] = None
    voucher_id: Optional[str] = None
    voucher_no: Optional[str] = None
    trace_id: Optional[str] = None
    action_time: Optional[int] = None
    action_type: Optional[str] = None
    express_no: Optional[str] = None
    express_company_code: Optional[str] = None
    express_company_name: Optional[str] = None
    receiver_name: Optional[str] = None
    receiver_mobile: Optional[str] = None
    receiver_address: Optional[str] = None
