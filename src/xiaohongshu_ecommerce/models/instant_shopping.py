"""Instant shopping models for Xiaohongshu e-commerce API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseRequest


@dataclass
class AddressLocation:
    """Address location information."""

    latitude: Optional[str] = None
    longitude: Optional[str] = None
    address: Optional[str] = None


@dataclass
class InstantShoppingTrackingDTO:
    """Instant shopping tracking DTO."""

    xhs_order_id: Optional[str] = None
    express_company_code: Optional[str] = None
    express_no: Optional[str] = None
    leaf_node_type: Optional[str] = None
    event_at: Optional[str] = None
    event_desc: Optional[str] = None
    current_location: Optional[AddressLocation] = None
    exception_code: Optional[str] = None
    exception_reason: Optional[str] = None
    courier_name: Optional[str] = None
    courier_phone: Optional[str] = None
    courier_phone_type: Optional[str] = None
    expect_arrival_time: Optional[str] = None
    delivery_distance: Optional[str] = None


# Request models
@dataclass
class UpdateInstantShoppingTrackRequest(BaseRequest):
    """Update instant shopping track request."""

    xhs_order_id: Optional[str] = None
    express_no: Optional[str] = None
    express_company_code: Optional[str] = None
    traces: List[InstantShoppingTrackingDTO] = field(default_factory=list)


@dataclass
class UpdateRiderLocationRequest(BaseRequest):
    """Update rider location request."""

    xhs_order_id: Optional[str] = None
    express_no: Optional[str] = None
    express_company_code: Optional[str] = None
    courier_name: Optional[str] = None
    courier_phone: Optional[str] = None
    current_location: Optional[AddressLocation] = None
    status: Optional[str] = None
    status_desc: Optional[str] = None
