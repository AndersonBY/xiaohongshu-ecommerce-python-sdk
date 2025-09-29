"""Inventory and warehouse domain models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, MutableMapping, Optional, Sequence

from .base import BaseRequest


def _filter_none(mapping: MutableMapping[str, object]) -> Dict[str, object]:
    return {key: value for key, value in mapping.items() if value is not None}


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


def _as_mapping(value: Any) -> Mapping[str, object]:
    if isinstance(value, Mapping):
        return value
    return {}


def _as_sequence(value: Any) -> List[Any]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return list(value)
    if value is None:
        return []
    return [value]


class GetItemStockRequest(BaseRequest):
    """Request wrapper for ``inventory.getItemStock``."""

    def __init__(self, item_id: str) -> None:
        super().__init__(method="inventory.getItemStock")
        self.item_id = item_id

    def extra_payload(self) -> Dict[str, object]:
        return {"itemId": self.item_id}


class SyncItemStockRequest(BaseRequest):
    """Request wrapper for ``inventory.syncItemStock``."""

    def __init__(
        self,
        item_id: str,
        total_qty: int,
        distribution_mode: Optional[str] = None,
        sku_qty_list: Optional[List] = None,
    ) -> None:
        super().__init__(method="inventory.syncItemStock")
        self.item_id = item_id
        self.total_qty = total_qty
        self.distribution_mode = distribution_mode
        self.sku_qty_list = sku_qty_list or []

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "itemId": self.item_id,
            "totalQty": self.total_qty,
        }
        if self.distribution_mode is not None:
            payload["distributionMode"] = self.distribution_mode
        if self.sku_qty_list:
            payload["skuQtyList"] = self.sku_qty_list
        return payload


class IncItemStockRequest(BaseRequest):
    """Request wrapper for ``inventory.incItemStock``."""

    def __init__(
        self,
        item_id: str,
        qty: int,
        reason: Optional[str] = None,
        reference_id: Optional[str] = None,
        distribution_mode: Optional[str] = None,
        sku_adjustments: Optional[List] = None,
    ) -> None:
        super().__init__(method="inventory.incItemStock")
        self.item_id = item_id
        self.qty = qty
        self.reason = reason
        self.reference_id = reference_id
        self.distribution_mode = distribution_mode
        self.sku_adjustments = sku_adjustments or []

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {"itemId": self.item_id, "qty": self.qty}
        if self.reason is not None:
            payload["reason"] = self.reason
        if self.reference_id is not None:
            payload["referenceId"] = self.reference_id
        if self.distribution_mode is not None:
            payload["distributionMode"] = self.distribution_mode
        if self.sku_adjustments:
            payload["skuAdjustments"] = self.sku_adjustments
        return payload


class GetSkuStockRequest(BaseRequest):
    """Request wrapper for ``inventory.getSkuStock``."""

    def __init__(self, sku_id: str) -> None:
        super().__init__(method="inventory.getSkuStock")
        self.sku_id = sku_id

    def extra_payload(self) -> Dict[str, object]:
        return {"skuId": self.sku_id}


class SyncSkuStockRequest(BaseRequest):
    """Request wrapper for ``inventory.syncSkuStock``."""

    def __init__(self, sku_id: str, qty: int) -> None:
        super().__init__(method="inventory.syncSkuStock")
        self.sku_id = sku_id
        self.qty = qty

    def extra_payload(self) -> Dict[str, object]:
        return {"skuId": self.sku_id, "qty": self.qty}


class IncSkuStockRequest(BaseRequest):
    """Request wrapper for ``inventory.incSkuStock``."""

    def __init__(self, sku_id: str, qty: int) -> None:
        super().__init__(method="inventory.incSkuStock")
        self.sku_id = sku_id
        self.qty = qty

    def extra_payload(self) -> Dict[str, object]:
        return {"skuId": self.sku_id, "qty": self.qty}


class GetSkuStockV2Request(BaseRequest):
    """Request wrapper for ``inventory.getSkuStockV2``."""

    def __init__(self, sku_id: str, inventory_type: Optional[int] = None) -> None:
        super().__init__(method="inventory.getSkuStockV2")
        self.sku_id = sku_id
        self.inventory_type = inventory_type

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {"skuId": self.sku_id}
        if self.inventory_type is not None:
            payload["inventoryType"] = self.inventory_type
        return payload


class SyncSkuStockV2Request(BaseRequest):
    """Request wrapper for ``inventory.syncSkuStockV2``."""

    def __init__(self, sku_id: str, qty_with_whcode: Mapping[str, int]) -> None:
        super().__init__(method="inventory.syncSkuStockV2")
        self.sku_id = sku_id
        self.qty_with_whcode = dict(qty_with_whcode)

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {"skuId": self.sku_id}
        if self.qty_with_whcode:
            payload["qtyWithWhcode"] = self.qty_with_whcode
        return payload


class GetWarehouseRequest(BaseRequest):
    """Request wrapper for ``warehouse.info``."""

    def __init__(self, code: str) -> None:
        super().__init__(method="warehouse.info")
        self.code = code

    def extra_payload(self) -> Dict[str, object]:
        return {"code": self.code}


class CreateWarehouseRequest(BaseRequest):
    """Request wrapper for ``warehouse.create``."""

    def __init__(
        self,
        *,
        code: str,
        name: str,
        zone_code: str,
        address: str,
        contact_name: Optional[str] = None,
        contact_tel: Optional[str] = None,
    ) -> None:
        super().__init__(method="warehouse.create")
        self.code = code
        self.name = name
        self.zone_code = zone_code
        self.address = address
        self.contact_name = contact_name
        self.contact_tel = contact_tel

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "code": self.code,
            "name": self.name,
            "zoneCode": self.zone_code,
            "address": self.address,
        }
        if self.contact_name is not None:
            payload["contactName"] = self.contact_name
        if self.contact_tel is not None:
            payload["contactTel"] = self.contact_tel
        return payload


class UpdateWarehouseRequest(BaseRequest):
    """Request wrapper for ``warehouse.update``."""

    def __init__(
        self,
        *,
        code: str,
        name: Optional[str] = None,
        zone_code: Optional[str] = None,
        address: Optional[str] = None,
        contact_name: Optional[str] = None,
        contact_tel: Optional[str] = None,
    ) -> None:
        super().__init__(method="warehouse.update")
        self.code = code
        self.name = name
        self.zone_code = zone_code
        self.address = address
        self.contact_name = contact_name
        self.contact_tel = contact_tel

    def extra_payload(self) -> Dict[str, object]:
        payload = _filter_none(
            {
                "code": self.code,
                "name": self.name,
                "zoneCode": self.zone_code,
                "address": self.address,
                "contactName": self.contact_name,
                "contactTel": self.contact_tel,
            }
        )
        payload["code"] = self.code
        return payload


class ListWarehouseRequest(BaseRequest):
    """Request wrapper for ``warehouse.list``."""

    def __init__(
        self,
        *,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        code: Optional[str] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(method="warehouse.list")
        self.page_no = page_no
        self.page_size = page_size
        self.code = code
        self.name = name

    def extra_payload(self) -> Dict[str, object]:
        payload = _filter_none(
            {
                "pageNo": self.page_no,
                "pageSize": self.page_size,
                "code": self.code,
                "name": self.name,
            }
        )
        return payload


class SetWarehouseCoverageRequest(BaseRequest):
    """Request wrapper for ``warehouse.setCoverage``."""

    def __init__(self, wh_code: str, zone_code_list: Sequence[str]) -> None:
        super().__init__(method="warehouse.setCoverage")
        self.wh_code = wh_code
        self.zone_code_list = [str(item) for item in zone_code_list]

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {"whCode": self.wh_code}
        if self.zone_code_list:
            payload["zoneCodeList"] = self.zone_code_list
        return payload


class SetWarehousePriorityRequest(BaseRequest):
    """Request wrapper for ``warehouse.setPriority``."""

    class WarehousePriority:
        def __init__(self, wh_code: str) -> None:
            self.wh_code = wh_code

        def to_payload(self) -> Dict[str, object]:
            return {"whCode": self.wh_code}

    def __init__(
        self,
        zone_code: str,
        warehouse_priority_list: Sequence[
            Mapping[str, object] | "SetWarehousePriorityRequest.WarehousePriority" | str
        ],
    ) -> None:
        super().__init__(method="warehouse.setPriority")
        self.zone_code = zone_code
        self.warehouse_priority_list = [
            self._coerce_priority(item) for item in warehouse_priority_list
        ]

    def _coerce_priority(
        self,
        item: Mapping[str, object]
        | "SetWarehousePriorityRequest.WarehousePriority"
        | str,
    ) -> "SetWarehousePriorityRequest.WarehousePriority":
        if isinstance(item, SetWarehousePriorityRequest.WarehousePriority):
            return item
        if isinstance(item, Mapping):
            wh_code = item.get("whCode") or item.get("whcode") or item.get("wh_code")
            if wh_code is None:
                raise ValueError("warehouse priority mapping requires a whCode field")
            return SetWarehousePriorityRequest.WarehousePriority(str(wh_code))
        if isinstance(item, str):
            return SetWarehousePriorityRequest.WarehousePriority(item)
        raise TypeError("Unsupported warehouse priority entry")

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {"zoneCode": self.zone_code}
        if self.warehouse_priority_list:
            payload["warehousePriorityList"] = [
                entry.to_payload() for entry in self.warehouse_priority_list
            ]
        return payload


@dataclass
class ItemStock:
    available: Optional[int] = None
    standalone: Optional[int] = None
    reserved: Optional[int] = None
    total: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "ItemStock":
        return cls(
            available=_opt_int(data.get("available")),
            standalone=_opt_int(data.get("standalone")),
            reserved=_opt_int(data.get("reserved")),
            total=_opt_int(data.get("total")),
        )


@dataclass
class ItemStockResponseData:
    item_id: Optional[str]
    item_stock: ItemStock

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "ItemStockResponseData":
        stock_data = _as_mapping(data.get("itemStock"))
        return cls(
            item_id=_opt_str(data.get("itemId")),
            item_stock=ItemStock.from_dict(stock_data),
        )


@dataclass
class SkuStock:
    available: Optional[int] = None
    standalone: Optional[int] = None
    reserved: Optional[int] = None
    total: Optional[int] = None
    occupied_quantity: Optional[int] = None
    product_channel_quantity: Optional[int] = None
    product_channel_occupied_quantity: Optional[int] = None
    activity_channel_quantity: Optional[int] = None
    activity_channel_occupied_quantity: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "SkuStock":
        return cls(
            available=_opt_int(data.get("available")),
            standalone=_opt_int(data.get("standalone")),
            reserved=_opt_int(data.get("reserved")),
            total=_opt_int(data.get("total")),
            occupied_quantity=_opt_int(data.get("occupiedQuantity")),
            product_channel_quantity=_opt_int(data.get("productChannelQuantity")),
            product_channel_occupied_quantity=_opt_int(
                data.get("productChannelOccupiedQuantity")
            ),
            activity_channel_quantity=_opt_int(data.get("activityChannelQuantity")),
            activity_channel_occupied_quantity=_opt_int(
                data.get("activityChannelOccupiedQuantity")
            ),
        )


@dataclass
class SkuStockOperationStatus:
    success: Optional[bool] = None
    message: Optional[str] = None
    code: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "SkuStockOperationStatus":
        return cls(
            success=_opt_bool(data.get("success")),
            message=_opt_str(data.get("message")) or _opt_str(data.get("msg")),
            code=_opt_int(data.get("code")),
        )


@dataclass
class SkuStockWithWarehouseCode:
    sku_id: Optional[str]
    whcode: Optional[str]
    sku_stock: Optional[SkuStock]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "SkuStockWithWarehouseCode":
        stock = data.get("skuStock")
        return cls(
            sku_id=_opt_str(data.get("skuId")),
            whcode=_opt_str(data.get("whcode")),
            sku_stock=SkuStock.from_dict(_as_mapping(stock))
            if isinstance(stock, Mapping)
            else None,
        )


@dataclass
class SkuStockResponseData:
    sku_id: Optional[str]
    sku_stock: Optional[SkuStock]
    sku_stock_info_with_whcode: List[SkuStockWithWarehouseCode]
    api_version: Optional[str]
    response: Optional[SkuStockOperationStatus]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "SkuStockResponseData":
        stock_info = data.get("skuStock")
        response = data.get("response")
        wh_list_raw = data.get("skuStockInfoWithWhcode")
        wh_list: List[SkuStockWithWarehouseCode] = []
        for entry in _as_sequence(wh_list_raw):
            if isinstance(entry, Mapping):
                wh_list.append(SkuStockWithWarehouseCode.from_dict(entry))
        sku_stock = (
            SkuStock.from_dict(_as_mapping(stock_info))
            if isinstance(stock_info, Mapping)
            else None
        )
        status = (
            SkuStockOperationStatus.from_dict(response)
            if isinstance(response, Mapping)
            else None
        )
        return cls(
            sku_id=_opt_str(data.get("skuId")),
            sku_stock=sku_stock,
            sku_stock_info_with_whcode=wh_list,
            api_version=_opt_str(data.get("apiVersion")),
            response=status,
        )


@dataclass
class SkuStockInfo:
    sku_id: Optional[str]
    sku_stock_info: Optional[SkuStock]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "SkuStockInfo":
        stock = data.get("skuStockInfo")
        return cls(
            sku_id=_opt_str(data.get("skuId")),
            sku_stock_info=SkuStock.from_dict(_as_mapping(stock))
            if isinstance(stock, Mapping)
            else None,
        )


@dataclass
class SkuStockInfoWithWhcode:
    sku_id: Optional[str]
    whcode: Optional[str]
    sku_stock_info: Optional[SkuStock]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "SkuStockInfoWithWhcode":
        stock = data.get("skuStockInfo")
        return cls(
            sku_id=_opt_str(data.get("skuId")),
            whcode=_opt_str(data.get("whcode")),
            sku_stock_info=SkuStock.from_dict(_as_mapping(stock))
            if isinstance(stock, Mapping)
            else None,
        )


@dataclass
class GetSkuStockV2ResponseData:
    response: Optional[SkuStockOperationStatus]
    api_version: Optional[str]
    sku_stock_info: Optional[SkuStockInfo]
    sku_stock_info_with_whcode: List[SkuStockInfoWithWhcode]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetSkuStockV2ResponseData":
        response = data.get("response")
        info = data.get("skuStockInfo")
        info_with_wh_code = data.get("skuStockInfoWithWhcode")
        wh_items: List[SkuStockInfoWithWhcode] = []
        for entry in _as_sequence(info_with_wh_code):
            if isinstance(entry, Mapping):
                wh_items.append(SkuStockInfoWithWhcode.from_dict(entry))
        return cls(
            response=SkuStockOperationStatus.from_dict(response)
            if isinstance(response, Mapping)
            else None,
            api_version=_opt_str(data.get("apiVersion")),
            sku_stock_info=SkuStockInfo.from_dict(info)
            if isinstance(info, Mapping)
            else None,
            sku_stock_info_with_whcode=wh_items,
        )


@dataclass
class SyncSkuStockV2ResponseData:
    response: Optional[SkuStockOperationStatus]
    api_version: Optional[str]
    sku_stock_info: Optional[SkuStockInfo]
    data: Dict[str, SkuStockInfoWithWhcode]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "SyncSkuStockV2ResponseData":
        response = data.get("response")
        info = data.get("skuStockInfo")
        entries = data.get("data")
        parsed_entries: Dict[str, SkuStockInfoWithWhcode] = {}
        if isinstance(entries, Mapping):
            for key, value in entries.items():
                if isinstance(value, Mapping):
                    parsed_entries[str(key)] = SkuStockInfoWithWhcode.from_dict(value)
        return cls(
            response=SkuStockOperationStatus.from_dict(response)
            if isinstance(response, Mapping)
            else None,
            api_version=_opt_str(data.get("apiVersion")),
            sku_stock_info=SkuStockInfo.from_dict(info)
            if isinstance(info, Mapping)
            else None,
            data=parsed_entries,
        )


@dataclass
class WarehouseCoverage:
    province: Optional[str]
    province_code: Optional[str]
    city: Optional[str]
    city_code: Optional[str]
    area: Optional[str]
    area_code: Optional[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "WarehouseCoverage":
        return cls(
            province=_opt_str(data.get("province")),
            province_code=_opt_str(data.get("provinceCode")),
            city=_opt_str(data.get("city")),
            city_code=_opt_str(data.get("cityCode")),
            area=_opt_str(data.get("area")),
            area_code=_opt_str(data.get("areaCode")),
        )


@dataclass
class Warehouse:
    code: Optional[str]
    name: Optional[str]
    province: Optional[str]
    province_code: Optional[str]
    city: Optional[str]
    city_code: Optional[str]
    area: Optional[str]
    area_code: Optional[str]
    town: Optional[str]
    town_code: Optional[str]
    address: Optional[str]
    contact_name: Optional[str]
    contact_tel: Optional[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "Warehouse":
        return cls(
            code=_opt_str(data.get("code")),
            name=_opt_str(data.get("name")),
            province=_opt_str(data.get("province")),
            province_code=_opt_str(data.get("provinceCode")),
            city=_opt_str(data.get("city")),
            city_code=_opt_str(data.get("cityCode")),
            area=_opt_str(data.get("area")),
            area_code=_opt_str(data.get("areaCode")),
            town=_opt_str(data.get("town")),
            town_code=_opt_str(data.get("townCode")),
            address=_opt_str(data.get("address")),
            contact_name=_opt_str(data.get("contactName")),
            contact_tel=_opt_str(data.get("contactTel")),
        )


@dataclass
class ListWarehouseResponseData:
    total: Optional[int]
    warehouse_list: List[Warehouse]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "ListWarehouseResponseData":
        warehouses_raw = data.get("warehouseList")
        warehouses: List[Warehouse] = []
        for entry in _as_sequence(warehouses_raw):
            if isinstance(entry, Mapping):
                warehouses.append(Warehouse.from_dict(entry))
        return cls(total=_opt_int(data.get("total")), warehouse_list=warehouses)


@dataclass
class GetWarehouseResponseData:
    code: Optional[str]
    name: Optional[str]
    province: Optional[str]
    province_code: Optional[str]
    city: Optional[str]
    city_code: Optional[str]
    area: Optional[str]
    area_code: Optional[str]
    town: Optional[str]
    town_code: Optional[str]
    address: Optional[str]
    contact_name: Optional[str]
    contact_tel: Optional[str]
    coverage_list: List[WarehouseCoverage]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetWarehouseResponseData":
        coverage_raw = data.get("coverageList")
        coverage: List[WarehouseCoverage] = []
        for entry in _as_sequence(coverage_raw):
            if isinstance(entry, Mapping):
                coverage.append(WarehouseCoverage.from_dict(entry))
        return cls(
            code=_opt_str(data.get("code")),
            name=_opt_str(data.get("name")),
            province=_opt_str(data.get("province")),
            province_code=_opt_str(data.get("provinceCode")),
            city=_opt_str(data.get("city")),
            city_code=_opt_str(data.get("cityCode")),
            area=_opt_str(data.get("area")),
            area_code=_opt_str(data.get("areaCode")),
            town=_opt_str(data.get("town")),
            town_code=_opt_str(data.get("townCode")),
            address=_opt_str(data.get("address")),
            contact_name=_opt_str(data.get("contactName")),
            contact_tel=_opt_str(data.get("contactTel")),
            coverage_list=coverage,
        )


__all__ = [
    "GetItemStockRequest",
    "SyncItemStockRequest",
    "IncItemStockRequest",
    "GetSkuStockRequest",
    "SyncSkuStockRequest",
    "IncSkuStockRequest",
    "GetSkuStockV2Request",
    "SyncSkuStockV2Request",
    "GetWarehouseRequest",
    "CreateWarehouseRequest",
    "UpdateWarehouseRequest",
    "ListWarehouseRequest",
    "SetWarehouseCoverageRequest",
    "SetWarehousePriorityRequest",
    "ItemStock",
    "ItemStockResponseData",
    "SkuStock",
    "SkuStockOperationStatus",
    "SkuStockWithWarehouseCode",
    "SkuStockResponseData",
    "SkuStockInfo",
    "SkuStockInfoWithWhcode",
    "GetSkuStockV2ResponseData",
    "SyncSkuStockV2ResponseData",
    "WarehouseCoverage",
    "Warehouse",
    "ListWarehouseResponseData",
    "GetWarehouseResponseData",
]
