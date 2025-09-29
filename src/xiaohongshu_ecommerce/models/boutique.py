"""Boutique module models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Mapping, Optional

from .base import BaseRequest


class BoutiqueMode(str, Enum):
    DOMESTIC_GENERAL_SHIPPING = "DOMESTIC_GENERAL_SHIPPING"
    DOMESTIC_FAST_SHIPPING = "DOMESTIC_FAST_SHIPPING"
    INCLUDE_TAX_FAST_SHIPPING = "INCLUDE_TAX_FAST_SHIPPING"
    INTERNATIONAL_DIRECT_GENERAL_SHIPPING = "INTERNATIONAL_DIRECT_GENERAL_SHIPPING"
    INTERNATIONAL_DIRECT_FAST_SHIPPING = "INTERNATIONAL_DIRECT_FAST_SHIPPING"


class OperationType(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


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


def _opt_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _opt_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    return bool(value)


def _serialize_modes(modes: list[BoutiqueMode]) -> list[str]:
    return [mode.value for mode in modes]


class CreateBoutiqueItemRequest(BaseRequest):
    def __init__(
        self,
        *,
        spu_id: str,
        boutique_modes: list[BoutiqueMode] | None = None,
        with_item_detail: bool = False,
        operation_type: OperationType | None = None,
    ) -> None:
        super().__init__(method="boutique.createBoutiqueItem")
        self.spu_id = spu_id
        self.boutique_modes = boutique_modes or []
        self.with_item_detail = with_item_detail
        self.operation_type = operation_type

    def extra_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "spuId": self.spu_id,
            "withItemDetail": self.with_item_detail,
        }
        if self.boutique_modes:
            payload["boutiqueModes"] = _serialize_modes(self.boutique_modes)
        if self.operation_type is not None:
            payload["operationType"] = self.operation_type.value
        return payload


class CreateBoutiqueSkuRequest(BaseRequest):
    def __init__(
        self,
        *,
        item_id: str,
        boutique_modes: list[BoutiqueMode] | None = None,
        with_sku_detail: bool = False,
        operation_type: OperationType | None = None,
    ) -> None:
        super().__init__(method="boutique.createBoutiqueSku")
        self.item_id = item_id
        self.boutique_modes = boutique_modes or []
        self.with_sku_detail = with_sku_detail
        self.operation_type = operation_type

    def extra_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "itemId": self.item_id,
            "withSkuDetail": self.with_sku_detail,
        }
        if self.boutique_modes:
            payload["boutiqueModes"] = _serialize_modes(self.boutique_modes)
        if self.operation_type is not None:
            payload["operationType"] = self.operation_type.value
        return payload


@dataclass
class BoutiqueItemBatchInfo:
    boutique_batch_id: Optional[str] = None
    identity_id: Optional[str] = None
    free_return: Optional[int] = None
    skucode: Optional[str] = None
    whcode: Optional[str] = None
    qty: Optional[int] = None

    def to_payload(self) -> Dict[str, Any]:
        return {
            key: value
            for key, value in {
                "boutiqueBatchId": self.boutique_batch_id,
                "identityId": self.identity_id,
                "freeReturn": self.free_return,
                "skucode": self.skucode,
                "whcode": self.whcode,
                "qty": self.qty,
            }.items()
            if value is not None
        }


@dataclass
class StockOperateInfo:
    operate_type: Optional[int] = None
    operator: Optional[str] = None
    remark: Optional[str] = None

    def to_payload(self) -> Dict[str, Any]:
        return {
            key: value
            for key, value in {
                "operateType": self.operate_type,
                "operator": self.operator,
                "remark": self.remark,
            }.items()
            if value is not None
        }


class UpdateBoutiqueItemRequest(BaseRequest):
    def __init__(
        self,
        *,
        item_id: str,
        boutique_item_batch_info: BoutiqueItemBatchInfo | None = None,
        boutique_batch_id: Optional[str] = None,
        identity_id: Optional[str] = None,
        with_item_detail: bool = False,
        free_return: Optional[int] = None,
        skucode: Optional[str] = None,
        whcode: Optional[str] = None,
        qty: Optional[int] = None,
        operate_info: StockOperateInfo | None = None,
    ) -> None:
        super().__init__(method="boutique.updateBoutiqueItem")
        self.item_id = item_id
        self.boutique_item_batch_info = boutique_item_batch_info
        self.boutique_batch_id = boutique_batch_id
        self.identity_id = identity_id
        self.with_item_detail = with_item_detail
        self.free_return = free_return
        self.skucode = skucode
        self.whcode = whcode
        self.qty = qty
        self.operate_info = operate_info

    def extra_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "itemId": self.item_id,
            "withItemDetail": self.with_item_detail,
        }
        if self.boutique_item_batch_info is not None:
            payload["boutiqueItemBatchInfo"] = (
                self.boutique_item_batch_info.to_payload()
            )
        if self.boutique_batch_id is not None:
            payload["boutiqueBatchId"] = self.boutique_batch_id
        if self.identity_id is not None:
            payload["identityId"] = self.identity_id
        if self.free_return is not None:
            payload["freeReturn"] = self.free_return
        if self.skucode is not None:
            payload["skucode"] = self.skucode
        if self.whcode is not None:
            payload["whcode"] = self.whcode
        if self.qty is not None:
            payload["qty"] = self.qty
        if self.operate_info is not None:
            payload["operateInfo"] = self.operate_info.to_payload()
        return payload


class UpdateBoutiqueSkuRequest(BaseRequest):
    def __init__(
        self,
        *,
        sku_id: str,
        boutique_sku_batch_info: BoutiqueItemBatchInfo | None = None,
        boutique_batch_id: Optional[str] = None,
        identity_id: Optional[str] = None,
        with_sku_detail: bool = False,
        free_return: Optional[int] = None,
        sc_skucode: Optional[str] = None,
        whcode: Optional[str] = None,
        qty: Optional[int] = None,
        operate_info: StockOperateInfo | None = None,
    ) -> None:
        super().__init__(method="boutique.updateBoutiqueSku")
        self.sku_id = sku_id
        self.boutique_sku_batch_info = boutique_sku_batch_info
        self.boutique_batch_id = boutique_batch_id
        self.identity_id = identity_id
        self.with_sku_detail = with_sku_detail
        self.free_return = free_return
        self.sc_skucode = sc_skucode
        self.whcode = whcode
        self.qty = qty
        self.operate_info = operate_info

    def extra_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "skuId": self.sku_id,
            "withSkuDetail": self.with_sku_detail,
        }
        if self.boutique_sku_batch_info is not None:
            payload["boutiqueSkuBatchInfo"] = self.boutique_sku_batch_info.to_payload()
        if self.boutique_batch_id is not None:
            payload["boutiqueBatchId"] = self.boutique_batch_id
        if self.identity_id is not None:
            payload["identityId"] = self.identity_id
        if self.free_return is not None:
            payload["freeReturn"] = self.free_return
        if self.sc_skucode is not None:
            payload["scSkucode"] = self.sc_skucode
        if self.whcode is not None:
            payload["whcode"] = self.whcode
        if self.qty is not None:
            payload["qty"] = self.qty
        if self.operate_info is not None:
            payload["operateInfo"] = self.operate_info.to_payload()
        return payload


@dataclass
class BasicBoutiqueItemData:
    item_id: Optional[str]
    name: Optional[str]
    price: Optional[float]
    skucode: Optional[str]
    buyable: Optional[bool]
    barcode: Optional[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "BasicBoutiqueItemData":
        return cls(
            item_id=_opt_str(data.get("itemId")),
            name=_opt_str(data.get("name")),
            price=_opt_float(data.get("price")),
            skucode=_opt_str(data.get("skucode")),
            buyable=_opt_bool(data.get("buyable")),
            barcode=_opt_str(data.get("barcode")),
        )


@dataclass
class BasicBoutiqueSkuData:
    sku_id: Optional[str]
    name: Optional[str]
    price: Optional[float]
    sc_skucode: Optional[str]
    buyable: Optional[bool]
    barcode: Optional[str]
    whcode: Optional[str]
    stock: Optional[int]
    boutique_mode: Optional[str]
    boutique_mode_name: Optional[str]
    vendor_code: Optional[str]
    boutique_batch_id: Optional[str]
    create_time: Optional[int]
    update_time: Optional[int]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "BasicBoutiqueSkuData":
        return cls(
            sku_id=_opt_str(data.get("skuId")),
            name=_opt_str(data.get("name")),
            price=_opt_float(data.get("price")),
            sc_skucode=_opt_str(data.get("scSkucode")),
            buyable=_opt_bool(data.get("buyable")),
            barcode=_opt_str(data.get("barcode")),
            whcode=_opt_str(data.get("whcode")),
            stock=_opt_int(data.get("stock")),
            boutique_mode=_opt_str(data.get("boutiqueMode")),
            boutique_mode_name=_opt_str(data.get("boutiqueModeName")),
            vendor_code=_opt_str(data.get("vendorCode")),
            boutique_batch_id=_opt_str(data.get("boutiqueBatchId")),
            create_time=_opt_int(data.get("createTime")),
            update_time=_opt_int(data.get("updateTime")),
        )


@dataclass
class CreateBoutiqueItemResponse:
    data: Mapping[str, Any]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "CreateBoutiqueItemResponse":
        return cls(data=data)


@dataclass
class CreateBoutiqueSkuResponse:
    data: Mapping[str, Any]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "CreateBoutiqueSkuResponse":
        return cls(data=data)


__all__ = [
    "BoutiqueMode",
    "OperationType",
    "CreateBoutiqueItemRequest",
    "CreateBoutiqueSkuRequest",
    "UpdateBoutiqueItemRequest",
    "UpdateBoutiqueSkuRequest",
    "BoutiqueItemBatchInfo",
    "StockOperateInfo",
    "BasicBoutiqueItemData",
    "BasicBoutiqueSkuData",
    "CreateBoutiqueItemResponse",
    "CreateBoutiqueSkuResponse",
]
