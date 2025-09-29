"""Invoice domain models for Xiaohongshu e-commerce API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from .base import BaseRequest


@dataclass
class GetInvoiceListRequest(BaseRequest):
    """Request for getting invoice list."""

    invoice_status: Optional[int] = None
    ref_no: Optional[str] = None
    start_date_long: Optional[int] = None
    end_date_long: Optional[int] = None
    page_num: Optional[int] = None
    page_size: Optional[int] = None
    sort_enum: Optional[int] = None
    title_type: Optional[int] = None

    def __init__(self, method: str = "") -> None:
        super().__init__(method)


@dataclass
class ConfirmInvoiceRequest(BaseRequest):
    """Request for confirming invoice."""

    xhs_invoice_no: Optional[str] = None
    ref_no: Optional[str] = None
    invoice_type: Optional[int] = None
    file: Optional[bytes] = None
    invoice_no: Optional[str] = None
    operator_id: Optional[str] = None
    operator_name: Optional[str] = None

    def __init__(self, method: str = "") -> None:
        super().__init__(method)


@dataclass
class ReverseInvoiceRequest(BaseRequest):
    """Request for reversing invoice."""

    xhs_invoice_no: Optional[str] = None
    operator_id: Optional[str] = None
    operator_name: Optional[str] = None

    def __init__(self, method: str = "") -> None:
        super().__init__(method)


@dataclass
class InvoiceFile:
    """Invoice file information."""

    origin_url: Optional[str] = None
    download_url: Optional[str] = None
    file_name: Optional[str] = None


@dataclass
class InvoiceItem:
    """Invoice item information."""

    item_id: Optional[str] = None
    item_name: Optional[str] = None
    price: Optional[str] = None
    tax_rate: Optional[str] = None
    bought_count: Optional[str] = None


@dataclass
class InvoiceRecord:
    """Invoice record information."""

    invoice_status: Optional[int] = None
    xhs_invoice_no: Optional[str] = None
    apply_time: Optional[int] = None
    title: Optional[str] = None
    tax_no: Optional[str] = None
    tax_bank_account: Optional[str] = None
    tax_bank_name: Optional[str] = None
    invoice_type: Optional[int] = None
    invoice_amt: Optional[str] = None
    invoice_nos: Optional[str] = None
    invoice_total_amt: Optional[str] = None
    ref_no: Optional[str] = None
    title_type: Optional[int] = None
    updated_time: Optional[int] = None
    attr_map: Optional[Dict[str, str]] = None
    item_list: Optional[List[InvoiceItem]] = None
    invoice_file_list: Optional[List[InvoiceFile]] = None
    pic_url: Optional[str] = None
    pdf_url: Optional[str] = None


@dataclass
class GetInvoiceListResponse:
    """Response for getting invoice list."""

    page_size: Optional[int] = None
    page_index: Optional[int] = None
    total: Optional[int] = None
    total_page: Optional[int] = None
    invoice_records: Optional[List[InvoiceRecord]] = None
