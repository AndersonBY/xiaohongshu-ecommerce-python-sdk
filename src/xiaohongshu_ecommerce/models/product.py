"""Product domain request and response models."""

from __future__ import annotations

from collections.abc import Mapping as MappingABC, Sequence as SequenceABC
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Sequence, Union

from .base import BaseRequest

if TYPE_CHECKING:  # pragma: no cover
    from .boutique import BoutiqueMode


def _filter_none(mapping: Mapping[str, object]) -> Dict[str, object]:
    """Remove ``None`` values from a mapping."""

    return {key: value for key, value in mapping.items() if value is not None}


def _enum_value(value: object) -> object:
    """Return the raw value for enum members."""

    if isinstance(value, Enum):
        return value.value  # type: ignore[attr-defined]
    return value


class GetBasicItemListRequest(BaseRequest):
    """Request wrapper for ``product.getBasicItemList``."""

    def __init__(
        self,
        *,
        item_id: Optional[str] = None,
        status: Optional[int] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        last_id: Optional[str] = None,
    ) -> None:
        super().__init__(method="product.getBasicItemList")
        self.item_id = item_id
        self.status = status
        self.page_no = page_no
        self.page_size = page_size
        self.last_id = last_id

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {}
        if self.item_id is not None:
            payload["id"] = self.item_id
        if self.status is not None:
            payload["status"] = self.status
        if self.page_no is not None:
            payload["pageNo"] = self.page_no
        if self.page_size is not None:
            payload["pageSize"] = self.page_size
        if self.last_id is not None:
            payload["lastId"] = self.last_id
        return payload


class GetDetailItemListRequest(BaseRequest):
    """Request wrapper for ``product.getDetailItemList``."""

    def __init__(
        self,
        *,
        item_ids: Optional[Sequence[str]] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> None:
        super().__init__(method="product.getDetailItemList")
        self.item_ids = list(item_ids or [])
        self.page_no = page_no
        self.page_size = page_size

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {}
        if self.item_ids:
            payload["itemIds"] = self.item_ids
        if self.page_no is not None:
            payload["pageNo"] = self.page_no
        if self.page_size is not None:
            payload["pageSize"] = self.page_size
        return payload


class GetSpuInfoRequest(BaseRequest):
    """Request wrapper for ``product.getSpuInfo``."""

    def __init__(self, spu_id: str) -> None:
        super().__init__(method="product.getSpuInfo")
        self.spu_id = spu_id

    def extra_payload(self) -> Dict[str, object]:
        return {"spuId": self.spu_id}


class UpdateLogisticsPlanRequest(BaseRequest):
    """Request wrapper for ``product.updateLogisticsPlan``."""

    def __init__(self, item_id: str, *, logistics_plan_id: str) -> None:
        super().__init__(method="product.updateLogisticsPlan")
        self.item_id = item_id
        self.logistics_plan_id = logistics_plan_id

    def extra_payload(self) -> Dict[str, object]:
        return {
            "itemId": self.item_id,
            "logisticsPlanId": self.logistics_plan_id,
        }


class UpdateAvailabilityRequest(BaseRequest):
    """Request wrapper for ``product.updateAvailability``."""

    def __init__(self, item_id: str, *, available: bool) -> None:
        super().__init__(method="product.updateAvailability")
        self.item_id = item_id
        self.available = available

    def extra_payload(self) -> Dict[str, object]:
        return {"itemId": self.item_id, "available": self.available}


class CreateSpuRequest(BaseRequest):
    """Request wrapper for ``product.createSpu``."""

    def __init__(self, *, spu: Mapping[str, object]) -> None:
        super().__init__(method="product.createSpu")
        self.spu = dict(spu)

    def extra_payload(self) -> Dict[str, object]:
        return {"spu": self.spu}


class UpdateSpuRequest(BaseRequest):
    """Request wrapper for ``product.updateSpu``."""

    def __init__(self, *, spu_id: str, updates: Mapping[str, object]) -> None:
        super().__init__(method="product.updateSpu")
        self.spu_id = spu_id
        self.updates = dict(updates)

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {"spuId": self.spu_id}
        payload.update(self.updates)
        return payload


class DeleteSpuRequest(BaseRequest):
    """Request wrapper for ``product.deleteSpu``."""

    def __init__(self, *, spu_ids: Sequence[str]) -> None:
        super().__init__(method="product.deleteSpu")
        self.spu_ids = list(spu_ids)

    def extra_payload(self) -> Dict[str, object]:
        return {"spuIds": self.spu_ids}


class CreateItemRequest(BaseRequest):
    """Request wrapper for ``product.createItem``."""

    def __init__(
        self,
        *,
        spu_id: str,
        price: Optional[float] = None,
        original_price: Optional[float] = None,
        stock: Optional[int] = None,
        logistics_plan_id: Optional[str] = None,
        variants: Optional[Sequence[Mapping[str, object]]] = None,
        delivery_time: Optional[Mapping[str, object]] = None,
        extra: Optional[Mapping[str, object]] = None,
    ) -> None:
        super().__init__(method="product.createItem")
        self.spu_id = spu_id
        self.price = price
        self.original_price = original_price
        self.stock = stock
        self.logistics_plan_id = logistics_plan_id
        self.variants = list(variants or [])
        self.delivery_time = dict(delivery_time) if delivery_time else None
        self.extra = dict(extra) if extra else {}

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {"spuId": self.spu_id}
        if self.price is not None:
            payload["price"] = self.price
        if self.original_price is not None:
            payload["originalPrice"] = self.original_price
        if self.stock is not None:
            payload["stock"] = self.stock
        if self.logistics_plan_id is not None:
            payload["logisticsPlanId"] = self.logistics_plan_id
        if self.variants:
            payload["variants"] = [_as_mapping(item) for item in self.variants]
        if self.delivery_time is not None:
            payload["deliveryTime"] = self.delivery_time
        payload.update(self.extra)
        return payload


class UpdateItemRequest(BaseRequest):
    """Request wrapper for ``product.updateItem``."""

    def __init__(
        self,
        item_id: str,
        *,
        name: Optional[str] = None,
        ename: Optional[str] = None,
        brand_id: Optional[int] = None,
        category_id: Optional[str] = None,
        attributes: Optional[Sequence[Mapping[str, object]]] = None,
        images: Optional[Sequence[str]] = None,
        image_descriptions: Optional[Sequence[str]] = None,
        shipping_template_id: Optional[str] = None,
        extra: Optional[Mapping[str, object]] = None,
        spu_id: Optional[str] = None,
        updates: Optional[Mapping[str, object]] = None,
    ) -> None:
        super().__init__(method="product.updateItem")
        self.item_id = item_id
        self.name = name
        self.ename = ename
        self.brand_id = brand_id
        self.category_id = category_id
        self.attributes = list(attributes or [])
        self.images = list(images or [])
        self.image_descriptions = list(image_descriptions or [])
        self.shipping_template_id = shipping_template_id
        self.extra = dict(extra or {})
        self.spu_id = spu_id
        self.updates = dict(updates or {})

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {"id": self.item_id}
        if self.spu_id is not None:
            payload["spuId"] = self.spu_id
        if self.name is not None:
            payload["name"] = self.name
        if self.ename is not None:
            payload["ename"] = self.ename
        if self.brand_id is not None:
            payload["brandId"] = self.brand_id
        if self.category_id is not None:
            payload["categoryId"] = self.category_id
        if self.attributes:
            payload["attributes"] = [_as_mapping(attr) for attr in self.attributes]
        if self.images:
            payload["images"] = list(self.images)
        if self.image_descriptions:
            payload["imageDescriptions"] = list(self.image_descriptions)
        if self.shipping_template_id is not None:
            payload["shippingTemplateId"] = self.shipping_template_id
        payload.update(self.extra)
        payload.update(self.updates)
        return payload


class DeleteItemRequest(BaseRequest):
    """Request wrapper for ``product.deleteItem``."""

    def __init__(self, *, item_id: str, spu_id: Optional[str] = None) -> None:
        super().__init__(method="product.deleteItem")
        self.item_id = item_id
        self.spu_id = spu_id

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {"id": self.item_id}
        if self.spu_id is not None:
            payload["spuId"] = self.spu_id
        return payload


class GetBasicSpuRequest(BaseRequest):
    """Request wrapper for ``product.getBasicSpu``."""

    def __init__(
        self,
        *,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        spu_ids: Optional[Sequence[str]] = None,
        extra: Optional[Mapping[str, object]] = None,
    ) -> None:
        super().__init__(method="product.getBasicSpu")
        self.page_no = page_no
        self.page_size = page_size
        self.spu_ids = list(spu_ids or [])
        self.extra = dict(extra or {})

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {}
        if self.page_no is not None:
            payload["pageNo"] = self.page_no
        if self.page_size is not None:
            payload["pageSize"] = self.page_size
        if self.spu_ids:
            payload["spuIds"] = self.spu_ids
        payload.update(self.extra)
        return payload


class UpdateItemPriceRequest(BaseRequest):
    """Request wrapper for ``product.updateItemPrice``."""

    def __init__(
        self,
        *,
        item_id: Optional[str] = None,
        sku_id: Optional[str] = None,
        price: Optional[Sequence[Mapping[str, object]]] = None,
        original_price: Optional[float] = None,
        extra: Optional[Mapping[str, object]] = None,
    ) -> None:
        super().__init__(method="product.updateItemPrice")
        self.item_id = item_id
        self.sku_id = sku_id
        self.price = [dict(p) for p in price or []]
        self.original_price = original_price
        self.extra = dict(extra or {})

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {}
        if self.item_id is not None:
            payload["itemId"] = self.item_id
        if self.sku_id is not None:
            payload["skuId"] = self.sku_id
        if self.price:
            payload["price"] = [dict(entry) for entry in self.price]
        if self.original_price is not None:
            payload["originalPrice"] = self.original_price
        payload.update(self.extra)
        return payload


class GetDetailSkuListRequest(BaseRequest):
    """Request wrapper for ``product.getDetailSkuList``."""

    def __init__(self, **filters: object) -> None:
        super().__init__(method="product.getDetailSkuList")
        self.filters = {
            key: value for key, value in filters.items() if value is not None
        }

    def extra_payload(self) -> Dict[str, object]:
        # Map Python snake_case parameter names to API camelCase field names
        field_mapping = {
            "page_no": "pageNo",
            "page_size": "pageSize",
            "create_time_from": "createTimeFrom",
            "create_time_to": "createTimeTo",
            "update_time_from": "updateTimeFrom",
            "update_time_to": "updateTimeTo",
            "stock_gte": "stockGte",
            "stock_lte": "stockLte",
            "sc_sku_code": "scSkuCode",
            "single_pack_only": "singlePackOnly",
            "last_id": "lastId",
            "is_channel": "isChannel",
        }

        payload = {}
        for key, value in self.filters.items():
            api_key = field_mapping.get(
                key, key
            )  # Use mapping if exists, otherwise use original key
            payload[api_key] = value
        return payload


class GetItemInfoRequest(BaseRequest):
    """Request wrapper for ``product.getItemInfo``."""

    def __init__(
        self,
        *,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        item_id: Optional[str] = None,
    ) -> None:
        super().__init__(method="product.getItemInfo")
        self.page_no = page_no
        self.page_size = page_size
        self.item_id = item_id

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {}
        if self.page_no is not None:
            payload["pageNo"] = self.page_no
        if self.page_size is not None:
            payload["pageSize"] = self.page_size
        if self.item_id is not None:
            payload["itemId"] = self.item_id
        return payload


class SearchItemListRequest(BaseRequest):
    """Request wrapper for ``product.searchItemList``."""

    def __init__(
        self,
        *,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        search_param: Optional[Mapping[str, object]] = None,
    ) -> None:
        super().__init__(method="product.searchItemList")
        self.page_no = page_no
        self.page_size = page_size
        self.search_param = dict(search_param or {})

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {}
        if self.page_no is not None:
            payload["pageNo"] = self.page_no
        if self.page_size is not None:
            payload["pageSize"] = self.page_size
        if self.search_param:
            payload["searchParam"] = self.search_param
        return payload


class UpdateSkuLogisticsPlanRequest(BaseRequest):
    """Request wrapper for ``product.updateSkuLogisticsPlan``."""

    def __init__(self, *, sku_id: str, logistics_plan_id: str) -> None:
        super().__init__(method="product.updateSkuLogisticsPlan")
        self.sku_id = sku_id
        self.logistics_plan_id = logistics_plan_id

    def extra_payload(self) -> Dict[str, object]:
        return {"skuId": self.sku_id, "logisticsPlanId": self.logistics_plan_id}


class UpdateSkuPriceRequest(BaseRequest):
    """Request wrapper for ``product.updateSkuPrice``."""

    def __init__(
        self,
        sku_id: str,
        *,
        price: Sequence[Mapping[str, object]],
        original_price: Optional[float] = None,
        extra: Optional[Mapping[str, object]] = None,
    ) -> None:
        super().__init__(method="product.updateSkuPrice")
        self.sku_id = sku_id
        self.price = [dict(entry) for entry in price]
        self.original_price = original_price
        self.extra = dict(extra or {})

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "skuId": self.sku_id,
            "price": [dict(entry) for entry in self.price],
        }
        if self.original_price is not None:
            payload["originalPrice"] = self.original_price
        payload.update(self.extra)
        return payload


class UpdateSkuAvailableRequest(BaseRequest):
    """Request wrapper for ``product.updateSkuAvailable``."""

    def __init__(self, *, sku_id: str, available: bool) -> None:
        super().__init__(method="product.updateSkuAvailable")
        self.sku_id = sku_id
        self.available = available

    def extra_payload(self) -> Dict[str, object]:
        return {"skuId": self.sku_id, "available": self.available}


class UpdateItemImageRequest(BaseRequest):
    """Request wrapper for ``product.updateItemImage``."""

    def __init__(
        self, *, item_id: str, material_type: int, material_urls: Sequence[str]
    ) -> None:
        super().__init__(method="product.updateItemImage")
        self.item_id = item_id
        self.material_type = material_type
        self.material_urls = list(material_urls)

    def extra_payload(self) -> Dict[str, object]:
        return {
            "itemId": self.item_id,
            "materialType": self.material_type,
            "materialUrls": self.material_urls,
        }


class UpdateSpuImageRequest(BaseRequest):
    """Request wrapper for ``product.updateSpuImage``."""

    def __init__(
        self,
        *,
        spu_id: str,
        material_type: Optional[int] = None,
        material_urls: Optional[Sequence[str]] = None,
        image_urls: Optional[Sequence[str]] = None,
        extra: Optional[Mapping[str, object]] = None,
    ) -> None:
        super().__init__(method="product.updateSpuImage")
        self.spu_id = spu_id
        # Default material_type to 1 (images) if not provided
        self.material_type = material_type if material_type is not None else 1
        # Use image_urls if material_urls not provided
        urls = material_urls or image_urls or []
        self.material_urls = list(urls)
        self.extra = dict(extra or {})

    def extra_payload(self) -> Dict[str, object]:
        payload = {
            "spuId": self.spu_id,
            "materialType": self.material_type,
            "materialUrls": self.material_urls,
        }
        payload.update(self.extra)
        return payload


class UpdateVariantImageRequest(BaseRequest):
    """Request wrapper for ``product.updateVariantImage``."""

    def __init__(
        self,
        *,
        variant_id: str,
        spu_id: Optional[str] = None,
        variant_value: Optional[str] = None,
        material_url: Optional[str] = None,
        image_url: Optional[str] = None,
        variant_type: Optional[str] = None,
        extra: Optional[Mapping[str, object]] = None,
    ) -> None:
        super().__init__(method="product.updateVariantImage")
        self.variant_id = variant_id
        self.spu_id = spu_id
        self.variant_value = variant_value or variant_type
        self.material_url = material_url or image_url
        self.extra = dict(extra or {})

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {"variantId": self.variant_id}
        if self.spu_id is not None:
            payload["spuId"] = self.spu_id
        if self.variant_value is not None:
            payload["variantValue"] = self.variant_value
        if self.material_url is not None:
            payload["materialUrl"] = self.material_url
        payload.update(self.extra)
        return payload


def _item_v3_payload(
    *,
    name: Optional[str],
    ename: Optional[str],
    brand_id: Optional[int],
    category_id: Optional[str],
    attributes: Sequence["ItemAttributeV3"],
    shipping_template_id: Optional[str],
    shipping_gross_weight: Optional[int],
    variant_ids: Sequence[str],
    images: Sequence[str],
    standard_images: Sequence[str],
    long_images: Sequence[str],
    video_url: Optional[str],
    article_no: Optional[str],
    image_descriptions: Sequence[str],
    transparent_image: Optional[str],
    description: Optional[str],
    faq: Sequence["ItemFaq"],
    is_channel: Optional[bool],
    delivery_mode: Optional[int],
    free_return: Optional[int],
    enable_multi_warehouse: Optional[bool],
    size_table_image: Optional[str],
    recommend_size_table_image: Optional[str],
    model_try_on_size_table_image: Optional[str],
    enable_main_spec_image: Optional[bool],
    item_short_title: Optional[str],
) -> Dict[str, object]:
    payload = _filter_none(
        {
            "name": name,
            "ename": ename,
            "brandId": brand_id,
            "categoryId": category_id,
            "shippingTemplateId": shipping_template_id,
            "shippingGrossWeight": shipping_gross_weight,
            "videoUrl": video_url,
            "articleNo": article_no,
            "transparentImage": transparent_image,
            "description": description,
            "isChannel": is_channel,
            "deliveryMode": delivery_mode,
            "freeReturn": free_return,
            "enableMultiWarehouse": enable_multi_warehouse,
            "sizeTableImage": size_table_image,
            "recommendSizeTableImage": recommend_size_table_image,
            "modelTryOnSizeTableImage": model_try_on_size_table_image,
            "enableMainSpecImage": enable_main_spec_image,
            "itemShortTitle": item_short_title,
        }
    )
    if attributes:
        payload["attributes"] = [attribute.to_payload() for attribute in attributes]
    if variant_ids:
        payload["variantIds"] = list(variant_ids)
    if images:
        payload["images"] = list(images)
    if standard_images:
        payload["standardImages"] = list(standard_images)
    if long_images:
        payload["longImages"] = list(long_images)
    if image_descriptions:
        payload["imageDescriptions"] = list(image_descriptions)
    if faq:
        payload["faq"] = [entry.to_payload() for entry in faq]
    return payload


def _item_and_sku_payload(
    *,
    name: Optional[str],
    ename: Optional[str],
    brand_id: Optional[int],
    category_id: Optional[str],
    attributes: Sequence["ItemAttributeV3"],
    shipping_template_id: Optional[str],
    shipping_gross_weight: Optional[int],
    variant_ids: Sequence[str],
    images: Sequence["MaterialResource"],
    standard_images: Sequence["MaterialResource"],
    long_images: Sequence["MaterialResource"],
    videos: Sequence["MaterialResource"],
    article_no: Optional[str],
    image_descriptions: Sequence["MaterialResource"],
    transparent_image: Optional[str],
    description: Optional[str],
    delivery_mode: Optional[int],
    free_return: Optional[int],
    enable_multi_warehouse: Optional[bool],
    size_table_image: Sequence["MaterialResource"],
    recommend_size_table_image: Sequence["MaterialResource"],
    model_try_on_size_table_image: Sequence["MaterialResource"],
    enable_main_spec_image: Optional[int],
    create_sku_list: Sequence["SkuV3"],
    enable_step_presale: Optional[bool],
    item_short_title: Optional[str],
) -> Dict[str, object]:
    payload = _filter_none(
        {
            "name": name,
            "ename": ename,
            "brandId": brand_id,
            "categoryId": category_id,
            "shippingTemplateId": shipping_template_id,
            "shippingGrossWeight": shipping_gross_weight,
            "articleNo": article_no,
            "transparentImage": transparent_image,
            "description": description,
            "deliveryMode": delivery_mode,
            "freeReturn": free_return,
            "enableMultiWarehouse": enable_multi_warehouse,
            "enableMainSpecImage": enable_main_spec_image,
            "enableStepPresale": enable_step_presale,
            "itemShortTitle": item_short_title,
        }
    )
    if attributes:
        payload["attributes"] = [attribute.to_payload() for attribute in attributes]
    if variant_ids:
        payload["variantIds"] = list(variant_ids)
    if images:
        payload["images"] = [material.to_payload() for material in images]
    if standard_images:
        payload["standardImages"] = [
            material.to_payload() for material in standard_images
        ]
    if long_images:
        payload["longImages"] = [material.to_payload() for material in long_images]
    if videos:
        payload["videos"] = [material.to_payload() for material in videos]
    if image_descriptions:
        payload["imageDescriptions"] = [
            material.to_payload() for material in image_descriptions
        ]
    if size_table_image:
        payload["sizeTableImage"] = [
            material.to_payload() for material in size_table_image
        ]
    if recommend_size_table_image:
        payload["recommendSizeTableImage"] = [
            material.to_payload() for material in recommend_size_table_image
        ]
    if model_try_on_size_table_image:
        payload["modelTryOnSizeTableImage"] = [
            material.to_payload() for material in model_try_on_size_table_image
        ]
    if create_sku_list:
        payload["createSkuList"] = [sku.to_payload() for sku in create_sku_list]
    return payload


class CreateItemV3Request(BaseRequest):
    """Request wrapper for ``product.createItemV2``."""

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        ename: Optional[str] = None,
        brand_id: Optional[int] = None,
        category_id: Optional[str] = None,
        attributes: Optional[
            Sequence[Union["ItemAttributeV3", Mapping[str, object]]]
        ] = None,
        shipping_template_id: Optional[str] = None,
        shipping_gross_weight: Optional[int] = None,
        variant_ids: Optional[Sequence[str]] = None,
        images: Optional[Sequence[str]] = None,
        standard_images: Optional[Sequence[str]] = None,
        long_images: Optional[Sequence[str]] = None,
        video_url: Optional[str] = None,
        article_no: Optional[str] = None,
        image_descriptions: Optional[Sequence[str]] = None,
        transparent_image: Optional[str] = None,
        description: Optional[str] = None,
        faq: Optional[Sequence[Union["ItemFaq", Mapping[str, object]]]] = None,
        is_channel: Optional[bool] = None,
        delivery_mode: Optional[int] = None,
        free_return: Optional[int] = None,
        enable_multi_warehouse: Optional[bool] = None,
        size_table_image: Optional[str] = None,
        recommend_size_table_image: Optional[str] = None,
        model_try_on_size_table_image: Optional[str] = None,
        enable_main_spec_image: Optional[bool] = None,
        item_short_title: Optional[str] = None,
    ) -> None:
        super().__init__(method="product.createItemV2")
        self.name = name
        self.ename = ename
        self.brand_id = brand_id
        self.category_id = category_id
        self.attributes = [_ensure_attribute_v3(attr) for attr in attributes or []]
        self.shipping_template_id = shipping_template_id
        self.shipping_gross_weight = shipping_gross_weight
        self.variant_ids = list(variant_ids or [])
        self.images = list(images or [])
        self.standard_images = list(standard_images or [])
        self.long_images = list(long_images or [])
        self.video_url = video_url
        self.article_no = article_no
        self.image_descriptions = list(image_descriptions or [])
        self.transparent_image = transparent_image
        self.description = description
        self.faq = [_ensure_faq(entry) for entry in faq or []]
        self.is_channel = is_channel
        self.delivery_mode = delivery_mode
        self.free_return = free_return
        self.enable_multi_warehouse = enable_multi_warehouse
        self.size_table_image = size_table_image
        self.recommend_size_table_image = recommend_size_table_image
        self.model_try_on_size_table_image = model_try_on_size_table_image
        self.enable_main_spec_image = enable_main_spec_image
        self.item_short_title = item_short_title

    def extra_payload(self) -> Dict[str, object]:
        return _item_v3_payload(
            name=self.name,
            ename=self.ename,
            brand_id=self.brand_id,
            category_id=self.category_id,
            attributes=self.attributes,
            shipping_template_id=self.shipping_template_id,
            shipping_gross_weight=self.shipping_gross_weight,
            variant_ids=self.variant_ids,
            images=self.images,
            standard_images=self.standard_images,
            long_images=self.long_images,
            video_url=self.video_url,
            article_no=self.article_no,
            image_descriptions=self.image_descriptions,
            transparent_image=self.transparent_image,
            description=self.description,
            faq=self.faq,
            is_channel=self.is_channel,
            delivery_mode=self.delivery_mode,
            free_return=self.free_return,
            enable_multi_warehouse=self.enable_multi_warehouse,
            size_table_image=self.size_table_image,
            recommend_size_table_image=self.recommend_size_table_image,
            model_try_on_size_table_image=self.model_try_on_size_table_image,
            enable_main_spec_image=self.enable_main_spec_image,
            item_short_title=self.item_short_title,
        )


class UpdateItemV3Request(BaseRequest):
    """Request wrapper for ``product.updateItemV2``."""

    def __init__(
        self,
        item_id: str,
        *,
        updated_fields: Optional[Sequence[str]] = None,
        name: Optional[str] = None,
        ename: Optional[str] = None,
        brand_id: Optional[int] = None,
        category_id: Optional[str] = None,
        attributes: Optional[
            Sequence[Union["ItemAttributeV3", Mapping[str, object]]]
        ] = None,
        shipping_template_id: Optional[str] = None,
        shipping_gross_weight: Optional[int] = None,
        variant_ids: Optional[Sequence[str]] = None,
        images: Optional[Sequence[str]] = None,
        standard_images: Optional[Sequence[str]] = None,
        long_images: Optional[Sequence[str]] = None,
        video_url: Optional[str] = None,
        article_no: Optional[str] = None,
        image_descriptions: Optional[Sequence[str]] = None,
        transparent_image: Optional[str] = None,
        description: Optional[str] = None,
        faq: Optional[Sequence[Union["ItemFaq", Mapping[str, object]]]] = None,
        is_channel: Optional[bool] = None,
        delivery_mode: Optional[int] = None,
        free_return: Optional[int] = None,
        enable_multi_warehouse: Optional[bool] = None,
        size_table_image: Optional[str] = None,
        recommend_size_table_image: Optional[str] = None,
        model_try_on_size_table_image: Optional[str] = None,
        enable_main_spec_image: Optional[bool] = None,
        item_short_title: Optional[str] = None,
    ) -> None:
        super().__init__(method="product.updateItemV2")
        self.item_id = item_id
        self.updated_fields = list(updated_fields or [])
        self.name = name
        self.ename = ename
        self.brand_id = brand_id
        self.category_id = category_id
        self.attributes = [_ensure_attribute_v3(attr) for attr in attributes or []]
        self.shipping_template_id = shipping_template_id
        self.shipping_gross_weight = shipping_gross_weight
        self.variant_ids = list(variant_ids or [])
        self.images = list(images or [])
        self.standard_images = list(standard_images or [])
        self.long_images = list(long_images or [])
        self.video_url = video_url
        self.article_no = article_no
        self.image_descriptions = list(image_descriptions or [])
        self.transparent_image = transparent_image
        self.description = description
        self.faq = [_ensure_faq(entry) for entry in faq or []]
        self.is_channel = is_channel
        self.delivery_mode = delivery_mode
        self.free_return = free_return
        self.enable_multi_warehouse = enable_multi_warehouse
        self.size_table_image = size_table_image
        self.recommend_size_table_image = recommend_size_table_image
        self.model_try_on_size_table_image = model_try_on_size_table_image
        self.enable_main_spec_image = enable_main_spec_image
        self.item_short_title = item_short_title

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "id": self.item_id,
        }
        if self.updated_fields:
            payload["updatedFields"] = list(self.updated_fields)
        payload.update(
            _item_v3_payload(
                name=self.name,
                ename=self.ename,
                brand_id=self.brand_id,
                category_id=self.category_id,
                attributes=self.attributes,
                shipping_template_id=self.shipping_template_id,
                shipping_gross_weight=self.shipping_gross_weight,
                variant_ids=self.variant_ids,
                images=self.images,
                standard_images=self.standard_images,
                long_images=self.long_images,
                video_url=self.video_url,
                article_no=self.article_no,
                image_descriptions=self.image_descriptions,
                transparent_image=self.transparent_image,
                description=self.description,
                faq=self.faq,
                is_channel=self.is_channel,
                delivery_mode=self.delivery_mode,
                free_return=self.free_return,
                enable_multi_warehouse=self.enable_multi_warehouse,
                size_table_image=self.size_table_image,
                recommend_size_table_image=self.recommend_size_table_image,
                model_try_on_size_table_image=self.model_try_on_size_table_image,
                enable_main_spec_image=self.enable_main_spec_image,
                item_short_title=self.item_short_title,
            )
        )
        return _filter_none(payload)


class CreateItemAndSkuRequest(BaseRequest):
    """Request wrapper for ``product.createItemAndSku``."""

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        ename: Optional[str] = None,
        brand_id: Optional[int] = None,
        category_id: Optional[str] = None,
        attributes: Optional[
            Sequence[Union["ItemAttributeV3", Mapping[str, object]]]
        ] = None,
        shipping_template_id: Optional[str] = None,
        shipping_gross_weight: Optional[int] = None,
        variant_ids: Optional[Sequence[str]] = None,
        images: Optional[
            Sequence[Union["MaterialResource", Mapping[str, object], str]]
        ] = None,
        standard_images: Optional[
            Sequence[Union["MaterialResource", Mapping[str, object], str]]
        ] = None,
        long_images: Optional[
            Sequence[Union["MaterialResource", Mapping[str, object], str]]
        ] = None,
        videos: Optional[
            Sequence[Union["MaterialResource", Mapping[str, object], str]]
        ] = None,
        video_url: Optional[str] = None,
        article_no: Optional[str] = None,
        image_descriptions: Optional[
            Sequence[Union["MaterialResource", Mapping[str, object], str]]
        ] = None,
        transparent_image: Optional[str] = None,
        description: Optional[str] = None,
        faq: Optional[Sequence[Union["ItemFaq", Mapping[str, object]]]] = None,
        delivery_mode: Optional[int] = None,
        free_return: Optional[int] = None,
        enable_multi_warehouse: Optional[bool] = None,
        size_table_image: Optional[
            Sequence[Union["MaterialResource", Mapping[str, object], str]]
        ] = None,
        recommend_size_table_image: Optional[
            Sequence[Union["MaterialResource", Mapping[str, object], str]]
        ] = None,
        model_try_on_size_table_image: Optional[
            Sequence[Union["MaterialResource", Mapping[str, object], str]]
        ] = None,
        enable_main_spec_image: Optional[int] = None,
        create_sku_list: Optional[
            Sequence[Union["SkuV3", Mapping[str, object]]]
        ] = None,
        enable_step_presale: Optional[bool] = None,
        item_short_title: Optional[str] = None,
        # SKU parameters
        price: Optional[int] = None,
        original_price: Optional[int] = None,
        stock: Optional[int] = None,
        logistics_plan_id: Optional[str] = None,
        variants: Optional[Sequence[Union["VariantV3", Mapping[str, object]]]] = None,
        delivery_time: Optional[Union["DeliveryTimeV3", Mapping[str, object]]] = None,
        whcode: Optional[str] = None,
        price_type: Optional[int] = None,
        erp_code: Optional[str] = None,
        spec_image: Optional[str] = None,
        barcode: Optional[str] = None,
        extra: Optional[Mapping[str, object]] = None,
    ) -> None:
        super().__init__(method="product.createItemAndSku")
        self.name = name
        self.ename = ename
        self.brand_id = brand_id
        self.category_id = category_id
        self.attributes = [_ensure_attribute_v3(attr) for attr in attributes or []]
        self.shipping_template_id = shipping_template_id
        self.shipping_gross_weight = shipping_gross_weight
        self.variant_ids = list(variant_ids or [])
        self.images = [_ensure_material_resource(item) for item in images or []]
        self.standard_images = [
            _ensure_material_resource(item) for item in standard_images or []
        ]
        self.long_images = [
            _ensure_material_resource(item) for item in long_images or []
        ]
        self.videos = [_ensure_material_resource(item) for item in videos or []]
        self.video_url = video_url
        self.article_no = article_no
        self.image_descriptions = [
            _ensure_material_resource(item) for item in image_descriptions or []
        ]
        self.transparent_image = transparent_image
        self.description = description
        self.faq = [_ensure_faq(entry) for entry in faq or []]
        self.delivery_mode = delivery_mode
        self.free_return = free_return
        self.enable_multi_warehouse = enable_multi_warehouse
        self.size_table_image = [
            _ensure_material_resource(item) for item in size_table_image or []
        ]
        self.recommend_size_table_image = [
            _ensure_material_resource(item) for item in recommend_size_table_image or []
        ]
        self.model_try_on_size_table_image = [
            _ensure_material_resource(item)
            for item in model_try_on_size_table_image or []
        ]
        self.enable_main_spec_image = enable_main_spec_image

        # If individual SKU parameters are provided and no create_sku_list, create a default SKU
        if (
            price is not None
            or original_price is not None
            or stock is not None
            or logistics_plan_id is not None
            or variants
            or delivery_time is not None
            or erp_code is not None
            or spec_image is not None
            or barcode is not None
        ) and not create_sku_list:
            default_sku = SkuV3(
                price=price,
                original_price=original_price,
                stock=stock,
                logistics_plan_id=logistics_plan_id,
                variants=[_ensure_variant_v3(v) for v in (variants or [])],
                delivery_time=_ensure_delivery_time_v3(delivery_time)
                if delivery_time
                else None,
                erp_code=erp_code,
                spec_image=spec_image,
                barcode=barcode,
            )
            self.create_sku_list = [default_sku]
        else:
            self.create_sku_list = [
                _ensure_sku_v3(item) for item in create_sku_list or []
            ]

        self.enable_step_presale = enable_step_presale
        self.item_short_title = item_short_title
        # SKU parameters
        self.price = price
        self.original_price = original_price
        self.stock = stock
        self.logistics_plan_id = logistics_plan_id
        self.variants = [_ensure_variant_v3(entry) for entry in variants or []]
        self.delivery_time = (
            _ensure_delivery_time_v3(delivery_time) if delivery_time else None
        )
        self.whcode = whcode
        self.price_type = price_type
        self.erp_code = erp_code
        self.spec_image = spec_image
        self.barcode = barcode
        self.extra = dict(extra or {})

    def extra_payload(self) -> Dict[str, object]:
        payload = _item_and_sku_payload(
            name=self.name,
            ename=self.ename,
            brand_id=self.brand_id,
            category_id=self.category_id,
            attributes=self.attributes,
            shipping_template_id=self.shipping_template_id,
            shipping_gross_weight=self.shipping_gross_weight,
            variant_ids=self.variant_ids,
            images=self.images,
            standard_images=self.standard_images,
            long_images=self.long_images,
            videos=self.videos,
            article_no=self.article_no,
            image_descriptions=self.image_descriptions,
            transparent_image=self.transparent_image,
            description=self.description,
            delivery_mode=self.delivery_mode,
            free_return=self.free_return,
            enable_multi_warehouse=self.enable_multi_warehouse,
            size_table_image=self.size_table_image,
            recommend_size_table_image=self.recommend_size_table_image,
            model_try_on_size_table_image=self.model_try_on_size_table_image,
            enable_main_spec_image=self.enable_main_spec_image,
            create_sku_list=self.create_sku_list,
            enable_step_presale=self.enable_step_presale,
            item_short_title=self.item_short_title,
        )
        payload.update(self.extra)
        return payload


class UpdateItemAndSkuRequest(CreateItemAndSkuRequest):
    """Request wrapper for ``product.updateItemAndSku``."""

    def __init__(
        self,
        item_id: str,
        *,
        sku_id: Optional[str] = None,
        name: Optional[str] = None,
        ename: Optional[str] = None,
        brand_id: Optional[int] = None,
        category_id: Optional[str] = None,
        attributes: Optional[
            Sequence[Union["ItemAttributeV3", Mapping[str, object]]]
        ] = None,
        shipping_template_id: Optional[str] = None,
        shipping_gross_weight: Optional[int] = None,
        variant_ids: Optional[Sequence[str]] = None,
        images: Optional[
            Sequence[Union["MaterialResource", Mapping[str, object], str]]
        ] = None,
        standard_images: Optional[
            Sequence[Union["MaterialResource", Mapping[str, object], str]]
        ] = None,
        long_images: Optional[
            Sequence[Union["MaterialResource", Mapping[str, object], str]]
        ] = None,
        videos: Optional[
            Sequence[Union["MaterialResource", Mapping[str, object], str]]
        ] = None,
        video_url: Optional[str] = None,
        article_no: Optional[str] = None,
        image_descriptions: Optional[
            Sequence[Union["MaterialResource", Mapping[str, object], str]]
        ] = None,
        transparent_image: Optional[str] = None,
        description: Optional[str] = None,
        faq: Optional[Sequence[Union["ItemFaq", Mapping[str, object]]]] = None,
        delivery_mode: Optional[int] = None,
        free_return: Optional[int] = None,
        enable_multi_warehouse: Optional[bool] = None,
        size_table_image: Optional[
            Sequence[Union["MaterialResource", Mapping[str, object], str]]
        ] = None,
        recommend_size_table_image: Optional[
            Sequence[Union["MaterialResource", Mapping[str, object], str]]
        ] = None,
        model_try_on_size_table_image: Optional[
            Sequence[Union["MaterialResource", Mapping[str, object], str]]
        ] = None,
        enable_main_spec_image: Optional[int] = None,
        create_sku_list: Optional[
            Sequence[Union["SkuV3", Mapping[str, object]]]
        ] = None,
        enable_step_presale: Optional[bool] = None,
        item_short_title: Optional[str] = None,
        # SKU parameters
        price: Optional[int] = None,
        original_price: Optional[int] = None,
        stock: Optional[int] = None,
        logistics_plan_id: Optional[str] = None,
        variants: Optional[Sequence[Union["VariantV3", Mapping[str, object]]]] = None,
        delivery_time: Optional[Union["DeliveryTimeV3", Mapping[str, object]]] = None,
        whcode: Optional[str] = None,
        price_type: Optional[int] = None,
        erp_code: Optional[str] = None,
        spec_image: Optional[str] = None,
        barcode: Optional[str] = None,
        # Update-specific parameters
        update_sku_list: Optional[
            Sequence[Union["SkuV3", Mapping[str, object]]]
        ] = None,
        delete_sku_id_list: Optional[Sequence[str]] = None,
        extra: Optional[Mapping[str, object]] = None,
    ) -> None:
        super().__init__(
            name=name,
            ename=ename,
            brand_id=brand_id,
            category_id=category_id,
            attributes=attributes,
            shipping_template_id=shipping_template_id,
            shipping_gross_weight=shipping_gross_weight,
            variant_ids=variant_ids,
            images=images,
            standard_images=standard_images,
            long_images=long_images,
            videos=videos,
            video_url=video_url,
            article_no=article_no,
            image_descriptions=image_descriptions,
            transparent_image=transparent_image,
            description=description,
            faq=faq,
            delivery_mode=delivery_mode,
            free_return=free_return,
            enable_multi_warehouse=enable_multi_warehouse,
            size_table_image=size_table_image,
            recommend_size_table_image=recommend_size_table_image,
            model_try_on_size_table_image=model_try_on_size_table_image,
            enable_main_spec_image=enable_main_spec_image,
            create_sku_list=create_sku_list,
            enable_step_presale=enable_step_presale,
            item_short_title=item_short_title,
            price=price,
            original_price=original_price,
            stock=stock,
            logistics_plan_id=logistics_plan_id,
            variants=variants,
            delivery_time=delivery_time,
            whcode=whcode,
            price_type=price_type,
            erp_code=erp_code,
            spec_image=spec_image,
            barcode=barcode,
            extra=extra,
        )
        self.method = "product.updateItemAndSku"
        self.item_id = item_id
        self.sku_id = sku_id
        self.update_sku_list = [_ensure_sku_v3(item) for item in update_sku_list or []]
        self.delete_sku_id_list = list(delete_sku_id_list or [])

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = super().extra_payload()
        payload["itemId"] = self.item_id
        if self.update_sku_list:
            payload["updateSkuList"] = [
                sku.to_payload() for sku in self.update_sku_list
            ]
        if self.delete_sku_id_list:
            payload["deleteSkuIdList"] = list(self.delete_sku_id_list)
        return payload


class CreateSkuV3Request(BaseRequest):
    """Request wrapper for ``product.createSkuV2``."""

    def __init__(
        self,
        item_id: str,
        *,
        ipq: Optional[int] = None,
        original_price: Optional[int] = None,
        price: Optional[int] = None,
        stock: Optional[int] = None,
        logistics_plan_id: Optional[str] = None,
        whcode: Optional[str] = None,
        price_type: Optional[int] = None,
        erp_code: Optional[str] = None,
        variants: Optional[Sequence[Union["VariantV3", Mapping[str, object]]]] = None,
        delivery_time: Optional[Union["DeliveryTimeV3", Mapping[str, object]]] = None,
        spec_image: Optional[str] = None,
        barcode: Optional[str] = None,
        origin_sku_id: Optional[str] = None,
        boutique_mode: Optional[Union["BoutiqueMode", str]] = None,
        free_return: Optional[int] = None,
    ) -> None:
        super().__init__(method="product.createSkuV2")
        self.item_id = item_id
        self.ipq = ipq
        self.original_price = original_price
        self.price = price
        self.stock = stock
        self.logistics_plan_id = logistics_plan_id
        self.whcode = whcode
        self.price_type = price_type
        self.erp_code = erp_code
        self.variants = [_ensure_variant_v3(entry) for entry in variants or []]
        self.delivery_time = (
            _ensure_delivery_time_v3(delivery_time) if delivery_time else None
        )
        self.spec_image = spec_image
        self.barcode = barcode
        self.origin_sku_id = origin_sku_id
        self.boutique_mode = boutique_mode
        self.free_return = free_return

    def extra_payload(self) -> Dict[str, object]:
        payload = _filter_none(
            {
                "itemId": self.item_id,
                "ipq": self.ipq,
                "originalPrice": self.original_price,
                "price": self.price,
                "stock": self.stock,
                "logisticsPlanId": self.logistics_plan_id,
                "whcode": self.whcode,
                "priceType": self.price_type,
                "erpCode": self.erp_code,
                "specImage": self.spec_image,
                "barcode": self.barcode,
                "originSkuId": self.origin_sku_id,
                "boutiqueMode": _enum_value(self.boutique_mode),
                "freeReturn": self.free_return,
            }
        )
        if self.variants:
            payload["variants"] = [variant.to_payload() for variant in self.variants]
        if self.delivery_time is not None:
            payload["deliveryTime"] = self.delivery_time.to_payload()
        return payload


class UpdateSkuV3Request(CreateSkuV3Request):
    """Request wrapper for ``product.updateSkuV2``."""

    def __init__(
        self,
        sku_id: str,
        *,
        item_id: str,
        updated_fields: Optional[Sequence[str]] = None,
        ipq: Optional[int] = None,
        original_price: Optional[int] = None,
        price: Optional[int] = None,
        stock: Optional[int] = None,
        logistics_plan_id: Optional[str] = None,
        whcode: Optional[str] = None,
        price_type: Optional[int] = None,
        erp_code: Optional[str] = None,
        variants: Optional[Sequence[Union["VariantV3", Mapping[str, object]]]] = None,
        delivery_time: Optional[Union["DeliveryTimeV3", Mapping[str, object]]] = None,
        spec_image: Optional[str] = None,
        barcode: Optional[str] = None,
        origin_sku_id: Optional[str] = None,
        boutique_mode: Optional[Union["BoutiqueMode", str]] = None,
        free_return: Optional[int] = None,
    ) -> None:
        super().__init__(
            item_id,
            ipq=ipq,
            original_price=original_price,
            price=price,
            stock=stock,
            logistics_plan_id=logistics_plan_id,
            whcode=whcode,
            price_type=price_type,
            erp_code=erp_code,
            variants=variants,
            delivery_time=delivery_time,
            spec_image=spec_image,
            barcode=barcode,
            origin_sku_id=origin_sku_id,
            boutique_mode=boutique_mode,
            free_return=free_return,
        )
        self.method = "product.updateSkuV2"
        self.sku_id = sku_id
        self.updated_fields = list(updated_fields or [])

    def extra_payload(self) -> Dict[str, object]:
        payload = super().extra_payload()
        payload["id"] = self.sku_id
        if self.updated_fields:
            payload["updatedFields"] = list(self.updated_fields)
        return payload


class DeleteItemV3Request(BaseRequest):
    """Request wrapper for ``product.deleteItemV2``."""

    def __init__(self, *, item_ids: Sequence[str]) -> None:
        super().__init__(method="product.deleteItemV2")
        self.item_ids = list(item_ids)

    def extra_payload(self) -> Dict[str, object]:
        return {"itemIds": self.item_ids}


class DeleteSkuV3Request(BaseRequest):
    """Request wrapper for ``product.deleteSkuV2``."""

    def __init__(self, *, sku_ids: Sequence[str]) -> None:
        super().__init__(method="product.deleteSkuV2")
        self.sku_ids = list(sku_ids)

    def extra_payload(self) -> Dict[str, object]:
        return {"skuIds": self.sku_ids}


def _opt_str(value: object) -> Optional[str]:
    if value is None:
        return None
    return str(value)


def _opt_bool(value: object) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    return bool(value)


def _opt_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _int(value: Any, default: int = 0) -> int:
    result = _opt_int(value)
    return result if result is not None else default


def _opt_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_mapping(value: Mapping[str, object]) -> Dict[str, object]:
    return dict(value)


def _sequence(raw: object) -> List[object]:
    if raw is None:
        return []
    if isinstance(raw, SequenceABC) and not isinstance(
        raw, (str, bytes, bytearray, memoryview)
    ):
        return list(raw)
    return [raw]


def _ensure_attribute_value_v3(
    value: Union["AttributeValueV3", Mapping[str, object]],
) -> "AttributeValueV3":
    if isinstance(value, AttributeValueV3):
        return value
    if isinstance(value, MappingABC):
        return AttributeValueV3.from_dict(value)
    raise TypeError("attribute value must be AttributeValueV3 or mapping")


def _ensure_attribute_v3(
    value: Union["ItemAttributeV3", Mapping[str, object]],
) -> "ItemAttributeV3":
    if isinstance(value, ItemAttributeV3):
        return value
    if isinstance(value, MappingABC):
        return ItemAttributeV3.from_dict(value)
    raise TypeError("attribute must be ItemAttributeV3 or mapping")


def _ensure_faq(value: Union["ItemFaq", Mapping[str, object]]) -> "ItemFaq":
    if isinstance(value, ItemFaq):
        return value
    if isinstance(value, MappingABC):
        return ItemFaq.from_dict(value)
    raise TypeError("faq entry must be ItemFaq or mapping")


def _ensure_material_resource(
    value: Union["MaterialResource", Mapping[str, object], str],
) -> "MaterialResource":
    if isinstance(value, MaterialResource):
        return value
    if isinstance(value, MappingABC):
        return MaterialResource.from_dict(value)
    return MaterialResource.from_dict(value)


def _ensure_variant_v3(value: Union["VariantV3", Mapping[str, object]]) -> "VariantV3":
    if isinstance(value, VariantV3):
        return value
    if isinstance(value, MappingABC):
        return VariantV3.from_dict(value)
    raise TypeError("variant must be VariantV3 or mapping")


def _ensure_delivery_time_v3(
    value: Union["DeliveryTimeV3", Mapping[str, object], str, int],
) -> "DeliveryTimeV3":
    if isinstance(value, DeliveryTimeV3):
        return value
    if isinstance(value, (str, int)):
        return DeliveryTimeV3(time=_opt_str(value))
    if isinstance(value, MappingABC):
        return DeliveryTimeV3.from_dict(value)
    raise TypeError("delivery time must be DeliveryTimeV3, mapping, or primitive")


def _ensure_sku_v3(value: Union["SkuV3", Mapping[str, object]]) -> "SkuV3":
    if isinstance(value, SkuV3):
        return value
    if isinstance(value, MappingABC):
        return SkuV3.from_dict(value)
    raise TypeError("sku must be SkuV3 or mapping")


def _coerce_delivery_type(value: object) -> Optional[Union[str, int]]:
    if isinstance(value, MappingABC):
        code = value.get("code")
        if code is not None:
            coerced = _opt_int(code)
            if coerced is not None:
                return coerced
        name = value.get("name")
        if name is not None:
            return _opt_str(name)
        value_field = value.get("value")
        if value_field is not None:
            if isinstance(value_field, (str, int)):
                return value_field
            return _opt_str(value_field)
    if isinstance(value, Enum):
        coerced: object = _enum_value(value)
        if isinstance(coerced, (str, int)):
            return coerced
        return _opt_str(coerced)
    if isinstance(value, (str, int)):
        return value
    return _opt_str(value)


@dataclass
class AttributeValueV3:
    value_id: Optional[str] = None
    value: Optional[str] = None

    def to_payload(self) -> Dict[str, object]:
        return _filter_none({"valueId": self.value_id, "value": self.value})

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "AttributeValueV3":
        return cls(
            value_id=_opt_str(data.get("valueId")),
            value=_opt_str(data.get("value")),
        )


@dataclass
class ItemAttributeV3:
    property_id: Optional[str] = None
    name: Optional[str] = None
    value: Optional[str] = None
    value_id: Optional[str] = None
    value_list: List[AttributeValueV3] = field(default_factory=list)

    def to_payload(self) -> Dict[str, object]:
        payload = _filter_none(
            {
                "propertyId": self.property_id,
                "name": self.name,
                "value": self.value,
                "valueId": self.value_id,
            }
        )
        if self.value_list:
            payload["valueList"] = [item.to_payload() for item in self.value_list]
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "ItemAttributeV3":
        value_list_raw = data.get("valueList", [])
        values: List[AttributeValueV3] = []
        if isinstance(value_list_raw, SequenceABC):
            for entry in value_list_raw:
                if isinstance(entry, MappingABC):
                    values.append(AttributeValueV3.from_dict(entry))
        return cls(
            property_id=_opt_str(data.get("propertyId")),
            name=_opt_str(data.get("name")),
            value=_opt_str(data.get("value")),
            value_id=_opt_str(data.get("valueId")),
            value_list=values,
        )


@dataclass
class ItemFaq:
    question: Optional[str] = None
    answer: Optional[str] = None

    def to_payload(self) -> Dict[str, object]:
        return _filter_none({"question": self.question, "answer": self.answer})

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "ItemFaq":
        return cls(
            question=_opt_str(data.get("question")),
            answer=_opt_str(data.get("answer")),
        )


@dataclass
class MaterialResource:
    link: Optional[str] = None

    def to_payload(self) -> Dict[str, object]:
        return _filter_none({"link": self.link})

    @classmethod
    def from_dict(cls, data: object) -> "MaterialResource":
        if isinstance(data, MappingABC):
            return cls(link=_opt_str(data.get("link")))
        return cls(link=_opt_str(data))


@dataclass
class VariantV3:
    variant_id: Optional[str] = None
    name: Optional[str] = None
    value: Optional[str] = None
    value_id: Optional[str] = None

    def to_payload(self) -> Dict[str, object]:
        return _filter_none(
            {
                "id": self.variant_id,
                "name": self.name,
                "value": self.value,
                "valueId": self.value_id,
            }
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "VariantV3":
        return cls(
            variant_id=_opt_str(data.get("id")),
            name=_opt_str(data.get("name")),
            value=_opt_str(data.get("value")),
            value_id=_opt_str(data.get("valueId")),
        )


@dataclass
class DeliveryTimeV3:
    time: Optional[str] = None
    type: Optional[Union[str, int]] = None

    def to_payload(self) -> Dict[str, object]:
        return _filter_none({"time": self.time, "type": _enum_value(self.type)})

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "DeliveryTimeV3":
        return cls(
            time=_opt_str(data.get("time")),
            type=_coerce_delivery_type(data.get("type")),
        )


@dataclass
class SkuV3:
    sku_id: Optional[str] = None
    original_price: Optional[int] = None
    price: Optional[int] = None
    stock: Optional[int] = None
    logistics_plan_id: Optional[str] = None
    include_tax: Optional[bool] = None
    erp_code: Optional[str] = None
    variants: List[VariantV3] = field(default_factory=list)
    delivery_time: Optional[DeliveryTimeV3] = None
    spec_image: Optional[str] = None
    barcode: Optional[str] = None
    delivery_flag: Optional[int] = None

    def to_payload(self) -> Dict[str, object]:
        payload = _filter_none(
            {
                "skuId": self.sku_id,
                "originalPrice": self.original_price,
                "price": self.price,
                "stock": self.stock,
                "logisticsPlanId": self.logistics_plan_id,
                "includeTax": self.include_tax,
                "erpCode": self.erp_code,
                "specImage": self.spec_image,
                "barcode": self.barcode,
                "deliveryFlag": self.delivery_flag,
            }
        )
        if self.variants:
            payload["variants"] = [variant.to_payload() for variant in self.variants]
        if self.delivery_time is not None:
            payload["deliveryTime"] = self.delivery_time.to_payload()
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "SkuV3":
        variants_raw = data.get("variants", [])
        variants: List[VariantV3] = []
        if isinstance(variants_raw, SequenceABC):
            for entry in variants_raw:
                if isinstance(entry, MappingABC):
                    variants.append(VariantV3.from_dict(entry))
        delivery_time_raw = data.get("deliveryTime")
        delivery_time = None
        if isinstance(delivery_time_raw, MappingABC):
            delivery_time = DeliveryTimeV3.from_dict(delivery_time_raw)
        return cls(
            sku_id=_opt_str(data.get("skuId")),
            original_price=_opt_int(data.get("originalPrice")),
            price=_opt_int(data.get("price")),
            stock=_opt_int(data.get("stock")),
            logistics_plan_id=_opt_str(data.get("logisticsPlanId")),
            include_tax=_opt_bool(data.get("includeTax")),
            erp_code=_opt_str(data.get("erpCode")),
            variants=variants,
            delivery_time=delivery_time,
            spec_image=_opt_str(data.get("specImage")),
            barcode=_opt_str(data.get("barcode")),
            delivery_flag=_opt_int(data.get("deliveryFlag")),
        )


@dataclass
class UnionItemResultV3:
    item_id: Optional[str] = None
    name: Optional[str] = None
    sc_sku_code: Optional[str] = None
    barcode: Optional[str] = None
    ipq: Optional[int] = None
    erp_code: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "UnionItemResultV3":
        return cls(
            item_id=_opt_str(data.get("id")),
            name=_opt_str(data.get("name")),
            sc_sku_code=_opt_str(data.get("scSkuCode") or data.get("scSkucode")),
            barcode=_opt_str(data.get("barcode")),
            ipq=_opt_int(data.get("ipq")),
            erp_code=_opt_str(data.get("erpCode")),
        )


@dataclass
class ItemDetailV3:
    item_id: Optional[str]
    create_time: Optional[int]
    update_time: Optional[int]
    name: Optional[str]
    ename: Optional[str]
    brand_id: Optional[int]
    category_id: Optional[str]
    attributes: List[ItemAttributeV3] = field(default_factory=list)
    shipping_template_id: Optional[str] = None
    shipping_gross_weight: Optional[int] = None
    variant_ids: List[str] = field(default_factory=list)
    images: List[str] = field(default_factory=list)
    standard_images: List[str] = field(default_factory=list)
    long_images: List[str] = field(default_factory=list)
    video_url: Optional[str] = None
    article_no: Optional[str] = None
    image_descriptions: List[str] = field(default_factory=list)
    transparent_image: Optional[str] = None
    description: Optional[str] = None
    faq: List[ItemFaq] = field(default_factory=list)
    is_channel: Optional[bool] = None
    delivery_mode: Optional[int] = None
    free_return: Optional[int] = None
    union_type: Optional[int] = None
    image_bind_item: Optional[bool] = None
    images_desc_bind_item: Optional[bool] = None
    enable_multi_warehouse: Optional[bool] = None
    item_short_title: Optional[str] = None
    enable_step_presale: Optional[bool] = None
    enable_main_spec_image: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "ItemDetailV3":
        attributes = [
            ItemAttributeV3.from_dict(entry)
            for entry in _sequence(data.get("attributes"))
            if isinstance(entry, MappingABC)
        ]
        variant_ids = [
            str(item) for item in _sequence(data.get("variantIds")) if item is not None
        ]
        images = [
            str(item) for item in _sequence(data.get("images")) if item is not None
        ]
        standard_images = [
            str(item)
            for item in _sequence(data.get("standardImages"))
            if item is not None
        ]
        long_images = [
            str(item) for item in _sequence(data.get("longImages")) if item is not None
        ]
        image_descriptions = [
            str(item)
            for item in _sequence(data.get("imageDescriptions"))
            if item is not None
        ]
        faq = [
            ItemFaq.from_dict(entry)
            for entry in _sequence(data.get("faq"))
            if isinstance(entry, MappingABC)
        ]
        return cls(
            item_id=_opt_str(data.get("id")),
            create_time=_opt_int(data.get("createTime")),
            update_time=_opt_int(data.get("updateTime")),
            name=_opt_str(data.get("name")),
            ename=_opt_str(data.get("ename")),
            brand_id=_opt_int(data.get("brandId")),
            category_id=_opt_str(data.get("categoryId")),
            attributes=attributes,
            shipping_template_id=_opt_str(data.get("shippingTemplateId")),
            shipping_gross_weight=_opt_int(data.get("shippingGrossWeight")),
            variant_ids=variant_ids,
            images=images,
            standard_images=standard_images,
            long_images=long_images,
            video_url=_opt_str(data.get("videoUrl")),
            article_no=_opt_str(data.get("articleNo")),
            image_descriptions=image_descriptions,
            transparent_image=_opt_str(data.get("transparentImage")),
            description=_opt_str(data.get("description")),
            faq=faq,
            is_channel=_opt_bool(data.get("isChannel")),
            delivery_mode=_opt_int(data.get("deliveryMode")),
            free_return=_opt_int(data.get("freeReturn")),
            union_type=_opt_int(data.get("unionType")),
            image_bind_item=_opt_bool(data.get("imageBindItem")),
            images_desc_bind_item=_opt_bool(data.get("imagesDescBindItem")),
            enable_multi_warehouse=_opt_bool(data.get("enableMultiWarehouse")),
            item_short_title=_opt_str(data.get("itemShortTitle")),
            enable_step_presale=_opt_bool(data.get("enableStepPresale")),
            enable_main_spec_image=_opt_bool(data.get("enableMainSpecImage")),
        )


@dataclass
class ItemAndSkuDetail:
    item_id: Optional[str]
    name: Optional[str]
    ename: Optional[str]
    brand_id: Optional[int]
    category_id: Optional[str]
    attributes: List[ItemAttributeV3]
    shipping_template_id: Optional[str]
    shipping_gross_weight: Optional[int]
    variant_ids: List[str]
    images: List[MaterialResource]
    standard_images: List[MaterialResource]
    long_images: List[MaterialResource]
    videos: List[MaterialResource]
    article_no: Optional[str]
    image_descriptions: List[MaterialResource]
    transparent_image: Optional[str]
    description: Optional[str]
    delivery_mode: Optional[int]
    free_return: Optional[int]
    enable_multi_warehouse: Optional[bool]
    size_table_image: List[MaterialResource]
    recommend_size_table_image: List[MaterialResource]
    model_try_on_size_table_image: List[MaterialResource]
    enable_main_spec_image: Optional[int]
    sku_list: List[SkuV3]
    enable_step_presale: Optional[bool]
    item_short_title: Optional[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "ItemAndSkuDetail":
        attributes = [
            ItemAttributeV3.from_dict(entry)
            for entry in _sequence(data.get("attributes"))
            if isinstance(entry, MappingABC)
        ]
        variant_ids = [
            str(entry)
            for entry in _sequence(data.get("variantIds"))
            if entry is not None
        ]
        images = [
            MaterialResource.from_dict(entry) for entry in _sequence(data.get("images"))
        ]
        standard_images = [
            MaterialResource.from_dict(entry)
            for entry in _sequence(data.get("standardImages"))
        ]
        long_images = [
            MaterialResource.from_dict(entry)
            for entry in _sequence(data.get("longImages"))
        ]
        videos = [
            MaterialResource.from_dict(entry) for entry in _sequence(data.get("videos"))
        ]
        image_descriptions = [
            MaterialResource.from_dict(entry)
            for entry in _sequence(data.get("imageDescriptions"))
        ]
        size_table_image = [
            MaterialResource.from_dict(entry)
            for entry in _sequence(data.get("sizeTableImage"))
        ]
        recommend_size_table_image = [
            MaterialResource.from_dict(entry)
            for entry in _sequence(data.get("recommendSizeTableImage"))
        ]
        model_try_on_size_table_image = [
            MaterialResource.from_dict(entry)
            for entry in _sequence(data.get("modelTryOnSizeTableImage"))
        ]
        sku_list = [
            SkuV3.from_dict(entry)
            for entry in _sequence(data.get("skuList"))
            if isinstance(entry, MappingABC)
        ]
        return cls(
            item_id=_opt_str(data.get("itemId")),
            name=_opt_str(data.get("name")),
            ename=_opt_str(data.get("ename")),
            brand_id=_opt_int(data.get("brandId")),
            category_id=_opt_str(data.get("categoryId")),
            attributes=attributes,
            shipping_template_id=_opt_str(data.get("shippingTemplateId")),
            shipping_gross_weight=_opt_int(data.get("shippingGrossWeight")),
            variant_ids=variant_ids,
            images=images,
            standard_images=standard_images,
            long_images=long_images,
            videos=videos,
            article_no=_opt_str(data.get("articleNo")),
            image_descriptions=image_descriptions,
            transparent_image=_opt_str(data.get("transparentImage")),
            description=_opt_str(data.get("description")),
            delivery_mode=_opt_int(data.get("deliveryMode")),
            free_return=_opt_int(data.get("freeReturn")),
            enable_multi_warehouse=_opt_bool(data.get("enableMultiWarehouse")),
            size_table_image=size_table_image,
            recommend_size_table_image=recommend_size_table_image,
            model_try_on_size_table_image=model_try_on_size_table_image,
            enable_main_spec_image=_opt_int(data.get("enableMainSpecImage")),
            sku_list=sku_list,
            enable_step_presale=_opt_bool(data.get("enableStepPresale")),
            item_short_title=_opt_str(data.get("itemShortTitle")),
        )


@dataclass
class SkuDetail:
    sku_id: Optional[str]
    sc_sku_code: Optional[str]
    buyable: Optional[bool]
    union_item_details: List[UnionItemResultV3]
    create_time: Optional[int]
    update_time: Optional[int]
    name: Optional[str]
    is_gift: Optional[bool]
    item_id: Optional[str]
    ipq: Optional[int]
    original_price: Optional[int]
    price: Optional[int]
    stock: Optional[int]
    logistics_plan_id: Optional[str]
    whcode: Optional[str]
    price_type: Optional[int]
    erp_code: Optional[str]
    variants: List[VariantV3]
    delivery_time: Optional[DeliveryTimeV3]
    spec_image: Optional[str]
    barcode: Optional[str]
    origin_sku_id: Optional[str]
    boutique_mode: Optional[str]
    free_return: Optional[int]
    row_number: Optional[int]
    delivery_flag: Optional[int]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "SkuDetail":
        variants_raw = data.get("variants", [])
        variants: List[VariantV3] = []
        if isinstance(variants_raw, SequenceABC):
            for entry in variants_raw:
                if isinstance(entry, MappingABC):
                    variants.append(VariantV3.from_dict(entry))
        delivery_time_raw = data.get("deliveryTime")
        delivery_time = None
        if isinstance(delivery_time_raw, MappingABC):
            delivery_time = DeliveryTimeV3.from_dict(delivery_time_raw)
        union_raw = data.get("unionItemDetails", [])
        union_details: List[UnionItemResultV3] = []
        if isinstance(union_raw, SequenceABC):
            for entry in union_raw:
                if isinstance(entry, MappingABC):
                    union_details.append(UnionItemResultV3.from_dict(entry))
        return cls(
            sku_id=_opt_str(data.get("id")),
            sc_sku_code=_opt_str(data.get("scSkucode") or data.get("scSkuCode")),
            buyable=_opt_bool(data.get("buyable")),
            union_item_details=union_details,
            create_time=_opt_int(data.get("createTime")),
            update_time=_opt_int(data.get("updateTime")),
            name=_opt_str(data.get("name")),
            is_gift=_opt_bool(data.get("isGift")),
            item_id=_opt_str(data.get("itemId")),
            ipq=_opt_int(data.get("ipq")),
            original_price=_opt_int(data.get("originalPrice")),
            price=_opt_int(data.get("price")),
            stock=_opt_int(data.get("stock")),
            logistics_plan_id=_opt_str(data.get("logisticsPlanId")),
            whcode=_opt_str(data.get("whcode")),
            price_type=_opt_int(data.get("priceType")),
            erp_code=_opt_str(data.get("erpCode")),
            variants=variants,
            delivery_time=delivery_time,
            spec_image=_opt_str(data.get("specImage")),
            barcode=_opt_str(data.get("barcode")),
            origin_sku_id=_opt_str(data.get("originSkuId")),
            boutique_mode=_opt_str(data.get("boutiqueMode")),
            free_return=_opt_int(data.get("freeReturn")),
            row_number=_opt_int(data.get("rowNumber")),
            delivery_flag=_opt_int(data.get("deliveryFlag")),
        )


@dataclass
class BasicItem:
    item_id: str
    name: Optional[str] = None
    spu_id: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    status: Optional[int] = None
    buyable: Optional[bool] = None
    freeze: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "BasicItem":
        return cls(
            item_id=_opt_str(data.get("itemId")) or "",
            name=_opt_str(data.get("name")),
            spu_id=_opt_str(data.get("spuId")),
            price=_opt_float(data.get("price")),
            stock=_opt_int(data.get("stock")),
            status=_opt_int(data.get("status")),
            buyable=_opt_bool(data.get("buyable")),
            freeze=_opt_bool(data.get("freeze")),
        )


@dataclass
class PageInfo:
    current_page: int
    page_size: int
    total: int

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "PageInfo":
        return cls(
            current_page=_int(data.get("currentPage")),
            page_size=_int(data.get("pageSize")),
            total=_int(data.get("total")),
        )


@dataclass
class GetBasicItemListResponse:
    hits: List[BasicItem] = field(default_factory=list)
    page: PageInfo = field(default_factory=lambda: PageInfo(0, 0, 0))

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetBasicItemListResponse":
        hits_raw = data.get("hits", [])
        if not isinstance(hits_raw, SequenceABC):
            hits_raw = []
        hits = [
            BasicItem.from_dict(item)
            for item in hits_raw
            if isinstance(item, MappingABC)
        ]
        page = PageInfo.from_dict(data)
        return cls(hits=hits, page=page)


@dataclass
class SpuInfo:
    spu_id: Optional[str]
    name: Optional[str]
    brand_id: Optional[str]
    category_id: Optional[str]
    image_urls: List[str] = field(default_factory=list)
    desc: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "SpuInfo":
        images = data.get("imageUrls")
        image_list = (
            [str(item) for item in images] if isinstance(images, SequenceABC) else []
        )
        return cls(
            spu_id=_opt_str(data.get("id")) or _opt_str(data.get("spuId")),
            name=_opt_str(data.get("name")),
            brand_id=_opt_str(data.get("brandId")),
            category_id=_opt_str(data.get("categoryId")),
            image_urls=image_list,
            desc=_opt_str(data.get("desc")),
        )


@dataclass
class ItemDetail:
    spu: Optional[SpuInfo]
    item: Optional[BasicItem]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "ItemDetail":
        spu_data = data.get("spuData")
        item_data = data.get("itemData")
        spu = SpuInfo.from_dict(spu_data) if isinstance(spu_data, MappingABC) else None
        item = (
            BasicItem.from_dict(item_data)
            if isinstance(item_data, MappingABC)
            else None
        )
        return cls(spu=spu, item=item)


@dataclass
class GetDetailItemListResponse:
    items: List[ItemDetail] = field(default_factory=list)
    page: PageInfo = field(default_factory=lambda: PageInfo(0, 0, 0))

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetDetailItemListResponse":
        records = data.get("data", [])
        if not isinstance(records, SequenceABC):
            records = []
        items = [
            ItemDetail.from_dict(item)
            for item in records
            if isinstance(item, MappingABC)
        ]
        page = PageInfo.from_dict(data)
        return cls(items=items, page=page)


@dataclass
class GetSpuInfoResponse:
    spu: SpuInfo

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetSpuInfoResponse":
        return cls(spu=SpuInfo.from_dict(data))


@dataclass
class SpuImage:
    link: Optional[str]
    name: Optional[str]
    path: Optional[str]
    extension: Optional[str]
    width: Optional[int]
    height: Optional[int]
    fingerprint: Optional[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "SpuImage":
        return cls(
            link=_opt_str(data.get("link")),
            name=_opt_str(data.get("name")),
            path=_opt_str(data.get("path")),
            extension=_opt_str(data.get("extension")),
            width=_opt_int(data.get("width")),
            height=_opt_int(data.get("height")),
            fingerprint=_opt_str(data.get("fingerprint")),
        )


@dataclass
class SpuBasicInfo:
    spu_id: Optional[str]
    name: Optional[str]
    min_price: Optional[float]
    max_price: Optional[float]
    buyable: Optional[bool]
    stock: Optional[int]
    category_id: Optional[str]
    min_create_time: Optional[int]
    max_create_time: Optional[int]
    top_image: Optional[SpuImage]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "SpuBasicInfo":
        top_image_data = data.get("topImage")
        top_image = (
            SpuImage.from_dict(top_image_data)
            if isinstance(top_image_data, MappingABC)
            else None
        )
        return cls(
            spu_id=_opt_str(data.get("id")),
            name=_opt_str(data.get("name")),
            min_price=_opt_float(data.get("minPrice")),
            max_price=_opt_float(data.get("maxPrice")),
            buyable=_opt_bool(data.get("buyable")),
            stock=_opt_int(data.get("stock")),
            category_id=_opt_str(data.get("categoryId")),
            min_create_time=_opt_int(data.get("minCreateTime")),
            max_create_time=_opt_int(data.get("maxCreateTime")),
            top_image=top_image,
        )


@dataclass
class GetBasicSpuResponse:
    spus: List[SpuBasicInfo]
    page: PageInfo

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetBasicSpuResponse":
        spus_raw = data.get("spuBasicInfos", [])
        if not isinstance(spus_raw, SequenceABC):
            spus_raw = []
        spus = [
            SpuBasicInfo.from_dict(item)
            for item in spus_raw
            if isinstance(item, MappingABC)
        ]
        page = PageInfo.from_dict(data)
        return cls(spus=spus, page=page)


@dataclass
class BaseItemResponse:
    item_id: Optional[str]
    available: Optional[bool]
    logistics_plan_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "BaseItemResponse":
        return cls(
            item_id=_opt_str(data.get("itemId")) or _opt_str(data.get("id")),
            available=_opt_bool(data.get("available")),
            logistics_plan_id=_opt_str(data.get("logisticsPlanId")),
        )


@dataclass
class SpuOperationResponse:
    spu_id: Optional[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "SpuOperationResponse":
        return cls(spu_id=_opt_str(data.get("spuId")) or _opt_str(data.get("id")))


@dataclass
class DeleteSpuResponse:
    deleted: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "DeleteSpuResponse":
        deleted = data.get("deleted")
        if isinstance(deleted, SequenceABC):
            return cls(deleted=[str(item) for item in deleted])
        return cls()


__all__ = [
    "GetBasicItemListRequest",
    "GetDetailItemListRequest",
    "GetDetailSkuListRequest",
    "GetSpuInfoRequest",
    "GetItemInfoRequest",
    "SearchItemListRequest",
    "UpdateLogisticsPlanRequest",
    "UpdateAvailabilityRequest",
    "CreateSpuRequest",
    "UpdateSpuRequest",
    "DeleteSpuRequest",
    "CreateItemRequest",
    "UpdateItemRequest",
    "DeleteItemRequest",
    "CreateItemV3Request",
    "UpdateItemV3Request",
    "CreateItemAndSkuRequest",
    "UpdateItemAndSkuRequest",
    "CreateSkuV3Request",
    "UpdateSkuV3Request",
    "DeleteItemV3Request",
    "DeleteSkuV3Request",
    "GetBasicSpuRequest",
    "UpdateItemPriceRequest",
    "UpdateSkuLogisticsPlanRequest",
    "UpdateSkuPriceRequest",
    "UpdateSkuAvailableRequest",
    "UpdateItemImageRequest",
    "UpdateSpuImageRequest",
    "UpdateVariantImageRequest",
    "BasicItem",
    "PageInfo",
    "GetBasicItemListResponse",
    "SpuInfo",
    "ItemDetail",
    "GetDetailItemListResponse",
    "GetSpuInfoResponse",
    "SpuImage",
    "SpuBasicInfo",
    "GetBasicSpuResponse",
    "BaseItemResponse",
    "SpuOperationResponse",
    "DeleteSpuResponse",
    "AttributeValueV3",
    "ItemAttributeV3",
    "ItemFaq",
    "MaterialResource",
    "VariantV3",
    "DeliveryTimeV3",
    "SkuV3",
    "ItemDetailV3",
    "ItemAndSkuDetail",
    "SkuDetail",
    "UnionItemResultV3",
]
