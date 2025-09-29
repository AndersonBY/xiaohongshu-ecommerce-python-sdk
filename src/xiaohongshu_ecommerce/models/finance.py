"""Finance domain models for Xiaohongshu e-commerce API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .base import BaseRequest


class SettleStatus(Enum):
    """Settlement status enumeration."""

    WAIT_SETTLE = 0
    SETTLED = 1


# Request Models
@dataclass
class QueryCpsSettleRequest(BaseRequest):
    """Query CPS settlement request."""

    package_id: Optional[str] = None

    def __init__(self, package_id: Optional[str] = None):
        super().__init__("")  # method will be set by the client
        self.package_id = package_id

    def extra_payload(self) -> Dict[str, Any]:
        return {
            "packageId": self.package_id,
        }


@dataclass
class DownloadStatementRequest(BaseRequest):
    """Download statement request."""

    month: Optional[str] = None

    def __init__(self, month: Optional[str] = None):
        super().__init__("")  # method will be set by the client
        self.month = month

    def extra_payload(self) -> Dict[str, Any]:
        return {
            "month": self.month,
        }


@dataclass
class QuerySellerAccountRecordsRequest(BaseRequest):
    """Query seller account records request."""

    start_time: Optional[int] = None
    end_time: Optional[int] = None
    page_num: Optional[int] = None
    page_size: Optional[int] = None
    business_no: Optional[str] = None
    debit_type: Optional[str] = None
    trade_types: Optional[List[str]] = None
    fund_type: Optional[int] = None

    def __init__(
        self,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        page_num: Optional[int] = None,
        page_size: Optional[int] = None,
        business_no: Optional[str] = None,
        debit_type: Optional[str] = None,
        trade_types: Optional[List[str]] = None,
        fund_type: Optional[int] = None,
    ):
        super().__init__("")  # method will be set by the client
        self.start_time = start_time
        self.end_time = end_time
        self.page_num = page_num
        self.page_size = page_size
        self.business_no = business_no
        self.debit_type = debit_type
        self.trade_types = trade_types
        self.fund_type = fund_type

    def extra_payload(self) -> Dict[str, Any]:
        return {
            "startTime": self.start_time,
            "endTime": self.end_time,
            "pageNum": self.page_num,
            "pageSize": self.page_size,
            "businessNo": self.business_no,
            "debitType": self.debit_type,
            "tradeTypes": self.trade_types,
            "fundType": self.fund_type,
        }


@dataclass
class PageQueryTransactionRequest(BaseRequest):
    """Page query transaction request."""

    settle_biz_type: Optional[int] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    erqing_type: Optional[int] = None
    common_settle_status: Optional[int] = None
    page_num: Optional[int] = None
    page_size: Optional[int] = None
    should_load_goods_info: Optional[bool] = None

    def __init__(
        self,
        settle_biz_type: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        erqing_type: Optional[int] = None,
        common_settle_status: Optional[int] = None,
        page_num: Optional[int] = None,
        page_size: Optional[int] = None,
        should_load_goods_info: Optional[bool] = None,
    ):
        super().__init__("")  # method will be set by the client
        self.settle_biz_type = settle_biz_type
        self.start_time = start_time
        self.end_time = end_time
        self.erqing_type = erqing_type
        self.common_settle_status = common_settle_status
        self.page_num = page_num
        self.page_size = page_size
        self.should_load_goods_info = should_load_goods_info

    def extra_payload(self) -> Dict[str, Any]:
        return {
            "settleBizType": self.settle_biz_type,
            "startTime": self.start_time,
            "endTime": self.end_time,
            "erqingType": self.erqing_type,
            "commonSettleStatus": self.common_settle_status,
            "pageNum": self.page_num,
            "pageSize": self.page_size,
            "shouldLoadGoodsInfo": self.should_load_goods_info,
        }


@dataclass
class PageQueryExpenseRequest(BaseRequest):
    """Page query expense request."""

    start_time: Optional[int] = None
    end_time: Optional[int] = None
    page_num: Optional[int] = None
    page_size: Optional[int] = None
    base_biz_type: Optional[int] = None
    settle_status: Optional[int] = None

    def __init__(
        self,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        page_num: Optional[int] = None,
        page_size: Optional[int] = None,
        base_biz_type: Optional[int] = None,
        settle_status: Optional[int] = None,
    ):
        super().__init__("")  # method will be set by the client
        self.start_time = start_time
        self.end_time = end_time
        self.page_num = page_num
        self.page_size = page_size
        self.base_biz_type = base_biz_type
        self.settle_status = settle_status

    def extra_payload(self) -> Dict[str, Any]:
        return {
            "startTime": self.start_time,
            "endTime": self.end_time,
            "pageNum": self.page_num,
            "pageSize": self.page_size,
            "baseBizType": self.base_biz_type,
            "settleStatus": self.settle_status,
        }


# Response Data Models
@dataclass
class CpsUserSettleDetail:
    """CPS user settlement detail."""

    package_id: Optional[str] = None
    return_ids: Optional[List[str]] = None
    goods_id: Optional[str] = None
    goods_name: Optional[str] = None
    goods_total: Optional[int] = None
    seller_id: Optional[str] = None
    kol_user_id: Optional[str] = None
    kol_user_name: Optional[str] = None
    deal_total_amount: Optional[int] = None
    return_total_amount: Optional[int] = None
    tax_total_amount: Optional[int] = None
    carrying_total_amount: Optional[int] = None
    seller_rate: Optional[int] = None
    kol_user_share_ratio: Optional[int] = None
    kol_user_rate: Optional[int] = None
    kol_user_commission_amount: Optional[int] = None
    settle_status: Optional[SettleStatus] = None
    order_time: Optional[int] = None
    finish_time: Optional[int] = None
    can_settle_time: Optional[int] = None
    settle_time: Optional[int] = None


@dataclass
class TransactionGoodsDetail:
    """Transaction goods detail."""

    transaction_id: Optional[int] = None
    new_sku_id: Optional[str] = None
    new_sku_quantity: Optional[int] = None
    raw_amount: Optional[str] = None
    pay_amount: Optional[str] = None
    seller_promotion: Optional[str] = None
    app_promotion: Optional[str] = None
    goods_amount: Optional[str] = None
    no_goods_reason: Optional[str] = None
    tax_amount: Optional[str] = None
    no_tax_reason: Optional[str] = None
    commission_amount: Optional[str] = None
    service_commission_amount: Optional[str] = None
    red_commission_amount: Optional[str] = None
    no_commission_reason: Optional[str] = None
    cps_amount: Optional[str] = None
    no_cps_reason: Optional[str] = None
    commission_return_amount: Optional[str] = None
    no_commission_return_reason: Optional[str] = None


@dataclass
class Transaction:
    """Transaction detail."""

    transaction_id: Optional[int] = None
    package_id: Optional[str] = None
    statement_type: Optional[int] = None
    transaction_biz_type: Optional[int] = None
    settle_biz_type: Optional[int] = None
    delivery_id: Optional[str] = None
    transaction_biz_no: Optional[str] = None
    return_id: Optional[str] = None
    order_time: Optional[int] = None
    can_settle_time: Optional[int] = None
    settled_time: Optional[int] = None
    predictable_settle_time: Optional[str] = None
    erqing_type: Optional[int] = None
    transaction_settle_status: Optional[int] = None
    common_settle_status: Optional[int] = None
    amount: Optional[str] = None
    goods_amount: Optional[str] = None
    pay_amount: Optional[str] = None
    app_promotion: Optional[str] = None
    freight_amount: Optional[str] = None
    freight_app_promotion: Optional[str] = None
    no_freight_reason: Optional[str] = None
    tax_amount: Optional[str] = None
    no_tax_reason: Optional[str] = None
    freight_tax_amount: Optional[str] = None
    no_freight_tax_reason: Optional[str] = None
    commission_amount: Optional[str] = None
    pay_channel_amount: Optional[str] = None
    no_pay_channel_reason: Optional[str] = None
    cps_amount: Optional[str] = None
    installment_amount: Optional[str] = None
    no_installment_reason: Optional[str] = None
    extra_amount: Optional[str] = None
    no_extra_reason: Optional[str] = None
    calculate_remark: Optional[str] = None
    goods_details: Optional[List[TransactionGoodsDetail]] = None


# Response Models
@dataclass
class QueryCpsSettleResponse:
    """Query CPS settlement response."""

    cps_user_settle_details: Optional[List[CpsUserSettleDetail]] = field(
        default_factory=list
    )


@dataclass
class DownloadStatementResponse:
    """Download statement response."""

    # Based on Java pattern, this seems to be a file download response
    # The actual structure may depend on the API implementation
    download_url: Optional[str] = None
    file_name: Optional[str] = None


@dataclass
class QuerySellerAccountRecordsResponse:
    """Query seller account records response."""

    # Based on Java pattern, specific structure not available in decompiled code
    # Will need to be determined from actual API response
    records: Optional[List[Dict[str, Any]]] = field(default_factory=list)


@dataclass
class PageQueryTransactionResponse:
    """Page query transaction response."""

    page_num: Optional[int] = None
    page_size: Optional[int] = None
    total: Optional[int] = None
    total_page: Optional[int] = None
    transactions: Optional[List[Transaction]] = field(default_factory=list)


@dataclass
class PageQueryExpenseResponse:
    """Page query expense response."""

    # Based on pattern similarity with PageQueryTransactionResponse
    page_num: Optional[int] = None
    page_size: Optional[int] = None
    total: Optional[int] = None
    total_page: Optional[int] = None
    expenses: Optional[List[Dict[str, Any]]] = field(default_factory=list)
