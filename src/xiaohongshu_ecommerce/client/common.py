"""通用信息查询客户端，用于小红书电商API的元数据和工具接口。"""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Mapping, Optional

from .base import SyncSubClient
from ..models import (
    BaseResponse,
    BatchGetDeliveryRuleRequest,
    CategoryMatchRequest,
    CategoryMatchResponse,
    CategoryMatchV2Request,
    CategoryMatchV2Response,
    CheckForbiddenKeywordRequest,
    CheckForbiddenKeywordResponse,
    GetAttributeListRequest,
    GetAttributeListResponse,
    GetAttributeValuesRequest,
    GetAttributeValuesResponse,
    GetBrandRequest,
    GetBrandResponse,
    GetCarriageTemplateListRequest,
    GetCarriageTemplateListResponse,
    GetCarriageTemplateRequest,
    GetCarriageTemplateResponse,
    GetCategoriesRequest,
    GetCategoriesResponse,
    GetDeliveryRuleResponse,
    GetExpressCompanyListRequest,
    GetExpressCompanyListResponse,
    GetLogisticsListRequest,
    GetLogisticsListResponse,
    GetLogisticsModeRequest,
    GetLogisticsModeResponse,
    GetNestZoneRequest,
    GetNestZoneResponse,
    GetSellerAddressRecordBySellerIdRequest,
    GetSellerAddressRecordListResponse,
    GetSellerKeyInfoRequest,
    GetSellerKeyInfoResponse,
    GetVariationsRequest,
    GetVariationsResponse,
    GetZonesRequest,
    ZoneInfo,
)


if TYPE_CHECKING:  # pragma: no cover
    pass


class CommonClient(SyncSubClient):
    """通用信息查询API的同步客户端。

    此客户端提供访问各种通用API的功能，包括类目管理、商品属性、
    物流信息、品牌信息和内容验证等基础数据服务。
    """

    def get_categories(
        self,
        category_id: Optional[str] = None,
    ) -> BaseResponse[GetCategoriesResponse]:
        """获取可售类目列表 (API: common.getCategories).

        获取可售类目列表，支持分级浏览和顶级类目列表获取。

        Args:
            category_id (Optional[str]): 父级分类,如果该参数为空，则返回所有的一级分类

        Returns:
            BaseResponse[GetCategoriesResponse]: 响应结果包含:
                - categoryV3s (List[CategoryV3]): 规格列表 包含:
                    - id (str): 分类id，用于创建商品时使用
                    - name (str): 分类中文名
                    - enName (str): 分类英文名
                    - supportSizeTable (bool): 是否支持基础尺码图
                    - supportRecommendSizeTable (bool): 是否支持尺码推荐图
                    - supportModelTryOnSizeTable (bool): 是否支持模特试穿图
                    - supportMainSpecImage (bool): 是否支持规格大图
                    - mainSpecId (str): 主规格id
                    - isLeaf (bool): 是否是叶子类目

        Example:
            ```python
            # Get top-level categories
            response = client.common.get_categories(access_token)

            # Get subcategories of a specific parent
            response = client.common.get_categories(
                access_token, category_id="52ce****8933"
            )
            ```

        Note:
            Use this API to build category hierarchies for product listing.
            Leaf categories (isLeaf=true) are required for product creation.
        """
        request = GetCategoriesRequest(category_id=category_id)
        return self._execute(request, response_model=GetCategoriesResponse)

    def get_attribute_values(
        self,
        attribute_id: str,
    ) -> BaseResponse[GetAttributeValuesResponse]:
        """由属性获取属性值 (API: common.getAttributeValues).

        根据属性ID获取该属性下的属性值列表。

        Args:
            attribute_id (str): 属性值编号

        Returns:
            BaseResponse[GetAttributeValuesResponse]: 响应结果包含:
                - attributeValueV3s (List[AttributeValueV3]): 属性值列表 包含:
                    - valueId (str): 属性编号
                    - valueName (str): 属性名

        Example:
            ```python
            response = client.common.get_attribute_values(
                access_token, attribute_id="5845***325e"
            )

            for value in response.data.attributeValueV3s:
                print(f"Value: {value.name} (ID: {value.id})")
            ```

        Note:
            This API is typically used after getting attributes from get_attribute_lists()
            to populate dropdown options for single-select and multi-select attributes.
        """
        request = GetAttributeValuesRequest(attribute_id=attribute_id)
        return self._execute(request, response_model=GetAttributeValuesResponse)

    def get_attribute_lists(
        self,
        category_id: str,
    ) -> BaseResponse[GetAttributeListResponse]:
        """由末级分类获取属性 (API: common.getAttributeLists).

        根据末级分类获取该分类下的所有属性信息。

        Args:
            category_id (str): 末级分类

        Returns:
            BaseResponse[GetAttributeListResponse]: 响应结果包含:
                - attributeV3s (List[AttributeV3]): 属性列表 包含:
                    - id (str): 属性编号
                    - isRequired (bool): 是否必填，true为必填，false为选填
                    - name (str): 属性中文名
                    - enName (str): 属性英文名
                    - acceptsImage (bool): 是否接受图片，true为是，false为否
                    - isMulti (bool): 是否多选, true为多选, false为单选
                    - inputType (int): 输入类型 0-文本 1-单选 2-多选
                    - customizable (bool): 是否可以自定义属性值（输入类型为单选、多选才有效），true为是，false为否

        Example:
            ```python
            response = client.common.get_attribute_lists(
                access_token, category_id="5845***325e"
            )

            for attr in response.data.attributeV3s:
                if attr.isRequired:
                    print(f"Required: {attr.name} (Type: {attr.inputType})")
            ```

        Note:
            Only leaf categories have attributes. Use get_categories() first to identify
            leaf categories (isLeaf=true), then call this API to get their attributes.
        """
        request = GetAttributeListRequest(category_id=category_id)
        return self._execute(request, response_model=GetAttributeListResponse)

    def get_variations(
        self,
        category_id: str,
    ) -> BaseResponse[GetVariationsResponse]:
        """由末级分类获取规格（新） (API: common.getVariations).

        根据末级分类获取该分类下的规格信息。

        Args:
            category_id (str): 末级分类

        Returns:
            BaseResponse[GetVariationsResponse]: 响应结果包含:
                - variations (List[VariationV3]): 规格列表 包含:
                    - id (str): ID
                    - name (str): 规格名
                    - enName (str): 规格英文名
                - splVariations (List[VariationV3]): 规格列表 包含相同结构

        Example:
            ```python
            response = client.common.get_variations(
                access_token, category_id="5845***325e"
            )

            print("Standard variations:")
            for variation in response.data.variations:
                print(f"- {variation.name} (ID: {variation.id})")

            print("Special variations:")
            for variation in response.data.splVariations:
                print(f"- {variation.name} (ID: {variation.id})")
            ```

        Note:
            Specifications are used to create product SKUs. Different combinations
            of specification values create different SKU variants of the same product.
        """
        request = GetVariationsRequest(category_id=category_id)
        return self._execute(request, response_model=GetVariationsResponse)

    def get_express_company_list(
        self,
    ) -> BaseResponse[GetExpressCompanyListResponse]:
        """获取快递公司信息 (API: common.getExpressCompanyList).

        获取平台支持的快递公司信息列表。

        Args:

        Returns:
            BaseResponse[GetExpressCompanyListResponse]: 响应结果包含:
                - expressCompanyInfos (List[ExpressCompanyInfo]): 物流公司信息列表 包含:
                    - expressCompanyId (int): 小红书内部定义的快递公司id
                    - expressCompanyCode (str): 快递公司编码,发货时需要传的值
                    - expressCompanyName (str): 快递公司名称
                    - comment (str): 备注

        Example:
            ```python
            response = client.common.get_express_company_list(access_token)

            for company in response.data.expressCompanyInfos:
                print(f"{company.expressCompanyName}: {company.expressCompanyCode}")
                if company.comment:
                    print(f"  Note: {company.comment}")
            ```

        Note:
            The expressCompanyCode is required when creating shipping orders.
            Store this mapping for use in order fulfillment workflows.
        """
        request = GetExpressCompanyListRequest()
        return self._execute(request, response_model=GetExpressCompanyListResponse)

    def get_logistics_list(
        self,
    ) -> BaseResponse[GetLogisticsListResponse]:
        """获取物流方案列表 (API: common.getLogisticsList).

        获取商家配置的物流方案列表。

        Args:

        Returns:
            BaseResponse[GetLogisticsListResponse]: 响应结果包含:
                - logisticsPlans (List[LogisticsPlan]): 物流方案列表 包含:
                    - planInfoId (str): 物流方案Id
                    - shopName (str): 店铺名称
                    - planInfoName (str): 物流方案名称
                    - tradeMode (int): 贸易模式 0：内贸 1：保税 2：直邮
                    - customsCode (str): 申报口岸代码
                    - logisticsCompanyCode (str): 快递公司代码
                    - logisticName (str): 物流方案名称
                    - isValid (bool): 是否有效
                    - countryName (str): 发货地国家名称
                    - privinceName (str): 发货地省份名称
                    - cityName (str): 发货地城市名称
                    - street (str): 发货地街道信息
                    - postCode (str): 发货地邮政编码
                    - sellerAddressRecordId (int): 商家地址库Id

        Example:
            ```python
            response = client.common.get_logistics_list(access_token)

            for plan in response.data.logisticsPlans:
                if plan.isValid:
                    trade_modes = {0: "内贸", 1: "保税", 2: "直邮"}
                    print(f"{plan.planInfoName} - {trade_modes.get(plan.tradeMode)}")
            ```

        Note:
            Use planInfoId when creating products to specify which logistics plan to use.
            Only plans with isValid=true should be used for new products.
        """
        request = GetLogisticsListRequest()
        return self._execute(request, response_model=GetLogisticsListResponse)

    def get_logistics_mode(
        self,
    ) -> BaseResponse[GetLogisticsModeResponse]:
        """获取物流模式列表 (API: common.logisticsMode).

        获取平台支持的物流模式列表。

        Args:

        Returns:
            BaseResponse[GetLogisticsModeResponse]: 响应结果包含:
                - logisticModes (List[LogisticsMode]): 物流模式列表 包含:
                    - logisticsCode (str): 物流模式代码
                    - logisticsTranslation (str): 物流模式名解释

        Example:
            ```python
            response = client.common.get_logistics_mode(access_token)

            for mode in response.data.logisticsModes:
                print(f"Mode {mode.id}: {mode.name}")
                if mode.description:
                    print(f"  Description: {mode.description}")
            ```

        Note:
            Logistics modes define how orders are processed and shipped.
            Use the appropriate mode ID when configuring products or processing orders.
        """
        request = GetLogisticsModeRequest()
        return self._execute(request, response_model=GetLogisticsModeResponse)

    def get_carriage_template_list(
        self,
        page_index: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> BaseResponse[GetCarriageTemplateListResponse]:
        """运费模版列表 (API: common.getCarriageTemplateList).

        获取商家的运费模板列表，支持分页查询。

        Args:
            page_index (Optional[int]): 默认返回运费模板的页数为1，限制 小于100
            page_size (Optional[int]): 默认返回20，限制 小于100

        Returns:
            BaseResponse[GetCarriageTemplateListResponse]: 响应结果包含:
                - carriageTemplateList (List[CarriageTemplate]): 运费模板列表 包含:
                    - templateId (str): 运费模板id
                    - templateName (str): 运费模板名称
                    - templateType (int): 运费模板类型 1-自定义邮费 2-卖家承担邮费
                    - costType (int): 计费类型 1-按件计费 2-按重量计费
                    - expressType (int): 快递方式(备用)
                    - supportNotDelivery (bool): 是否包含不可以配送区域
                    - notDeliveryAreas (List[str]): 不可配送区域，最细可到区级别（区对应的zonecode）
                    - enabled (bool): 是否有效
                    - syncdAt (int): 同步商品时间
                    - createBy (str): 创建人
                    - createAt (int): 创建时间 单位ms
                    - updateAt (int): 更新时间 单位ms
                - totalCount (int): 返回的运费模板总数

        Example:
            ```python
            # Get first page of templates
            response = client.common.get_carriage_template_list(
                access_token, page_index=1, page_size=20
            )

            for template in response.data.carriageTemplateList:
                type_desc = "Custom" if template.templateType == 1 else "Seller Pays"
                print(f"{template.templateName} ({type_desc})")
            ```

        Note:
            Use templateId when creating products to specify which shipping cost
            calculation template to apply. Default templates are automatically used
            if no template is specified.
        """
        request = GetCarriageTemplateListRequest(
            page_index=page_index,
            page_size=page_size,
        )
        return self._execute(request, response_model=GetCarriageTemplateListResponse)

    def get_carriage_template(
        self,
        template_id: str,
    ) -> BaseResponse[GetCarriageTemplateResponse]:
        """运费模版详情 (API: common.getCarriageTemplate).

        根据模板ID获取运费模板的详细配置信息。

        Args:
            template_id (str): 运费模板id

        Returns:
            BaseResponse[GetCarriageTemplateResponse]: 响应结果包含:
                - templateId (str): 运费模板id
                - templateName (str): 运费模板名称
                - templateType (int): 运费模板类型 1-自定义邮费 2-卖家承担邮费
                - costType (int): 计费类型 1-按件计费 2-按重量计费
                - expressType (int): 快递方式(备用)
                - supportNotDelivery (bool): 是否包含不可以配送区域
                - notDeliveryAreas (List[str]): 不可配送区域，最细可到区级别（区对应的zonecode）
                - normalConfig (object): 快递运费配置
                - enabled (bool): 是否有效
                - syncdAt (int): 同步商品时间
                - createBy (str): 创建人
                - createAt (int): 创建时间 单位ms
                - updateAt (int): 更新时间 单位ms
                - sendAddress (object): 发货地址信息

        Example:
            ```python
            response = client.common.get_carriage_template(
                access_token, template_id="601a6186095e7a0001c5fb49"
            )

            template = response.data
            print(f"Template: {template.templateName}")
            print(f"Default cost: {template.defaultCost}")
            if template.freeShippingThreshold:
                print(f"Free shipping over: {template.freeShippingThreshold}")
            ```

        Note:
            Use this API to display shipping cost details to customers or to
            understand how shipping costs will be calculated for products using
            this template.
        """
        request = GetCarriageTemplateRequest(template_id=template_id)
        return self._execute(request, response_model=GetCarriageTemplateResponse)

    def brand_search(
        self,
        category_id: str,
        keyword: Optional[str] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> BaseResponse[GetBrandResponse]:
        """获取品牌信息 (API: common.brandSearch).

        根据类目搜索品牌信息，支持关键词搜索和分页。

        Args:
            category_id (str): 末级类目id
            keyword (Optional[str]): 品牌关键字
            page_no (Optional[int]): 品牌页数, 从第一页开始,默认为1
            page_size (Optional[int]): 品牌列表每页数量，默认为20,最大20

        Returns:
            BaseResponse[GetBrandResponse]: 响应结果包含:
                - brands (List[BrandV3]): 品牌信息列表 包含:
                    - id (str): 品牌id
                    - name (str): 品牌名
                    - enName (str): 品牌英文名
                    - image (str): 品牌图片

        Example:
            ```python
            # Search for specific brand
            response = client.common.brand_search(
                access_token,
                category_id="5a31****9876",
                keyword="Charles & Keith",
                page_size=20
            )

            for brand in response.data.brands:
                print(f"{brand.name} ({brand.enName}) - ID: {brand.id}")

            # List all brands in category
            response = client.common.brand_search(
                access_token, category_id="5a31****9876"
            )
            ```

        Note:
            Brand ID is required when creating products. Use the search functionality
            to help users find and select appropriate brands for their products.
        """
        request = GetBrandRequest(
            category_id=category_id,
            keyword=keyword,
            page_no=page_no,
            page_size=page_size,
        )
        return self._execute(request, response_model=GetBrandResponse)

    def get_seller_key_info(
        self,
    ) -> BaseResponse[GetSellerKeyInfoResponse]:
        """获取老版本商家授权信息 (API: common.getSellerKeyInfo).

        获取商家在新旧授权体系中的标识信息。

        Args:

        Returns:
            BaseResponse[GetSellerKeyInfoResponse]: 响应结果包含:
                - sellerId (str): 商家id(新授权体系)
                - appKey (str): 商家Key(旧授权体系)

        Example:
            ```python
            response = client.common.get_seller_key_info(access_token)

            print(f"Seller ID (new): {response.data.sellerId}")
            print(f"App Key (legacy): {response.data.appKey}")
            ```

        Note:
            This API is primarily used for system compatibility and migration purposes.
            The sellerId is used in the new authorization system, while appKey is
            from the legacy system.
        """
        request = GetSellerKeyInfoRequest()
        return self._execute(request, response_model=GetSellerKeyInfoResponse)

    def get_nest_zone(
        self,
    ) -> BaseResponse[GetNestZoneResponse]:
        """获取地址信息 (API: common.getNestZone).

        获取分层级的行政区划信息，包括省市区三级结构。

        Args:

        Returns:
            BaseResponse[GetNestZoneResponse]: 响应结果包含:
                - provinceZoneList (List[ProvinceZone]): 省级行政区划列表 包含:
                    - id (str): 行政区划在系统中的id
                    - code (str): 行政区划代码
                    - name (str): 行政区划名称
                    - upper (str): 上一级的行政区划代码，省级行政区划的upper为1
                    - zipcode (str): 行政区划的邮政编码
                    - isDeactive (bool): 是否已停用
                    - zones (List[CityZone]): 市级行政区划列表 包含:
                        - id (str): 行政区划在系统中的id
                        - code (str): 行政区划代码
                        - name (str): 行政区划名称
                        - upper (str): 上一级的行政区划代码
                        - zipcode (str): 行政区划的邮政编码
                        - isDeactive (bool): 是否已停用
                        - zones (List[DistrictZone]): 县级行政区划列表 包含相同结构

        Example:
            ```python
            response = client.common.get_nest_zone(access_token)

            for province in response.data.provinceZoneList:
                if not province.isDeactive:
                    print(f"Province: {province.name} ({province.code})")
                    for city in province.zones:
                        if not city.isDeactive:
                            print(f"  City: {city.name} ({city.code})")
            ```

        Note:
            This API returns the complete hierarchical address structure.
            Use the codes for shipping zone configuration and address validation.
            Only use active zones (isDeactive=false) for current operations.
        """
        request = GetNestZoneRequest()
        return self._execute(request, response_model=GetNestZoneResponse)

    def category_match(
        self,
        spu_name: str,
        top_k: Optional[int] = None,
    ) -> BaseResponse[CategoryMatchResponse]:
        """商品标题类目预测 (API: common.categoryMatch).

        基于商品名称进行AI类目预测，帮助商家快速选择合适的类目。

        Args:
            spu_name (str): spu名称
            top_k (Optional[int]): 返回最符合的类目数量，默认为1

        Returns:
            BaseResponse[CategoryMatchResponse]: 响应结果包含:
                - categoryInfo (List[CategoryInfo]): 末级类目信息 包含:
                    - id (str): 类目ID
                    - name (str): 类目名称
                    - ename (str): 类目英文名

        Example:
            ```python
            # Basic category prediction
            response = client.common.category_match(
                access_token, spu_name="爱马仕手提包包"
            )

            # Get multiple predictions
            response = client.common.category_match(
                access_token,
                spu_name="爱马仕手提包包",
                top_k=3,
            )

            for category in response.data.categories:
                print(f"Category: {category.categoryName} (ID: {category.categoryId})")
                print(f"Confidence: {category.confidence:.2f}")
            ```

        Note:
            This API helps with automatic category selection during product listing.
            Higher confidence scores indicate more reliable predictions.
            Only leaf categories can be used for actual product creation.
        """
        request = CategoryMatchRequest(
            spu_name=spu_name,
            top_k=top_k,
        )
        return self._execute(request, response_model=CategoryMatchResponse)

    def category_match_v2(
        self,
        name: str,
        image_urls: List[str],
        scene: Optional[str] = None,
    ) -> BaseResponse[CategoryMatchV2Response]:
        """获取预测类目（新） (API: common.categoryMatchV2).

        基于商品名称和图片进行AI类目预测，提供更准确的预测结果。

        Args:
            name (str): 商品名称
            image_urls (List[str]): 商品图片
            scene (Optional[str]): 1:智能推断，2:智能发布，3:类目判定，默认为1

        Returns:
            BaseResponse[CategoryMatchV2Response]: 响应结果包含:
                - recommendCategories (List[RecommendedCategory]): 推荐类目列表 包含:
                    - categoryPathList (List[CategoryPath]): 类目树 包含:
                        - id (str): 类目ID
                        - name (str): 类目名称
                        - level (int): 类目层级
                        - categoryType (int): 类目类型
                        - isLeaf (bool): 是否为叶子类目
                        - parentId (str): 父类目ID
                    - marketable (bool): 商家是否可售
                    - categoryName (str): 类目名
                    - categoryId (str): 类目id

        Example:
            ```python
            response = client.common.category_match_v2(
                access_token,
                name="雅诗兰黛小棕瓶眼霜",
                scene="1",
                image_urls=[
                    "https://example.com/product1.jpg",
                    "https://example.com/product2.jpg"
                ]
            )

            for rec in response.data.recommendCategories:
                # Get the leaf category from the path
                leaf_category = next(cat for cat in rec.categoryPathList if cat.isLeaf)
                print(f"Recommended: {leaf_category.name} (ID: {leaf_category.id})")
                print(f"Confidence: {rec.confidence:.2f}")
            ```

        Note:
            This V2 API provides more accurate predictions by analyzing product images
            in addition to the product name. Use the leaf category ID for product creation.
            Higher confidence scores indicate more reliable predictions.
        """
        request = CategoryMatchV2Request(
            name=name,
            scene=scene,
            image_urls=image_urls,
        )
        return self._execute(request, response_model=CategoryMatchV2Response)

    def get_delivery_rule(
        self,
        get_delivery_rule_requests: List[dict],
    ) -> BaseResponse[GetDeliveryRuleResponse]:
        """批量获取发货时间规则 (API: common.getDeliveryRule).

        批量获取不同类目和物流方案组合的发货时间规则。

        Args:
            get_delivery_rule_requests (List[dict]): 批量查询 每项包含:
                - categoryId (str): 类目id
                - logisticsPlanId (str): 物流方案id
                - whcode (str, optional): 仓库号，自营使用
                - itemId (str, optional): 商品id

        Returns:
            BaseResponse[GetDeliveryRuleResponse]: 响应结果包含:
                - deliveryRuleList (List[DeliveryRule]): 批量查询结果 包含:
                    - sellerId (str): 商家id
                    - planInfoId (str): 物流方案id
                    - whcode (str): 仓库号，自营使用
                    - categoryId (str): 类目id
                    - logisticsMode (int): 1:内贸，2:保税，3:直邮
                    - existing (List): 现货规则，分为当日发，和指定value的几个枚举
                    - presale (List): 预售（最多只有两条规则，相对/绝对）
                    - comment (str): 备注，如果无法返回配置数据的原因
                    - mustFreeReturn (bool): 是否必须支持7天无理由
                    - supportPreSale (bool): 是否支持预售（可用预售规则）
                    - notSupportPreSaleCode (int): 不支持预售原因，1:发货时间格式不正确或不符合规则 2：该类目不支持，3：店铺分过低不支持预售
                    - stepPresale (List): 阶梯预售规则
                    - supportStepPreSale (bool): 是否支持阶梯预售

        Example:
            ```python
            delivery_requests = [
                {
                    "categoryId": "5845***325e",
                    "logisticsPlanId": "601a****fb4b"
                },
                {
                    "categoryId": "5a31****9876",
                    "logisticsPlanId": "601a****fb4b",
                    "whcode": "WH001"
                }
            ]
            response = client.common.get_delivery_rule(
                access_token, get_delivery_rule_requests=delivery_requests
            )

            for rule in response.data.deliveryRules:
                if rule.isValid:
                    print(f"Category {rule.categoryId}: {rule.minDeliveryDays}-{rule.maxDeliveryDays} days")
            ```

        Note:
            Use this API to display accurate delivery timeframes to customers.
            Only use rules with isValid=true for current delivery estimates.
        """
        queries = [
            BatchGetDeliveryRuleRequest.DeliveryRuleQuery(
                whcode=req.get("whcode"),
                logistics_plan_id=req.get("logisticsPlanId"),
                category_id=req.get("categoryId"),
                item_id=req.get("itemId"),
            )
            for req in get_delivery_rule_requests
        ]
        request = BatchGetDeliveryRuleRequest(queries=queries)
        return self._execute(request, response_model=GetDeliveryRuleResponse)

    def get_address_record(
        self,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> BaseResponse[GetSellerAddressRecordListResponse]:
        """获取商家地址库 (API: common.getAddressRecord).

        获取商家保存的地址库信息，支持分页查询。

        Args:
            page_no (Optional[int]): 默认返回商家收货地址的页数为1，限制 小于100
            page_size (Optional[int]): 默认返回20，限制 小于200

        Returns:
            BaseResponse[GetSellerAddressRecordListResponse]: 响应结果包含:
                - sellerAddressRecordList (List[SellerAddressRecord]): 商家地址列表 包含:
                    - sellerAddressRecordId (int): 商家地址id
                    - contactName (str): 联系人
                    - phoneAreaCode (str): 手机区号
                    - phone (str): 手机号
                    - landlineAreaCode (str): 座机区号
                    - landlinePhone (str): 座机号
                    - landlineExtensionNumber (str): 分机号
                    - countryCode (str): 国家代码
                    - provinceCode (str): 省代码
                    - cityCode (str): 市代码
                    - countyCode (str): 区/县代码
                    - townCode (str): 镇/街道代码
                    - countryName (str): 国家名称
                    - provinceName (str): 省名称
                    - cityName (str): 市名称
                    - countyName (str): 区/县名称
                    - townName (str): 镇/街道名称
                    - address (str): 详细地址
                    - fullAddress (str): 完整地址
                    - deliveryDefault (str): 是否发货默认 NON_DEFAULT-非默认; DEFAULT-默认
                    - aftersaleDefault (str): 是否售后默认 NON_DEFAULT-非默认; DEFAULT-默认
                    - version (int): 版本号
                    - active (str): 是否生效 ACTIVE-生效; INACTIVE-无效
                    - createTime (int): 创建时间
                    - updateTime (int): 更新时间
                - total (int): 返回的商家地址总数

        Example:
            ```python
            response = client.common.get_address_record(
                access_token, page_size=50
            )

            for address in response.data.addressRecords:
                print(f"{address.name}: {address.province} {address.city} {address.district}")
                print(f"  Contact: {address.contactPerson} - {address.contactPhone}")
                if address.isDefault:
                    print("  [DEFAULT ADDRESS]")
            ```

        Note:
            Use these addresses for configuring shipping origins or as templates
            for order fulfillment. Default addresses are automatically used when
            no specific address is provided.
        """
        request = GetSellerAddressRecordBySellerIdRequest(
            page_index=page_no,
            page_size=page_size,
        )
        return self._execute(request, response_model=GetSellerAddressRecordListResponse)

    def get_zones(
        self,
        code: Optional[str] = None,
        name: Optional[str] = None,
        upper: Optional[str] = None,
        filter_non_continental: Optional[bool] = None,
    ) -> BaseResponse[List[ZoneInfo]]:
        """获取地址信息（新） (API: common.getZones).

        获取行政区域信息，支持多种筛选条件。

        Args:
            code (Optional[str]): 行政区域代码
            name (Optional[str]): 行政区域名称
            upper (Optional[str]): 上一级行政区域
            filter_non_continental (Optional[bool]): 是否过滤非大陆行政区域

        Returns:
            BaseResponse[List[ZoneInfo]]: 响应结果包含ZoneInfo列表:
                - name (str): 行政区域名称
                - shortName (str): 行政区域简称
                - code (str): 行政区域代码
                - upper (str): 上一级行政区域代码
                - initialPinyin (str): 行政区域名称拼音首字母
                - pinyin (str): 行政区域名称拼音
                - isActive (str): 是否有效，ACTIVE-有效；INACTIVE-无效

        Example:
            ```python
            # Get all provinces
            response = client.common.get_zones(
                access_token, upper="1", filter_non_continental=True
            )

            # Search by name
            response = client.common.get_zones(
                access_token, name="北京"
            )

            # Get specific zone by code
            response = client.common.get_zones(
                access_token, code="110100"
            )

            for zone in response.data:
                level_names = {1: "Province", 2: "City", 3: "District"}
                print(f"{level_names.get(zone.level, 'Zone')}: {zone.name} ({zone.code})")
            ```

        Note:
            This is the newer version of address information API with enhanced
            filtering capabilities. Use filterNonContinental=True to exclude
            Hong Kong, Macau, and Taiwan if needed for mainland-only operations.
        """
        request = GetZonesRequest(
            code=code,
            name=name,
            upper=upper,
            filter_non_continental=filter_non_continental,
        )
        response = self._execute(request)
        if response.success and isinstance(response.data, list):
            response.data = [
                ZoneInfo.from_dict(item) if isinstance(item, Mapping) else item
                for item in response.data
            ]
        return response

    def check_forbidden_keyword(
        self,
        text: str,
    ) -> BaseResponse[CheckForbiddenKeywordResponse]:
        """判断文本中是否含有违禁词 (API: common.checkForbiddenKeyword).

        检查文本内容是否包含平台禁止使用的违禁词汇。

        Args:
            text (str): 文本

        Returns:
            BaseResponse[CheckForbiddenKeywordResponse]: 响应结果包含:
                - forbiddenKeywords (List[str]): 违禁词列表，为空表示无违禁词

        Example:
            ```python
            # Check product title
            response = client.common.check_forbidden_keyword(
                access_token,
                text="这是一个标题包含违禁词防脱发"
            )

            if response.data.hasForbiddenKeyword:
                print("Forbidden keywords detected:")
                for keyword in response.data.forbiddenKeywords:
                    print(f"- {keyword}")

                if response.data.suggestions:
                    print("Suggested alternatives:")
                    for suggestion in response.data.suggestions:
                        print(f"- {suggestion}")
            else:
                print("Text is compliant - no forbidden keywords found")

            # Check multiple texts before product creation
            texts_to_check = [product_title, product_description, product_tags]
            for text in texts_to_check:
                response = client.common.check_forbidden_keyword(
                    access_token, text=text
                )
                if response.data.hasForbiddenKeyword:
                    print(f"Issues found in: {text[:50]}...")
            ```

        Note:
            Always check product titles, descriptions, and other content before
            submission to avoid content policy violations. Use the suggested
            alternatives when forbidden keywords are detected.
        """
        request = CheckForbiddenKeywordRequest(text=text)
        return self._execute(request, response_model=CheckForbiddenKeywordResponse)
