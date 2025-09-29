"""Package domain models for Xiaohongshu e-commerce API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from .base import BaseRequest


class PackageStatusEnum(Enum):
    """Package status enumeration."""

    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PackageTypeEnum(Enum):
    """Package type enumeration."""

    NORMAL = "normal"
    BONDED = "bonded"
    OVERSEAS = "overseas"


@dataclass
class PackageSimpleDetail:
    """Simple package detail."""

    package_id: Optional[str] = None
    package_no: Optional[str] = None
    package_status: Optional[int] = None
    package_type: Optional[int] = None
    create_time: Optional[int] = None
    update_time: Optional[int] = None
    total_amount: Optional[float] = None
    actual_amount: Optional[float] = None
    buyer_id: Optional[str] = None
    seller_id: Optional[str] = None


@dataclass
class PackageDetailInfo:
    """Detailed package information."""

    package_id: Optional[str] = None
    package_no: Optional[str] = None
    package_status: Optional[int] = None
    package_type: Optional[int] = None
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
    package_items: List[dict] = field(default_factory=list)
    customs_info: Optional[dict] = None


@dataclass
class PackageCustomsItem:
    """Package customs item information."""

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
class PackageReceiverInfo:
    """Package receiver information."""

    name: Optional[str] = None
    phone: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    id_card: Optional[str] = None


@dataclass
class PackageTrackingInfo:
    """Package tracking information."""

    express_company: Optional[str] = None
    express_no: Optional[str] = None
    tracking_details: List[dict] = field(default_factory=list)


@dataclass
class PackageDeclareInfo:
    """Package declare information."""

    declare_no: Optional[str] = None
    declare_status: Optional[int] = None
    customs_code: Optional[str] = None
    port_code: Optional[str] = None
    declare_items: List[PackageCustomsItem] = field(default_factory=list)


@dataclass
class PackageSupportedPort:
    """Package supported port information."""

    port_code: Optional[str] = None
    port_name: Optional[str] = None
    customs_code: Optional[str] = None


@dataclass
class CancelApplyInfo:
    """Cancel apply information."""

    apply_id: Optional[str] = None
    package_id: Optional[str] = None
    apply_status: Optional[int] = None
    apply_reason: Optional[str] = None
    apply_time: Optional[int] = None
    audit_result: Optional[str] = None
    audit_time: Optional[int] = None


@dataclass
class PackageTransferBatch:
    """Package transfer batch information."""

    batch_id: Optional[str] = None
    batch_no: Optional[str] = None
    status: Optional[int] = None
    create_time: Optional[int] = None


# Request models
@dataclass
class GetPackageListRequest(BaseRequest):
    """Get package list request."""

    start_time: Optional[int] = None
    end_time: Optional[int] = None
    time_type: Optional[int] = None
    package_type: Optional[int] = None
    package_status: Optional[int] = None
    page_no: Optional[int] = None
    page_size: Optional[int] = None


@dataclass
class GetPackageDetailRequest(BaseRequest):
    """Get package detail request."""

    package_id: Optional[str] = None
    package_no: Optional[str] = None


@dataclass
class ResendBondedPaymentRequest(BaseRequest):
    """Resend bonded payment request."""

    package_id: Optional[str] = None
    payment_no: Optional[str] = None


@dataclass
class SyncItemCustomsRequest(BaseRequest):
    """Sync item customs request."""

    package_id: Optional[str] = None
    customs_items: List[PackageCustomsItem] = field(default_factory=list)


@dataclass
class GetItemCustomInfoRequest(BaseRequest):
    """Get item customs info request."""

    package_id: Optional[str] = None


@dataclass
class GetReceiverInfoRequest(BaseRequest):
    """Get receiver info request."""

    package_id: Optional[str] = None


@dataclass
class ModifyPackageExpressRequest(BaseRequest):
    """Modify package express request."""

    package_id: Optional[str] = None
    express_company: Optional[str] = None
    express_no: Optional[str] = None


@dataclass
class PackageDeliverRequest(BaseRequest):
    """Package deliver request."""

    package_id: Optional[str] = None
    express_company: Optional[str] = None
    express_no: Optional[str] = None
    delivery_time: Optional[int] = None


@dataclass
class ModifySellerMarkRequest(BaseRequest):
    """Modify seller mark request."""

    package_id: Optional[str] = None
    seller_mark: Optional[str] = None


@dataclass
class GetPackageTrackRequest(BaseRequest):
    """Get package tracking request."""

    package_id: Optional[str] = None
    express_no: Optional[str] = None


@dataclass
class GetPackageDeclareRequest(BaseRequest):
    """Get package declare request."""

    package_id: Optional[str] = None


@dataclass
class GetSupportedPortListRequest(BaseRequest):
    """Get supported port list request."""

    customs_code: Optional[str] = None


@dataclass
class GetCancelApplyListRequest(BaseRequest):
    """Get cancel apply list request."""

    start_time: Optional[int] = None
    end_time: Optional[int] = None
    status: Optional[int] = None
    page_no: Optional[int] = None
    page_size: Optional[int] = None


@dataclass
class AuditCancelApplyRequest(BaseRequest):
    """Audit cancel apply request."""

    apply_id: Optional[str] = None
    audit_result: Optional[int] = None
    audit_reason: Optional[str] = None


@dataclass
class AddDeclarePortRequest(BaseRequest):
    """Add declare port request."""

    package_id: Optional[str] = None
    port_code: Optional[str] = None


@dataclass
class UpdateProxyPackageWeightRequest(BaseRequest):
    """Update proxy package weight request."""

    package_id: Optional[str] = None
    weight: Optional[float] = None


@dataclass
class CreateTransferBatchRequest(BaseRequest):
    """Create transfer batch request."""

    package_ids: List[str] = field(default_factory=list)
    batch_type: Optional[int] = None


# Response models
@dataclass
class GetPackagesListResponse:
    """Get packages list response."""

    total: int = 0
    page_no: int = 0
    page_size: int = 0
    max_page_no: int = 0
    package_list: List[PackageSimpleDetail] = field(default_factory=list)


@dataclass
class GetPackageDetailResponse:
    """Get package detail response."""

    package_detail: Optional[PackageDetailInfo] = None


@dataclass
class GetItemCustomsInfoResponse:
    """Get item customs info response."""

    package_id: Optional[str] = None
    customs_items: List[PackageCustomsItem] = field(default_factory=list)


@dataclass
class GetReceiveInfoResponse:
    """Get receive info response."""

    receiver_info: Optional[PackageReceiverInfo] = None


@dataclass
class GetPackageTrackResponse:
    """Get package tracking response."""

    tracking_info: Optional[PackageTrackingInfo] = None


@dataclass
class GetPackageDeclareResponse:
    """Get package declare response."""

    declare_info: Optional[PackageDeclareInfo] = None


@dataclass
class GetSupportedPortListResponse:
    """Get supported port list response."""

    ports: List[PackageSupportedPort] = field(default_factory=list)


@dataclass
class GetCancelApplyListResponse:
    """Get cancel apply list response."""

    total: int = 0
    page_no: int = 0
    page_size: int = 0
    max_page_no: int = 0
    apply_list: List[CancelApplyInfo] = field(default_factory=list)


@dataclass
class CreateTransferBatchResponse:
    """Create transfer batch response."""

    transfer_batch: Optional[PackageTransferBatch] = None
