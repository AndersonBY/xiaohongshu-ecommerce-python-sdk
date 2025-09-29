"""Common module models."""

from __future__ import annotations

from collections.abc import Mapping as MappingABC, Sequence as SequenceABC
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Protocol, Type, TypeVar

from .base import BaseRequest


class GetCategoriesRequest(BaseRequest):
    def __init__(self, category_id: Optional[str] = None) -> None:
        super().__init__(method="common.getCategories")
        self.category_id = category_id

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {}
        if self.category_id is not None:
            payload["categoryId"] = self.category_id
        return payload


class GetAttributeValuesRequest(BaseRequest):
    def __init__(self, attribute_id: str) -> None:
        super().__init__(method="common.getAttributeValues")
        self.attribute_id = attribute_id

    def extra_payload(self) -> Dict[str, object]:
        return {"attributeId": self.attribute_id}


class GetAttributeListRequest(BaseRequest):
    def __init__(self, category_id: str) -> None:
        super().__init__(method="common.getAttributeLists")
        self.category_id = category_id

    def extra_payload(self) -> Dict[str, object]:
        return {"categoryId": self.category_id}


class GetVariationsRequest(BaseRequest):
    def __init__(self, category_id: str) -> None:
        super().__init__(method="common.getVariations")
        self.category_id = category_id

    def extra_payload(self) -> Dict[str, object]:
        return {"categoryId": self.category_id}


class GetExpressCompanyListRequest(BaseRequest):
    def __init__(self) -> None:
        super().__init__(method="common.getExpressCompanyList")


class GetLogisticsListRequest(BaseRequest):
    def __init__(self) -> None:
        super().__init__(method="common.getLogisticsList")


class GetLogisticsModeRequest(BaseRequest):
    def __init__(self) -> None:
        super().__init__(method="common.getLogisticsMode")


class GetCarriageTemplateListRequest(BaseRequest):
    def __init__(
        self, page_index: Optional[int] = None, page_size: Optional[int] = None
    ) -> None:
        super().__init__(method="common.getCarriageTemplateList")
        self.page_index = page_index
        self.page_size = page_size

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {}
        if self.page_index is not None:
            payload["pageIndex"] = self.page_index
        if self.page_size is not None:
            payload["pageSize"] = self.page_size
        return payload


class GetCarriageTemplateRequest(BaseRequest):
    def __init__(self, template_id: str) -> None:
        super().__init__(method="common.getCarriageTemplate")
        self.template_id = template_id

    def extra_payload(self) -> Dict[str, object]:
        return {"templateId": self.template_id}


class GetBrandRequest(BaseRequest):
    def __init__(
        self,
        *,
        category_id: Optional[str] = None,
        keyword: Optional[str] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> None:
        super().__init__(method="common.brandSearch")
        self.category_id = category_id
        self.keyword = keyword
        self.page_no = page_no
        self.page_size = page_size

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {}
        if self.category_id is not None:
            payload["categoryId"] = self.category_id
        if self.keyword is not None:
            payload["keyword"] = self.keyword
        if self.page_no is not None:
            payload["pageNo"] = self.page_no
        if self.page_size is not None:
            payload["pageSize"] = self.page_size
        return payload


class GetSellerKeyInfoRequest(BaseRequest):
    def __init__(self) -> None:
        super().__init__(method="common.getSellerKeyInfo")


class GetNestZoneRequest(BaseRequest):
    def __init__(self) -> None:
        super().__init__(method="common.getNestZone")


class CategoryMatchRequest(BaseRequest):
    def __init__(self, spu_name: str, top_k: Optional[int] = None) -> None:
        super().__init__(method="common.categoryMatch")
        self.spu_name = spu_name
        self.top_k = top_k

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {"spuName": self.spu_name}
        if self.top_k is not None:
            payload["topK"] = self.top_k
        return payload


class CategoryMatchV2Request(BaseRequest):
    def __init__(
        self,
        name: str,
        scene: Optional[str] = None,
        image_urls: Optional[List[str]] = None,
    ) -> None:
        super().__init__(method="common.categoryMatchV2")
        self.name = name
        self.scene = scene
        self.image_urls = list(image_urls or [])

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {"name": self.name}
        if self.scene is not None:
            payload["scene"] = self.scene
        if self.image_urls:
            payload["imageUrls"] = self.image_urls
        return payload


class BatchGetDeliveryRuleRequest(BaseRequest):
    class DeliveryRuleQuery:
        def __init__(
            self,
            *,
            whcode: Optional[str] = None,
            logistics_plan_id: Optional[str] = None,
            category_id: Optional[str] = None,
            item_id: Optional[str] = None,
        ) -> None:
            self.whcode = whcode
            self.logistics_plan_id = logistics_plan_id
            self.category_id = category_id
            self.item_id = item_id

        def to_payload(self) -> Dict[str, Optional[str]]:
            return {
                key: value
                for key, value in {
                    "whcode": self.whcode,
                    "logisticsPlanId": self.logistics_plan_id,
                    "categoryId": self.category_id,
                    "itemId": self.item_id,
                }.items()
                if value is not None
            }

    def __init__(
        self, queries: List["BatchGetDeliveryRuleRequest.DeliveryRuleQuery"]
    ) -> None:
        super().__init__(method="common.getDeliveryRule")
        self.queries = queries

    def extra_payload(self) -> Dict[str, object]:
        return {"getDeliveryRuleRequests": [q.to_payload() for q in self.queries]}


class GetSellerAddressRecordBySellerIdRequest(BaseRequest):
    def __init__(
        self, page_index: Optional[int] = None, page_size: Optional[int] = None
    ) -> None:
        super().__init__(method="common.getAddressRecord")
        self.page_index = page_index
        self.page_size = page_size

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {}
        if self.page_index is not None:
            payload["pageIndex"] = self.page_index
        if self.page_size is not None:
            payload["pageSize"] = self.page_size
        return payload


class GetZonesRequest(BaseRequest):
    def __init__(
        self,
        *,
        code: Optional[str] = None,
        name: Optional[str] = None,
        upper: Optional[str] = None,
        filter_non_continental: Optional[bool] = None,
    ) -> None:
        super().__init__(method="common.getZones")
        self.code = code
        self.name = name
        self.upper = upper
        self.filter_non_continental = filter_non_continental

    def extra_payload(self) -> Dict[str, object]:
        payload: Dict[str, object] = {}
        if self.code is not None:
            payload["code"] = self.code
        if self.name is not None:
            payload["name"] = self.name
        if self.upper is not None:
            payload["upper"] = self.upper
        if self.filter_non_continental is not None:
            payload["filterNonContinental"] = self.filter_non_continental
        return payload


class CheckForbiddenKeywordRequest(BaseRequest):
    def __init__(self, text: str) -> None:
        super().__init__(method="common.checkForbiddenKeyword")
        self.text = text

    def extra_payload(self) -> Dict[str, object]:
        return {"text": self.text}


@dataclass
class Category:
    id: str
    name: str
    en_name: Optional[str] = None
    support_size_table: Optional[bool] = None
    support_recommend_size_table: Optional[bool] = None
    support_model_try_on_size_table: Optional[bool] = None
    support_main_spec_image: Optional[bool] = None
    main_spec_id: Optional[str] = None
    is_leaf: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "Category":
        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            en_name=_opt_str(data.get("enName")),
            support_size_table=_opt_bool(data.get("supportSizeTable")),
            support_recommend_size_table=_opt_bool(
                data.get("supportRecommendSizeTable")
            ),
            support_model_try_on_size_table=_opt_bool(
                data.get("supportModelTryOnSizeTable")
            ),
            support_main_spec_image=_opt_bool(data.get("supportMainSpecImage")),
            main_spec_id=_opt_str(data.get("mainSpecId")),
            is_leaf=_opt_bool(data.get("isLeaf")),
        )


@dataclass
class GetCategoriesResponse:
    seller_in_category_gray: Optional[bool]
    categories: List[Category]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetCategoriesResponse":
        categories = _coerce_many(data.get("categoryV3s"), Category)
        return cls(
            seller_in_category_gray=_opt_bool(data.get("sellerInCategoryGray")),
            categories=categories,
        )


@dataclass
class Attribute:
    id: str
    name: str
    en_name: Optional[str]
    is_required: Optional[bool]
    accepts_image: Optional[bool]
    is_multi: Optional[bool]
    input_type: Optional[int]
    data_type: Optional[int]
    customizable: Optional[bool]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "Attribute":
        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            en_name=_opt_str(data.get("enName")),
            is_required=_opt_bool(data.get("isRequired")),
            accepts_image=_opt_bool(data.get("acceptsImage")),
            is_multi=_opt_bool(data.get("isMulti")),
            input_type=_opt_int(data.get("inputType")),
            data_type=_opt_int(data.get("dataType")),
            customizable=_opt_bool(data.get("customizable")),
        )


@dataclass
class GetAttributeListResponse:
    attributes: List[Attribute]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetAttributeListResponse":
        attributes = _coerce_many(data.get("attributeV3s"), Attribute)
        return cls(attributes=attributes)


@dataclass
class AttributeValue:
    value_id: str
    value_name: str

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "AttributeValue":
        return cls(
            value_id=str(data.get("valueId", "")),
            value_name=str(data.get("valueName", "")),
        )


@dataclass
class GetAttributeValuesResponse:
    values: List[AttributeValue]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetAttributeValuesResponse":
        values = _coerce_many(data.get("attributeValueV3s"), AttributeValue)
        return cls(values=values)


@dataclass
class Variation:
    id: str
    name: str
    en_name: Optional[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "Variation":
        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            en_name=_opt_str(data.get("enName")),
        )


@dataclass
class GetVariationsResponse:
    variations: List[Variation]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetVariationsResponse":
        variations = _coerce_many(data.get("variations"), Variation)
        return cls(variations=variations)


@dataclass
class ExpressCompany:
    express_company_id: int
    code: Optional[str]
    name: Optional[str]
    comment: Optional[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "ExpressCompany":
        return cls(
            express_company_id=_int(data.get("expressCompanyId")),
            code=_opt_str(data.get("expressCompanyCode")),
            name=_opt_str(data.get("expressCompanyName")),
            comment=_opt_str(data.get("comment")),
        )


@dataclass
class GetExpressCompanyListResponse:
    express_company_infos: List[ExpressCompany]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetExpressCompanyListResponse":
        infos = _coerce_many(data.get("expressCompanyInfos"), ExpressCompany)
        return cls(express_company_infos=infos)


@dataclass
class LogisticsPlan:
    plan_info_id: Optional[str]
    plan_info_name: Optional[str]
    logistic_name: Optional[str]
    logistics_company_code: Optional[str]
    trade_mode: Optional[int]
    customs_code: Optional[str]
    is_valid: Optional[bool]
    country_name: Optional[str]
    province_name: Optional[str]
    city_name: Optional[str]
    street: Optional[str]
    post_code: Optional[str]
    seller_address_record_id: Optional[int]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "LogisticsPlan":
        return cls(
            plan_info_id=_opt_str(data.get("planInfoId")),
            plan_info_name=_opt_str(data.get("planInfoName")),
            logistic_name=_opt_str(data.get("logisticName")),
            logistics_company_code=_opt_str(data.get("logisticsCompanyCode")),
            trade_mode=_opt_int(data.get("tradeMode")),
            customs_code=_opt_str(data.get("customsCode")),
            is_valid=_opt_bool(data.get("isValid")),
            country_name=_opt_str(data.get("countryName")),
            province_name=_opt_str(data.get("privinceName")),
            city_name=_opt_str(data.get("cityName")),
            street=_opt_str(data.get("street")),
            post_code=_opt_str(data.get("postCode")),
            seller_address_record_id=_opt_int(data.get("sellerAddressRecordId")),
        )


@dataclass
class GetLogisticsListResponse:
    logistics_plans: List[LogisticsPlan]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetLogisticsListResponse":
        plans = _coerce_many(data.get("logisticsPlans"), LogisticsPlan)
        return cls(logistics_plans=plans)


@dataclass
class CarriageTemplate:
    template_id: Optional[str]
    template_name: Optional[str]
    template_type: Optional[int]
    cost_type: Optional[int]
    express_type: Optional[int]
    support_not_delivery: Optional[bool]
    not_delivery_areas: List[str] = field(default_factory=list)
    normal_config: Optional[Mapping[str, Any]] = None
    enabled: Optional[bool] = None
    syncd_at: Optional[int] = None
    create_by: Optional[str] = None
    create_at: Optional[int] = None
    update_at: Optional[int] = None
    send_address: Optional[Mapping[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "CarriageTemplate":
        return cls(
            template_id=_opt_str(data.get("templateId")),
            template_name=_opt_str(data.get("templateName")),
            template_type=_opt_int(data.get("templateType")),
            cost_type=_opt_int(data.get("costType")),
            express_type=_opt_int(data.get("expressType")),
            support_not_delivery=_opt_bool(data.get("supportNotDelivery")),
            not_delivery_areas=[
                str(item) for item in _sequence(data.get("notDeliveryAreas"))
            ],
            normal_config=_opt_mapping(data.get("normalConfig")),
            enabled=_opt_bool(data.get("enabled")),
            syncd_at=_opt_int(data.get("syncdAt")),
            create_by=_opt_str(data.get("createBy")),
            create_at=_opt_int(data.get("createAt")),
            update_at=_opt_int(data.get("updateAt")),
            send_address=_opt_mapping(data.get("sendAddress")),
        )


@dataclass
class GetCarriageTemplateListResponse:
    carriage_template_list: List[CarriageTemplate]
    total_count: Optional[int]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetCarriageTemplateListResponse":
        templates = _coerce_many(data.get("carriageTemplateList"), CarriageTemplate)
        total = data.get("totalCount")
        return cls(carriage_template_list=templates, total_count=_opt_int(total))


@dataclass
class GetCarriageTemplateResponse:
    template: CarriageTemplate

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetCarriageTemplateResponse":
        template = CarriageTemplate.from_dict(data)
        return cls(template=template)


@dataclass
class Brand:
    id: Optional[str]
    name: Optional[str]
    en_name: Optional[str]
    image: Optional[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "Brand":
        return cls(
            id=_opt_str(data.get("id")),
            name=_opt_str(data.get("name")),
            en_name=_opt_str(data.get("enName")),
            image=_opt_str(data.get("image")),
        )


@dataclass
class GetBrandResponse:
    brands: List[Brand]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetBrandResponse":
        brands = _coerce_many(data.get("brands"), Brand)
        return cls(brands=brands)


@dataclass
class LogisticMode:
    logistics_code: Optional[str]
    logistics_translation: Optional[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "LogisticMode":
        return cls(
            logistics_code=_opt_str(data.get("logisticsCode")),
            logistics_translation=_opt_str(data.get("logisticsTranslation")),
        )


@dataclass
class GetLogisticsModeResponse:
    logistic_modes: List[LogisticMode]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetLogisticsModeResponse":
        modes = _coerce_many(data.get("logisticModes"), LogisticMode)
        return cls(logistic_modes=modes)


@dataclass
class GetSellerKeyInfoResponse:
    seller_id: Optional[str]
    app_key: Optional[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetSellerKeyInfoResponse":
        return cls(
            seller_id=_opt_str(data.get("sellerId")),
            app_key=_opt_str(data.get("appKey")),
        )


@dataclass
class NestZone:
    id: Optional[str]
    code: Optional[str]
    name: Optional[str]
    upper: Optional[str]
    zipcode: Optional[str]
    is_deactive: Optional[bool]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "NestZone":
        return cls(
            id=_opt_str(data.get("id")),
            code=_opt_str(data.get("code")),
            name=_opt_str(data.get("name")),
            upper=_opt_str(data.get("upper")),
            zipcode=_opt_str(data.get("zipcode")),
            is_deactive=_opt_bool(data.get("isDeactive")),
        )


@dataclass
class CityZone(NestZone):
    zones: List[NestZone] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "CityZone":
        base = super().from_dict(data)
        zones = _coerce_many(data.get("zones"), NestZone)
        return cls(
            id=base.id,
            code=base.code,
            name=base.name,
            upper=base.upper,
            zipcode=base.zipcode,
            is_deactive=base.is_deactive,
            zones=zones,
        )


@dataclass
class ProvinceZone(NestZone):
    zones: List[CityZone] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "ProvinceZone":
        base = super().from_dict(data)
        zones = _coerce_many(data.get("zones"), CityZone)
        return cls(
            id=base.id,
            code=base.code,
            name=base.name,
            upper=base.upper,
            zipcode=base.zipcode,
            is_deactive=base.is_deactive,
            zones=zones,
        )


@dataclass
class GetNestZoneResponse:
    province_zone_list: List[ProvinceZone]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetNestZoneResponse":
        zones = _coerce_many(data.get("provinceZoneList"), ProvinceZone)
        return cls(province_zone_list=zones)


@dataclass
class CategoryMatch:
    id: Optional[str]
    name: Optional[str]
    score: Optional[float]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "CategoryMatch":
        return cls(
            id=_opt_str(data.get("id")),
            name=_opt_str(data.get("name")),
            score=_opt_float(data.get("score")),
        )


@dataclass
class CategoryMatchResponse:
    category_info: List[CategoryMatch]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "CategoryMatchResponse":
        matches = _coerce_many(data.get("categoryInfo"), CategoryMatch)
        return cls(category_info=matches)


@dataclass
class CategoryPath:
    category_type: Optional[int]
    level: Optional[int]
    name: Optional[str]
    id: Optional[str]
    is_leaf: Optional[bool]
    parent_id: Optional[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "CategoryPath":
        return cls(
            category_type=_opt_int(data.get("categoryType")),
            level=_opt_int(data.get("level")),
            name=_opt_str(data.get("name")),
            id=_opt_str(data.get("id")),
            is_leaf=_opt_bool(data.get("isLeaf")),
            parent_id=_opt_str(data.get("parentId")),
        )


@dataclass
class RecommendCategory:
    category_path_list: List[CategoryPath]
    marketable: Optional[bool]
    category_name: Optional[str]
    category_id: Optional[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "RecommendCategory":
        path = _coerce_many(data.get("categoryPathList"), CategoryPath)
        return cls(
            category_path_list=path,
            marketable=_opt_bool(data.get("marketable")),
            category_name=_opt_str(data.get("categoryName")),
            category_id=_opt_str(data.get("categoryId")),
        )


@dataclass
class CategoryMatchV2Response:
    recommend_categories: List[RecommendCategory]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "CategoryMatchV2Response":
        categories = _coerce_many(data.get("recommendCategories"), RecommendCategory)
        return cls(recommend_categories=categories)


@dataclass
class DeliveryTimeRuleConfigItem:
    time_type: Optional[int]
    value: Optional[int]
    min: Optional[int]
    max: Optional[int]
    desc: Optional[str]
    is_default: Optional[bool]
    step_delivery_time: List[int] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "DeliveryTimeRuleConfigItem":
        return cls(
            time_type=_opt_int(data.get("timeType")),
            value=_opt_int(data.get("value")),
            min=_opt_int(data.get("min")),
            max=_opt_int(data.get("max")),
            desc=_opt_str(data.get("desc")),
            is_default=_opt_bool(data.get("isDefault")),
            step_delivery_time=[
                _int(item) for item in _sequence(data.get("stepDeliveryTime"))
            ],
        )


@dataclass
class DeliveryRule:
    seller_id: Optional[str]
    plan_info_id: Optional[str]
    whcode: Optional[str]
    category_id: Optional[str]
    logistics_mode: Optional[int]
    existing: List[DeliveryTimeRuleConfigItem] = field(default_factory=list)
    presale: List[DeliveryTimeRuleConfigItem] = field(default_factory=list)
    step_presale: List[DeliveryTimeRuleConfigItem] = field(default_factory=list)
    comment: Optional[str] = None
    must_free_return: Optional[bool] = None
    not_support_pre_sale_code: Optional[int] = None
    support_pre_sale: Optional[bool] = None
    support_step_pre_sale: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "DeliveryRule":
        return cls(
            seller_id=_opt_str(data.get("sellerId")),
            plan_info_id=_opt_str(data.get("planInfoId")),
            whcode=_opt_str(data.get("whcode")),
            category_id=_opt_str(data.get("categoryId")),
            logistics_mode=_opt_int(data.get("logisticsMode")),
            existing=_coerce_many(data.get("existing"), DeliveryTimeRuleConfigItem),
            presale=_coerce_many(data.get("presale"), DeliveryTimeRuleConfigItem),
            step_presale=_coerce_many(
                data.get("stepPresale"), DeliveryTimeRuleConfigItem
            ),
            comment=_opt_str(data.get("comment")),
            must_free_return=_opt_bool(data.get("mustFreeReturn")),
            not_support_pre_sale_code=_opt_int(data.get("notSupportPreSaleCode")),
            support_pre_sale=_opt_bool(data.get("supportPreSale")),
            support_step_pre_sale=_opt_bool(data.get("supportStepPreSale")),
        )


@dataclass
class GetDeliveryRuleResponse:
    delivery_rule_list: List[DeliveryRule]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetDeliveryRuleResponse":
        rules = _coerce_many(data.get("deliveryRuleList"), DeliveryRule)
        return cls(delivery_rule_list=rules)


@dataclass
class SellerAddressRecord:
    seller_address_record_id: Optional[int]
    contact_name: Optional[str]
    phone_area_code: Optional[str]
    phone: Optional[str]
    landline_area_code: Optional[str]
    landline_phone: Optional[str]
    landline_extension_number: Optional[str]
    country_code: Optional[str]
    province_code: Optional[str]
    city_code: Optional[str]
    county_code: Optional[str]
    town_code: Optional[str]
    country_name: Optional[str]
    province_name: Optional[str]
    city_name: Optional[str]
    county_name: Optional[str]
    town_name: Optional[str]
    address: Optional[str]
    full_address: Optional[str]
    delivery_default: Optional[str]
    aftersale_default: Optional[str]
    version: Optional[int]
    active: Optional[str]
    create_time: Optional[int]
    update_time: Optional[int]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "SellerAddressRecord":
        return cls(
            seller_address_record_id=_opt_int(data.get("sellerAddressRecordId")),
            contact_name=_opt_str(data.get("contactName")),
            phone_area_code=_opt_str(data.get("phoneAreaCode")),
            phone=_opt_str(data.get("phone")),
            landline_area_code=_opt_str(data.get("landlineAreaCode")),
            landline_phone=_opt_str(data.get("landlinePhone")),
            landline_extension_number=_opt_str(data.get("landlineExtensionNumber")),
            country_code=_opt_str(data.get("countryCode")),
            province_code=_opt_str(data.get("provinceCode")),
            city_code=_opt_str(data.get("cityCode")),
            county_code=_opt_str(data.get("countyCode")),
            town_code=_opt_str(data.get("townCode")),
            country_name=_opt_str(data.get("countryName")),
            province_name=_opt_str(data.get("provinceName")),
            city_name=_opt_str(data.get("cityName")),
            county_name=_opt_str(data.get("countyName")),
            town_name=_opt_str(data.get("townName")),
            address=_opt_str(data.get("address")),
            full_address=_opt_str(data.get("fullAddress")),
            delivery_default=_opt_str(data.get("deliveryDefault")),
            aftersale_default=_opt_str(data.get("aftersaleDefault")),
            version=_opt_int(data.get("version")),
            active=_opt_str(data.get("active")),
            create_time=_opt_int(data.get("createTime")),
            update_time=_opt_int(data.get("updateTime")),
        )


@dataclass
class GetSellerAddressRecordListResponse:
    seller_address_record_list: List[SellerAddressRecord]
    total: Optional[int]

    @classmethod
    def from_dict(
        cls, data: Mapping[str, object]
    ) -> "GetSellerAddressRecordListResponse":
        records = _coerce_many(data.get("sellerAddressRecordList"), SellerAddressRecord)
        return cls(
            seller_address_record_list=records, total=_opt_int(data.get("total"))
        )


@dataclass
class ZoneInfo:
    name: Optional[str]
    short_name: Optional[str]
    code: Optional[str]
    upper: Optional[str]
    initial_pinyin: Optional[str]
    pinyin: Optional[str]
    is_active: Optional[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "ZoneInfo":
        return cls(
            name=_opt_str(data.get("name")),
            short_name=_opt_str(data.get("shortName")),
            code=_opt_str(data.get("code")),
            upper=_opt_str(data.get("upper")),
            initial_pinyin=_opt_str(data.get("initialPinyin")),
            pinyin=_opt_str(data.get("pinyin")),
            is_active=_opt_str(data.get("isActive")),
        )


@dataclass
class CheckForbiddenKeywordResponse:
    forbidden_keywords: List[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "CheckForbiddenKeywordResponse":
        return cls(
            forbidden_keywords=[
                str(item) for item in _sequence(data.get("forbiddenKeywords"))
            ]
        )


@dataclass
class CategoryV3:
    """Category V3 entity."""

    id: Optional[str]
    name: Optional[str]
    en_name: Optional[str]
    support_size_table: Optional[bool]
    support_recommend_size_table: Optional[bool]
    support_model_try_on_size_table: Optional[bool]
    support_main_spec_image: Optional[bool]
    main_spec_id: Optional[str]
    is_leaf: Optional[bool]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "CategoryV3":
        return cls(
            id=_opt_str(data.get("id")),
            name=_opt_str(data.get("name")),
            en_name=_opt_str(data.get("enName")),
            support_size_table=_opt_bool(data.get("supportSizeTable")),
            support_recommend_size_table=_opt_bool(
                data.get("supportRecommendSizeTable")
            ),
            support_model_try_on_size_table=_opt_bool(
                data.get("supportModelTryOnSizeTable")
            ),
            support_main_spec_image=_opt_bool(data.get("supportMainSpecImage")),
            main_spec_id=_opt_str(data.get("mainSpecId")),
            is_leaf=_opt_bool(data.get("isLeaf")),
        )


@dataclass
class GetCategoriseResponse:
    """Response for getCategorise API."""

    seller_in_category_gray: Optional[bool]
    category_v3s: List[CategoryV3]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "GetCategoriseResponse":
        category_v3s = _coerce_many(data.get("categoryV3s"), CategoryV3)
        return cls(
            seller_in_category_gray=_opt_bool(data.get("sellerInCategoryGray")),
            category_v3s=category_v3s,
        )


def _opt_str(value: object) -> Optional[str]:
    if value is None:
        return None
    return str(value)


def _opt_bool(value: object) -> Optional[bool]:
    if value is None:
        return None
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


def _float(value: Any, default: float = 0.0) -> float:
    result = _opt_float(value)
    return result if result is not None else default


def _opt_mapping(value: object) -> Optional[Mapping[str, Any]]:
    if isinstance(value, MappingABC):
        return value
    return None


_ModelT = TypeVar("_ModelT", bound="_SupportsFromDict")


class _SupportsFromDict(Protocol):
    @classmethod
    def from_dict(cls: Type[_ModelT], data: Mapping[str, object]) -> _ModelT: ...


def _coerce(raw: object, model: Type[_ModelT]) -> _ModelT:
    if isinstance(raw, MappingABC):
        return model.from_dict(raw)
    raise TypeError("Expected mapping value")


def _coerce_many(raw: object, model: Type[_ModelT]) -> List[_ModelT]:
    return [_coerce(item, model) for item in _mapping_sequence(raw)]


def _mapping_sequence(raw: object) -> List[Mapping[str, object]]:
    if raw is None:
        return []
    if isinstance(raw, MappingABC):
        return [raw]
    if isinstance(raw, SequenceABC) and not isinstance(raw, (str, bytes, bytearray)):
        items: List[Mapping[str, object]] = []
        for item in raw:
            if isinstance(item, MappingABC):
                items.append(item)
        return items
    return []


def _sequence(raw: object) -> List[object]:
    if raw is None:
        return []
    if isinstance(raw, SequenceABC) and not isinstance(
        raw, (str, bytes, bytearray, MappingABC)
    ):
        return list(raw)
    return [raw]


__all__ = [
    "GetCategoriesRequest",
    "GetAttributeValuesRequest",
    "GetAttributeListRequest",
    "GetVariationsRequest",
    "GetExpressCompanyListRequest",
    "GetLogisticsListRequest",
    "GetLogisticsModeRequest",
    "GetCarriageTemplateListRequest",
    "GetCarriageTemplateRequest",
    "GetBrandRequest",
    "GetSellerKeyInfoRequest",
    "GetNestZoneRequest",
    "CategoryMatchRequest",
    "CategoryMatchV2Request",
    "BatchGetDeliveryRuleRequest",
    "GetSellerAddressRecordBySellerIdRequest",
    "GetZonesRequest",
    "CheckForbiddenKeywordRequest",
    "Category",
    "GetCategoriesResponse",
    "Attribute",
    "GetAttributeListResponse",
    "AttributeValue",
    "GetAttributeValuesResponse",
    "Variation",
    "GetVariationsResponse",
    "ExpressCompany",
    "GetExpressCompanyListResponse",
    "LogisticsPlan",
    "GetLogisticsListResponse",
    "CarriageTemplate",
    "GetCarriageTemplateListResponse",
    "GetCarriageTemplateResponse",
    "Brand",
    "GetBrandResponse",
    "LogisticMode",
    "GetLogisticsModeResponse",
    "GetSellerKeyInfoResponse",
    "ProvinceZone",
    "CityZone",
    "NestZone",
    "GetNestZoneResponse",
    "CategoryMatch",
    "CategoryMatchResponse",
    "CategoryPath",
    "RecommendCategory",
    "CategoryMatchV2Response",
    "DeliveryTimeRuleConfigItem",
    "DeliveryRule",
    "GetDeliveryRuleResponse",
    "SellerAddressRecord",
    "GetSellerAddressRecordListResponse",
    "ZoneInfo",
    "CheckForbiddenKeywordResponse",
    "CategoryV3",
    "GetCategoriseResponse",
]
