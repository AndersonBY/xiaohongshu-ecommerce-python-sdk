"""商品客户端实现。"""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from .base import SyncSubClient
from ..models import (
    BaseItemResponse,
    CreateItemAndSkuRequest,
    CreateItemRequest,
    CreateItemV3Request,
    CreateSkuV3Request,
    CreateSpuRequest,
    DeleteItemRequest,
    DeleteItemV3Request,
    DeleteSkuV3Request,
    DeleteSpuRequest,
    DeleteSpuResponse,
    GetBasicItemListRequest,
    GetBasicItemListResponse,
    GetBasicSpuRequest,
    GetBasicSpuResponse,
    GetDetailItemListRequest,
    GetDetailItemListResponse,
    GetDetailSkuListRequest,
    GetItemInfoRequest,
    GetSpuInfoRequest,
    GetSpuInfoResponse,
    ItemAndSkuDetail,
    ItemDetail,
    ItemDetailV3,
    SearchItemListRequest,
    SkuDetail,
    SpuOperationResponse,
    UpdateAvailabilityRequest,
    UpdateItemAndSkuRequest,
    UpdateItemImageRequest,
    UpdateItemPriceRequest,
    UpdateItemRequest,
    UpdateItemV3Request,
    UpdateLogisticsPlanRequest,
    UpdateSkuAvailableRequest,
    UpdateSkuLogisticsPlanRequest,
    UpdateSkuPriceRequest,
    UpdateSkuV3Request,
    UpdateSpuImageRequest,
    UpdateSpuRequest,
    UpdateVariantImageRequest,
)

if TYPE_CHECKING:  # pragma: no cover
    from ..models import BaseResponse


class ProductClient(SyncSubClient):
    """商品管理接口的同步访问客户端。"""

    def get_basic_item_list(
        self,
        item_id: Optional[str] = None,
        status: Optional[int] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        last_id: Optional[str] = None,
    ) -> "BaseResponse[GetBasicItemListResponse]":
        """获取商品基础列表 (API: product.getBasicItemList).

        获取商品基础信息列表，支持可选筛选条件。
        此API提供基础商品详情，不包含完整SKU信息。

        Args:
            item_id (Optional[str]): 商品ID筛选条件
            status (Optional[int]): 商品状态筛选
            page_no (Optional[int]): 页码，从1开始
            page_size (Optional[int]): 页大小，最大100
            last_id (Optional[str]): 分页查询的最后ID

        Returns:
            BaseResponse[GetBasicItemListResponse]: 响应包含:
                - currentPage (int): 当前页码
                - pageSize (int): 页大小
                - total (int): 商品总数
                - itemDetailV3s (List[ItemDetailV3]): 基础商品详情列表

        Note:
            此功能用于获取基础商品列表，不包含详细SKU信息。
            如需完整的商品信息和SKU详情，请使用get_detail_sku_list()。
        """
        request = GetBasicItemListRequest(
            item_id=item_id,
            status=status,
            page_no=page_no,
            page_size=page_size,
            last_id=last_id,
        )
        return self._execute(request, response_model=GetBasicItemListResponse)

    def get_detail_item_list(
        self,
        item_ids: Optional[List[str]] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> "BaseResponse[GetDetailItemListResponse]":
        """获取商品详细列表 (API: product.getDetailItemList).

        获取包含全面数据的详细商品信息列表。
        此API提供完整的商品详情，包括属性和配置信息。

        Args:
            item_ids (Optional[List[str]]): 要筛选的商品ID列表
            page_no (Optional[int]): 页码，从1开始
            page_size (Optional[int]): 页大小，最大100

        Returns:
            BaseResponse[GetDetailItemListResponse]: 响应包含:
                - data (List[ItemDetailV3]): 详细商品信息列表
                - 分页元数据

        Note:
            此功能相比get_basic_item_list()提供更详细的商品信息。
            用于获取完整的商品元数据和配置详情。
        """
        request = GetDetailItemListRequest(
            item_ids=item_ids or [],
            page_no=page_no,
            page_size=page_size,
        )
        return self._execute(request, response_model=GetDetailItemListResponse)

    def get_detail_sku_list(
        self,
        id: Optional[str] = None,
        create_time_from: Optional[int] = None,
        create_time_to: Optional[int] = None,
        update_time_from: Optional[int] = None,
        update_time_to: Optional[int] = None,
        buyable: Optional[bool] = None,
        stock_gte: Optional[int] = None,
        stock_lte: Optional[int] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        barcode: Optional[str] = None,
        sc_sku_code: Optional[str] = None,
        single_pack_only: Optional[bool] = None,
        last_id: Optional[str] = None,
        is_channel: Optional[bool] = None,
    ) -> "BaseResponse[dict]":
        """商品列表完整版（新）(API: product.getDetailSkuList).

        获取包含完整SKU信息的商品列表，提供最全面的商品信息，
        包括库存、价格、物流和规格等详细信息。

        Args:
            id (Optional[str]): 商品编号，使用id查询其他条件可以不填.
            create_time_from (Optional[int]): 商品创建时间开始时间，Unix-Time时间戳.
            create_time_to (Optional[int]): 商品创建时间结束时间，Unix-Time时间戳.
            update_time_from (Optional[int]): 商品更新时间开始时间，Unix-Time时间戳.
            update_time_to (Optional[int]): 商品更新时间结束时间，Unix-Time时间戳.
            buyable (Optional[bool]): 是否在架上.
            stock_gte (Optional[int]): 库存大于等于某数.
            stock_lte (Optional[int]): 库存小于等于某数.
            page_no (Optional[int]): 返回页码 默认 1，页码从 1 开始 PS：当前采用分页返回，数量和页数会一起传，如果不传，则采用 默认值.
            page_size (Optional[int]): 返回数量，默认50最大100.
            barcode (Optional[str]): 商品条码.
            sc_sku_code (Optional[str]): 小红书编码,即将废弃.
            single_pack_only (Optional[bool]): 只返回单品类型的商品.
            last_id (Optional[str]): 查询起始商品id，全店商品时间倒序.
            is_channel (Optional[bool]): 不传返回全部，传true只返回渠道商品，传false只返回非渠道商品.

        Returns:
            BaseResponse[dict]: Response containing:
                - data (List[ProductV3]): 商品列表 with:
                    - item (ItemDetailV3): item列表 including:
                        - id (str): itemId,创建时不填，删除更新必填
                        - name (str): item标题
                        - ename (str): item英文名
                        - brandId (int): 品牌ID,目前查询品牌返回均为String但是是数字可以强转成Long使用
                        - categoryId (str): 末级商品类目ID,根据common.getCategories获取
                        - attributes (List): item属性，根据common.getAttributeLists和common.getAttributeValues获取，必填属性必填，无必填属性可不填
                        - images (List[str]): 商品主图(必传)
                        - imageDescriptions (List[str]): 商品详情描述图片
                        - shippingTemplateId (str): 运费模板ID，根据common.getCarriageTemplateList获取
                        - createTime (int): item创建时间
                        - updateTime (int): item更新时间
                    - sku (SkuDetailNew): SKU详细信息 including:
                        - id (str): skuId
                        - itemId (str): itemId
                        - price (int): 售价，单位分，要求小于市场价，上限10w元，即10000000分
                        - originalPrice (int): 市场价，单位分
                        - stock (int): 库存
                        - variants (List): 规格列表，根据item定义对规格填写具体规格值，item没有则不填
                        - logisticsPlanId (str): 物流方案Id，通过common.getLogisticsList获取
                        - deliveryTime (DeliveryTimeV3): 发货时间信息
                        - buyable (bool): 是否在架上，仅用于返回
                        - scSkucode (str): scSkuCode编号,小红书编码,即将废弃
                        - barcode (str): 商品条形码，创建特定品类必填
                        - createTime (int): 商品创建时间，仅返回使用
                        - updateTime (int): 商品更新时间，仅返回使用
                - pageNO (int): 页码
                - pageSize (int): 页大小
                - total (int): 总数

        Examples:
            >>> # Get all products with pagination
            >>> response = client.product.get_detail_sku_list(
            ...     access_token, page_no=1, page_size=50
            ... )

            >>> # Get specific product by ID
            >>> response = client.product.get_detail_sku_list(
            ...     access_token, id="607***450"
            ... )

            >>> # Filter by stock levels
            >>> response = client.product.get_detail_sku_list(
            ...     access_token, stock_gte=10, stock_lte=100, buyable=True
            ... )

        Note:
            This is the most comprehensive product listing API. scSkucode字段即将废弃，请使用id字段。
            价格以分为单位返回 (例如：8000 = 80.00 元)。
        """
        request = GetDetailSkuListRequest(
            id=id,
            create_time_from=create_time_from,
            create_time_to=create_time_to,
            update_time_from=update_time_from,
            update_time_to=update_time_to,
            buyable=buyable,
            stock_gte=stock_gte,
            stock_lte=stock_lte,
            page_no=page_no,
            page_size=page_size,
            barcode=barcode,
            sc_sku_code=sc_sku_code,
            single_pack_only=single_pack_only,
            last_id=last_id,
            is_channel=is_channel,
        )
        return self._execute(request)

    def get_spu_info(
        self,
        spu_id: str,
    ) -> "BaseResponse[GetSpuInfoResponse]":
        """获取SPU信息 (API: product.getSpuInfo).

        获取特定SPU的详细信息，SPU代表可以有多个变体(商品)的
        标准化产品单元。

        Args:
            spu_id (str): 要获取信息的SPU ID

        Returns:
            BaseResponse[GetSpuInfoResponse]: 响应包含:
                - SPU详细信息，包括基础属性
                - 关联的商品和变体
                - 创建和更新时间戳

        Note:
            SPU代表定义跨产品变体共享通用属性的产品模板。
            用于产品目录管理。
        """
        request = GetSpuInfoRequest(spu_id=spu_id)
        return self._execute(request, response_model=GetSpuInfoResponse)

    def get_basic_spu(
        self,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        spu_ids: Optional[List[str]] = None,
        extra: Optional[dict] = None,
    ) -> "BaseResponse[GetBasicSpuResponse]":
        """获取基础SPU列表 (API: product.getBasicSpu).

        获取带有可选筛选的基础SPU信息列表。
        SPU代表可以有多个变体的标准化产品实体。

        Args:
            page_no (Optional[int]): 页码，从1开始
            page_size (Optional[int]): 分页的页大小
            spu_ids (Optional[List[str]]): 要筛选的SPU ID列表
            extra (Optional[dict]): SPU搜索的附加筛选参数

        Returns:
            BaseResponse[GetBasicSpuResponse]: 响应包含:
                - 基础SPU信息列表
                - 分页元数据

        Note:
            用于基础SPU目录浏览和选择。
            如需详细SPU信息，请使用get_spu_info()。
        """
        request = GetBasicSpuRequest(
            page_no=page_no,
            page_size=page_size,
            spu_ids=spu_ids or [],
            extra=extra or {},
        )
        return self._execute(request, response_model=GetBasicSpuResponse)

    def get_item_info(
        self,
        item_id: Optional[str] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> "BaseResponse[dict]":
        """查询Item详情 (API: product.getItemInfo).

        获取特定商品的详细信息，包括所有关联的SKU和详细规格信息。

        Args:
            item_id (Optional[str]): itemid.
            page_no (Optional[int]): 页码大小.
            page_size (Optional[int]): 当前页码.

        Returns:
            BaseResponse[dict]: Response containing:
                - itemInfo (ItemDetailV3): item列表 including:
                    - id (str): itemId,创建时不填，删除更新必填
                    - name (str): item标题
                    - brandId (int): 品牌ID,目前查询品牌返回均为String但是是数字可以强转成Long使用
                    - categoryId (str): 末级商品类目ID,根据common.getCategories获取
                    - attributes (List): item属性，根据common.getAttributeLists和common.getAttributeValues获取，必填属性必填，无必填属性可不填
                    - images (List[str]): 商品主图(必传)
                    - imageDescriptions (List[str]): 商品详情描述图片
                    - shippingTemplateId (str): 运费模板ID，根据common.getCarriageTemplateList获取
                    - variants specifications and other metadata
                - skuInfos (List[SkuDetailNew]): sku列表 with:
                    - Complete SKU details including pricing, inventory
                    - Variant specifications
                    - Logistics configuration
                - total (int): sku数量
                - pageNO (int): 页码
                - pageSize (int): 页大小

        Examples:
            >>> # Get item with all SKUs
            >>> response = client.product.get_item_info(
            ...     access_token, item_id="64******412f1f"
            ... )

            >>> # Get item with paginated SKUs
            >>> response = client.product.get_item_info(
            ...     access_token, item_id="64******412f1f", page_no=1, page_size=10
            ... )

        Note:
            此API提供完整的商品信息，包括所有关联的SKU。
            当需要特定商品的完整详情时使用此API。
        """
        request = GetItemInfoRequest(
            item_id=item_id,
            page_no=page_no,
            page_size=page_size,
        )
        return self._execute(request)

    def search_item_list(
        self,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        search_param: Optional[dict] = None,
    ) -> "BaseResponse[dict]":
        """查询Item列表 (API: product.searchItemList).

        根据各种条件搜索和检索商品列表，包括关键词、类目、状态等高级筛选。

        Args:
            page_no (Optional[int]): 页码.
            page_size (Optional[int]): 页大小.
            search_param (Optional[dict]): 查询条件 including:
                - keyword (str, optional): 商品名称关键词
                - topCategoryIds (List[str], optional): 一级品类
                - lvl2CategoryIds (List[str], optional): 二级品类
                - lvl3CategoryIds (List[str], optional): 三级品类
                - lvl4CategoryIds (List[str], optional): 四级品类
                - buyable (bool, optional): 在架状态
                - keywords (List[str], optional): 小红书编码/条形码/商品ID/SPUID/货号
                - logisticsPlanIds (List[str], optional): 商品物流方案ID
                - createTimeFrom (int, optional): 商品创建时间大于
                - createTimeTo (int, optional): 商品创建时间小于
                - lastId (str, optional): 查询起始itemId，全店item按照时间倒序

        Returns:
            BaseResponse[dict]: Response containing:
                - currentPage (int): 当前页码
                - pageSize (int): 页大小
                - total (int): item总数
                - itemDetailV3s (List[ItemDetailV3]): item列表 with:
                    - Complete item details including attributes
                    - Product images and descriptions
                    - Category and brand information
                    - Shipping and logistics configuration

        Examples:
            >>> # Search by keyword
            >>> search_param = {"keyword": "lipstick"}
            >>> response = client.product.search_item_list(
            ...     access_token, page_no=1, page_size=20, search_param=search_param
            ... )

            >>> # Search by category and status
            >>> search_param = {
            ...     "topCategoryIds": ["cat123"],
            ...     "buyable": True
            ... }
            >>> response = client.product.search_item_list(
            ...     access_token, page_no=1, page_size=50, search_param=search_param
            ... )

            >>> # Search by multiple identifiers
            >>> search_param = {
            ...     "keywords": ["XHS123", "690123456789", "ITEM001"]
            ... }
            >>> response = client.product.search_item_list(
            ...     access_token, page_no=1, page_size=30, search_param=search_param
            ... )

        Note:
            此API提供灵活的商品搜索功能。
            使用lastId参数可以高效地进行基于时间的大数据集分页。
            keywords字段支持多种标识符类型的灵活搜索。
        """
        request = SearchItemListRequest(
            page_no=page_no,
            page_size=page_size,
            search_param=search_param or {},
        )
        return self._execute(request)

    def update_logistics_plan(
        self,
        item_id: str,
        logistics_plan_id: str,
    ) -> "BaseResponse[BaseItemResponse]":
        """更新物流方案 (API: product.updateSkuLogisticsPlan).

        更新特定SKU的物流方案配置，影响商品的运输方式和配送选项。

        Args:
            item_id (str): skuId.
            logistics_plan_id (str): wuliufanganid.

        Returns:
            BaseResponse[BaseItemResponse]: Response indicating success/failure:
                - error_code (int): 错误码
                - success (bool): 是否成功
                - data (object): 返回信息

        Examples:
            >>> # Update logistics plan for a SKU
            >>> response = client.product.update_logistics_plan(
            ...     access_token, item_id="6123**5132", logistics_plan_id="5e37***a9f0"
            ... )

        Note:
            物流方案ID可通过common.getLogisticsList API获取。
            此操作仅更新物流配置，不影响其他SKU属性。
        """
        request = UpdateLogisticsPlanRequest(
            item_id=item_id,
            logistics_plan_id=logistics_plan_id,
        )
        return self._execute(request, response_model=BaseItemResponse)

    def update_availability(
        self,
        item_id: str,
        available: bool,
    ) -> "BaseResponse[BaseItemResponse]":
        """商品上下架 (API: product.updateSkuAvailable).

        通过更新商品的上架状态来控制SKU是否可以购买。
        这是商家上架或下架商品的意愿。

        Args:
            item_id (str): skuId.
            available (bool): 商家上架意愿.

        Returns:
            BaseResponse[BaseItemResponse]: Response indicating success/failure:
                - error_code (int): 错误码
                - success (bool): 是否成功
                - data (object): 返回信息

        Examples:
            >>> # Put product on shelf
            >>> response = client.product.update_availability(
            ...     access_token,
            ...     item_id="6123**5132",
            ...     available=True
            ... )

            >>> # Take product off shelf
            >>> response = client.product.update_availability(
            ...     access_token,
            ...     item_id="6123**5132",
            ...     available=False
            ... )

        Note:
            这控制商家上架意愿。实际的可购买状态可能还取决于库存水平和平台政策等其他因素。
        """
        request = UpdateAvailabilityRequest(item_id=item_id, available=available)
        return self._execute(request, response_model=BaseItemResponse)

    def create_spu(
        self,
        spu: dict,
    ) -> "BaseResponse[SpuOperationResponse]":
        """创建SPU (API: product.createSpu).

        创建新的SPU，作为产品变体的模板。
        SPU定义跨多个产品商品共享的通用属性。

        Args:
            spu (dict): SPU基础信息和属性，包括:
                - 类目和品牌关联
                - 模板配置

        Returns:
            BaseResponse[SpuOperationResponse]: 响应包含:
                - 已创建的SPU信息
                - 用于后续操作的SPU ID
                - 操作状态

        Note:
            SPU充当产品模板。创建SPU后，
            您可以基于它创建多个商品和SKU。
        """
        request = CreateSpuRequest(spu=spu)
        return self._execute(request, response_model=SpuOperationResponse)

    def update_spu(
        self,
        spu_id: str,
        updates: dict,
    ) -> "BaseResponse[SpuOperationResponse]":
        """更新SPU (API: product.updateSpu).

        更新SPU信息，包括属性、类目关联
        和模板配置。

        Args:
            spu_id (str): 要更新的SPU ID
            updates (dict): 更新的SPU信息和属性，包括:
                - 修改的配置

        Returns:
            BaseResponse[SpuOperationResponse]: 响应包含:
                - 更新后的SPU信息
                - 操作状态

        Note:
            更新SPU可能会影响所有关联的商品和SKU。
            确保与现有产品变体的兼容性。
        """
        request = UpdateSpuRequest(spu_id=spu_id, updates=updates)
        return self._execute(request, response_model=SpuOperationResponse)

    def delete_spu(
        self,
        spu_ids: List[str],
    ) -> "BaseResponse[DeleteSpuResponse]":
        """删除SPU (API: product.deleteSpu).

        永久删除SPU及其所有关联的商品和SKU。
        此操作无法撤销。

        Args:
            spu_ids (List[str]): 要删除的SPU ID列表

        Returns:
            BaseResponse[DeleteSpuResponse]: 响应包含:
                - 删除确认
                - 操作状态

        Warning:
            此操作将永久删除SPU和所有关联产品。
            请确保这是预期的操作后再执行。

        Note:
            与SPU关联的所有商品和SKU也将被删除。
            考虑将产品更新到不同的SPU而不是删除。
        """
        request = DeleteSpuRequest(spu_ids=spu_ids)
        return self._execute(request, response_model=DeleteSpuResponse)

    def create_item(
        self,
        spu_id: str,
        price: Optional[float] = None,
        original_price: Optional[float] = None,
        stock: Optional[int] = None,
        logistics_plan_id: Optional[str] = None,
        variants: Optional[List[dict]] = None,
        delivery_time: Optional[dict] = None,
        extra: Optional[dict] = None,
    ) -> "BaseResponse[ItemDetail]":
        """创建商品 (API: product.createItem).

        创建包含完整规格的新商品，包括
        属性、图片、描述和变体配置。

        Args:
            spu_id (str): 关联的SPU ID
            price (Optional[float]): 售价
            original_price (Optional[float]): 市场价
            stock (Optional[int]): 初始库存数量
            logistics_plan_id (Optional[str]): 物流方案ID
            variants (Optional[List[dict]]): 产品变体配置
            delivery_time (Optional[dict]): 发货时间配置
            extra (Optional[dict]): 额外的商品规格

        Returns:
            BaseResponse[ItemDetail]: 响应包含:
                - 带有分配ID的已创建商品信息
                - 完整的商品配置
                - 创建时间戳

        Note:
            创建商品后，您需要创建关联的SKU
            用于库存和价格管理。使用create_sku功能。
        """
        request = CreateItemRequest(
            spu_id=spu_id,
            price=price,
            original_price=original_price,
            stock=stock,
            logistics_plan_id=logistics_plan_id,
            variants=variants or [],
            delivery_time=delivery_time or {},
            extra=extra or {},
        )
        return self._execute(request, response_model=ItemDetail)

    def update_item(
        self,
        item_id: str,
        name: Optional[str] = None,
        ename: Optional[str] = None,
        brand_id: Optional[int] = None,
        category_id: Optional[str] = None,
        attributes: Optional[List[dict]] = None,
        images: Optional[List[str]] = None,
        image_descriptions: Optional[List[str]] = None,
        shipping_template_id: Optional[str] = None,
        extra: Optional[dict] = None,
    ) -> "BaseResponse[ItemDetail]":
        """更新商品 (API: product.updateItem).

        更新商品信息，包括标题、属性、图片、
        描述和其他规格。

        Args:
            item_id (str): 要更新的商品ID
            name (Optional[str]): 更新的商品标题
            ename (Optional[str]): 更新的英文商品名称
            brand_id (Optional[int]): 更新的品牌ID
            category_id (Optional[str]): 更新的类目ID
            attributes (Optional[List[dict]]): 更新的商品属性
            images (Optional[List[str]]): 更新的商品主图
            image_descriptions (Optional[List[str]]): 更新的详情描述图片
            shipping_template_id (Optional[str]): 更新的运费模板ID
            extra (Optional[dict]): 额外的商品规格

        Returns:
            BaseResponse[ItemDetail]: 响应包含:
                - 更新的商品信息
                - 修改时间戳

        Note:
            更新商品会影响其显示和规格，但
            不会直接修改关联的SKU价格或库存。
        """
        request = UpdateItemRequest(
            item_id=item_id,
            name=name,
            ename=ename,
            brand_id=brand_id,
            category_id=category_id,
            attributes=attributes or [],
            images=images or [],
            image_descriptions=image_descriptions or [],
            shipping_template_id=shipping_template_id,
            extra=extra or {},
        )
        return self._execute(request, response_model=ItemDetail)

    def delete_item(
        self,
        item_id: str,
    ) -> "BaseResponse[str]":
        """删除商品 (API: product.deleteItem).

        永久删除商品及其所有关联的SKU。
        此操作无法撤销。

        Args:
            item_id (str): 要删除的商品ID

        Returns:
            BaseResponse[str]: 响应包含:
                - 删除确认消息
                - 操作状态

        Warning:
            此操作将永久删除商品和所有关联的SKU。
            请确保这是预期的操作后再执行。

        Note:
            与商品关联的所有SKU也将被删除。
            如果您以后可能需要恢复，请考虑下架商品而不是删除。
        """
        request = DeleteItemRequest(item_id=item_id)
        return self._execute(request)

    def create_item_v2(
        self,
        name: str,
        brand_id: int,
        category_id: str,
        attributes: List[dict],
        images: List[str],
        image_descriptions: List[str],
        shipping_template_id: str,
        ename: Optional[str] = None,
        shipping_gross_weight: Optional[int] = None,
        variant_ids: Optional[List[str]] = None,
        video_url: Optional[str] = None,
        article_no: Optional[str] = None,
        transparent_image: Optional[str] = None,
        description: Optional[str] = None,
        faq: Optional[List[dict]] = None,
        delivery_mode: Optional[int] = None,
        free_return: Optional[int] = None,
        enable_multi_warehouse: Optional[bool] = None,
        size_table_image: Optional[str] = None,
        recommend_size_table_image: Optional[str] = None,
        model_try_on_size_table_image: Optional[str] = None,
        enable_main_spec_image: Optional[bool] = None,
        item_short_title: Optional[str] = None,
    ) -> "BaseResponse[ItemDetailV3]":
        """使用V2 API创建商品 (API: product.createItemV2) - 即将废弃.

        使用V2 API格式创建新商品。此API提供
        增强的商品创建功能和额外的配置选项。

        Args:
            name (str): 商品标题 (必填)
            brand_id (int): 品牌ID (必填)
            category_id (str): 类目ID (必填)
            attributes (List[dict]): 商品属性 (必填)
            images (List[str]): 商品主图 (必填)
            image_descriptions (List[str]): 详情描述图片 (必填)
            shipping_template_id (str): 运费模板ID (必填)
            ename (Optional[str]): 英文商品名称
            shipping_gross_weight (Optional[int]): 商品重量（克）
            variant_ids (Optional[List[str]]): 变体类型定义
            video_url (Optional[str]): 主图视频
            article_no (Optional[str]): 商品货号
            transparent_image (Optional[str]): 透明背景图片
            description (Optional[str]): 商品描述（最多500字）
            faq (Optional[List[dict]]): 常见问题
            delivery_mode (Optional[int]): 物流模式（0=普通，1=无物流）
            free_return (Optional[int]): 7天退货支持（1=是，2=否）
            enable_multi_warehouse (Optional[bool]): 启用多仓
            size_table_image (Optional[str]): 基础尺码表图片
            recommend_size_table_image (Optional[str]): 推荐尺码表
            model_try_on_size_table_image (Optional[str]): 模特试穿表
            enable_main_spec_image (Optional[bool]): 启用主规格图片
            item_short_title (Optional[str]): 短标题（6-12个汉字）

        Returns:
            BaseResponse[ItemDetailV3]: 响应包含:
                - 带有分配ID的完整商品详情
                - 所有配置设置
                - 创建和更新时间戳

        Note:
            此API标记为即将废弃。考虑使用较新的商品创建API
            或create_item_and_sku进行组合商品+SKU创建。
        """
        request = CreateItemV3Request(
            name=name,
            brand_id=brand_id,
            category_id=category_id,
            attributes=attributes,
            images=images,
            image_descriptions=image_descriptions,
            shipping_template_id=shipping_template_id,
            ename=ename,
            shipping_gross_weight=shipping_gross_weight,
            variant_ids=variant_ids or [],
            video_url=video_url,
            article_no=article_no,
            transparent_image=transparent_image,
            description=description,
            faq=faq or [],
            delivery_mode=delivery_mode,
            free_return=free_return,
            enable_multi_warehouse=enable_multi_warehouse,
            size_table_image=size_table_image,
            recommend_size_table_image=recommend_size_table_image,
            model_try_on_size_table_image=model_try_on_size_table_image,
            enable_main_spec_image=enable_main_spec_image,
            item_short_title=item_short_title,
        )
        return self._execute(request, response_model=ItemDetailV3)

    def update_item_v2(
        self,
        item_id: str,
        name: Optional[str] = None,
        brand_id: Optional[int] = None,
        category_id: Optional[str] = None,
        attributes: Optional[List[dict]] = None,
        images: Optional[List[str]] = None,
        image_descriptions: Optional[List[str]] = None,
        shipping_template_id: Optional[str] = None,
        ename: Optional[str] = None,
        shipping_gross_weight: Optional[int] = None,
        variant_ids: Optional[List[str]] = None,
        video_url: Optional[str] = None,
        article_no: Optional[str] = None,
        transparent_image: Optional[str] = None,
        description: Optional[str] = None,
        faq: Optional[List[dict]] = None,
        delivery_mode: Optional[int] = None,
        free_return: Optional[int] = None,
        enable_multi_warehouse: Optional[bool] = None,
        size_table_image: Optional[str] = None,
        recommend_size_table_image: Optional[str] = None,
        model_try_on_size_table_image: Optional[str] = None,
        enable_main_spec_image: Optional[bool] = None,
        item_short_title: Optional[str] = None,
    ) -> "BaseResponse[ItemDetailV3]":
        """使用V2 API更新商品 (API: product.updateItemV2).

        使用V2 API格式更新现有商品，具有增强的
        配置选项和全面的属性管理。

        Args:
            item_id (str): 要更新的商品ID（更新操作必填）
            name (Optional[str]): 更新的商品标题
            brand_id (Optional[int]): 更新的品牌ID
            category_id (Optional[str]): 更新的类目ID
            attributes (Optional[List[dict]]): 更新的商品属性
            images (Optional[List[str]]): 更新的商品主图
            image_descriptions (Optional[List[str]]): 更新的详情描述图片
            shipping_template_id (Optional[str]): 更新的运费模板ID
            ename (Optional[str]): 更新的英文商品名称
            shipping_gross_weight (Optional[int]): 商品重量（克）
            variant_ids (Optional[List[str]]): 变体类型定义
            video_url (Optional[str]): 主图视频
            article_no (Optional[str]): 商品货号
            transparent_image (Optional[str]): 透明背景图片
            description (Optional[str]): 商品描述（最多500字）
            faq (Optional[List[dict]]): 常见问题
            delivery_mode (Optional[int]): 物流模式（0=普通，1=无物流）
            free_return (Optional[int]): 7天退货支持（1=是，2=否）
            enable_multi_warehouse (Optional[bool]): 启用多仓
            size_table_image (Optional[str]): 基础尺码表图片
            recommend_size_table_image (Optional[str]): 推荐尺码表
            model_try_on_size_table_image (Optional[str]): 模特试穿表
            enable_main_spec_image (Optional[bool]): 启用主规格图片
            item_short_title (Optional[str]): 短标题（6-12个汉字）

        Returns:
            BaseResponse[ItemDetailV3]: 响应包含:
                - 更新的商品详情
                - 修改的配置设置
                - 更新时间戳

        Note:
            此V2 API提供增强的商品管理功能。
            更新时确保提供所有必需字段。
        """
        # Automatically determine updated fields based on non-None parameters
        updated_fields = []
        params = locals()
        field_names = [
            "name",
            "brand_id",
            "category_id",
            "attributes",
            "images",
            "image_descriptions",
            "shipping_template_id",
            "ename",
            "shipping_gross_weight",
            "variant_ids",
            "video_url",
            "article_no",
            "transparent_image",
            "description",
            "faq",
            "delivery_mode",
            "free_return",
            "enable_multi_warehouse",
            "size_table_image",
            "recommend_size_table_image",
            "model_try_on_size_table_image",
            "enable_main_spec_image",
            "item_short_title",
        ]

        for field in field_names:
            if params.get(field) is not None:
                updated_fields.append(field)

        request = UpdateItemV3Request(
            item_id=item_id,
            updated_fields=updated_fields,
            name=name,
            brand_id=brand_id,
            category_id=category_id,
            attributes=attributes,
            images=images,
            image_descriptions=image_descriptions,
            shipping_template_id=shipping_template_id,
            ename=ename,
            shipping_gross_weight=shipping_gross_weight,
            variant_ids=variant_ids,
            video_url=video_url,
            article_no=article_no,
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
            item_short_title=item_short_title,
        )
        return self._execute(request, response_model=ItemDetailV3)

    def create_item_and_sku(
        self,
        # Item data
        name: str,
        brand_id: int,
        category_id: str,
        attributes: List[dict],
        images: List[str],
        image_descriptions: List[str],
        shipping_template_id: str,
        # SKU data
        price: int,
        original_price: Optional[int] = None,
        stock: int = 0,
        logistics_plan_id: Optional[str] = None,
        variants: Optional[List[dict]] = None,
        delivery_time: Optional[dict] = None,
        # Optional item data
        ename: Optional[str] = None,
        shipping_gross_weight: Optional[int] = None,
        variant_ids: Optional[List[str]] = None,
        video_url: Optional[str] = None,
        article_no: Optional[str] = None,
        transparent_image: Optional[str] = None,
        description: Optional[str] = None,
        faq: Optional[List[dict]] = None,
        delivery_mode: Optional[int] = None,
        free_return: Optional[int] = None,
        enable_multi_warehouse: Optional[bool] = None,
        size_table_image: Optional[str] = None,
        recommend_size_table_image: Optional[str] = None,
        model_try_on_size_table_image: Optional[str] = None,
        enable_main_spec_image: Optional[bool] = None,
        item_short_title: Optional[str] = None,
        # Optional SKU data
        whcode: Optional[str] = None,
        price_type: Optional[int] = None,
        erp_code: Optional[str] = None,
        spec_image: Optional[str] = None,
        barcode: Optional[str] = None,
    ) -> "BaseResponse[ItemAndSkuDetail]":
        """创建商品（Item+Sku）(API: product.createItemAndSku).

        在单个操作中同时创建完整的商品，包括商品和SKU信息。
        这是创建新商品的推荐方法。

        Args:
            name (str): item标题 (required).
            brand_id (int): 品牌ID,目前查询品牌返回均为String但是是数字可以强转成Long使用 (required).
            category_id (str): 末级商品类目ID,根据common.getCategories获取 (required).
            attributes (List[dict]): item属性，根据common.getAttributeLists和common.getAttributeValues获取，必填属性必填，无必填属性可不填 (required).
            images (List[str]): 商品主图 (required).
            image_descriptions (List[str]): 商品详情描述图片 (required).
            shipping_template_id (str): 运费模板ID，根据common.getCarriageTemplateList获取 (required).
            price (int): 售价，单位分，要求小于市场价，上限10w元，即10000000分 (required).
            original_price (Optional[int]): 市场价，单位分.
            stock (int): 库存.
            logistics_plan_id (Optional[str]): 物流方案Id，通过common.getLogisticsList获取.
            variants (Optional[List[dict]]): 规格列表，根据item定义对规格填写具体规格值，item没有则不填.
            delivery_time (Optional[dict]): 发货时间信息.
            ename (Optional[str]): item英文名.
            shipping_gross_weight (Optional[int]): 商品物流重量（克），当运费模版选择按重量计费时，该值必须大于0.
            variant_ids (Optional[List[str]]): 定义item可以有的规格类型，例如颜色，尺码，sku依赖了此处定义的规格类型.
            video_url (Optional[str]): 主图视频.
            article_no (Optional[str]): 商品货号.
            transparent_image (Optional[str]): 透明图.
            description (Optional[str]): 商品描述文字，上限500字.
            faq (Optional[List[dict]]): 常见问题.
            delivery_mode (Optional[int]): 物流模式,0：普通，1：支持无物流发货（限定类目支持，不支持的类目创建会报错）.
            free_return (Optional[int]): 是否支持7天无理由,1：支持，2：不支持，不传会按照规则给默认值，必须支持则支持，不必须则不支持.
            enable_multi_warehouse (Optional[bool]): 是否启用多仓.
            size_table_image (Optional[str]): 基础尺码表.
            recommend_size_table_image (Optional[str]): 尺码推荐表.
            model_try_on_size_table_image (Optional[str]): 模特试穿表.
            enable_main_spec_image (Optional[bool]): 是否启用规格大图.
            item_short_title (Optional[str]): 商品短标题 (长度限制：最小6个汉字12个字符，最大6个汉字24个字符).
            whcode (Optional[str]): 仓库号.
            price_type (Optional[int]): 是否包税.
            erp_code (Optional[str]): 商家编码.
            spec_image (Optional[str]): 规格图.
            barcode (Optional[str]): 商品条形码，创建特定品类必填.

        Returns:
            BaseResponse[ItemAndSkuDetail]: Response containing:
                - Created item details with assigned ID
                - Created SKU details with pricing and inventory
                - Complete product configuration

        Note:
            这是创建新商品的推荐API，因为它确保了item和SKU数据之间的一致性。
            item和SKU都在单个原子操作中创建。
        """
        request = CreateItemAndSkuRequest(
            name=name,
            brand_id=brand_id,
            category_id=category_id,
            attributes=attributes,
            images=images,
            image_descriptions=image_descriptions,
            shipping_template_id=shipping_template_id,
            price=price,
            original_price=original_price,
            stock=stock,
            logistics_plan_id=logistics_plan_id,
            variants=variants or [],
            delivery_time=delivery_time or {},
            ename=ename,
            shipping_gross_weight=shipping_gross_weight,
            variant_ids=variant_ids or [],
            video_url=video_url,
            article_no=article_no,
            transparent_image=transparent_image,
            description=description,
            faq=faq or [],
            delivery_mode=delivery_mode,
            free_return=free_return,
            enable_multi_warehouse=enable_multi_warehouse,
            size_table_image=size_table_image,
            recommend_size_table_image=recommend_size_table_image,
            model_try_on_size_table_image=model_try_on_size_table_image,
            enable_main_spec_image=enable_main_spec_image,
            item_short_title=item_short_title,
            whcode=whcode,
            price_type=price_type,
            erp_code=erp_code,
            spec_image=spec_image,
            barcode=barcode,
        )
        return self._execute(request, response_model=ItemAndSkuDetail)

    def update_item_and_sku(
        self,
        item_id: str,
        sku_id: str,
        # Item data
        name: Optional[str] = None,
        brand_id: Optional[int] = None,
        category_id: Optional[str] = None,
        attributes: Optional[List[dict]] = None,
        images: Optional[List[str]] = None,
        image_descriptions: Optional[List[str]] = None,
        shipping_template_id: Optional[str] = None,
        # SKU data
        price: Optional[int] = None,
        original_price: Optional[int] = None,
        stock: Optional[int] = None,
        logistics_plan_id: Optional[str] = None,
        variants: Optional[List[dict]] = None,
        delivery_time: Optional[dict] = None,
        # Optional item data
        ename: Optional[str] = None,
        shipping_gross_weight: Optional[int] = None,
        variant_ids: Optional[List[str]] = None,
        video_url: Optional[str] = None,
        article_no: Optional[str] = None,
        transparent_image: Optional[str] = None,
        description: Optional[str] = None,
        faq: Optional[List[dict]] = None,
        delivery_mode: Optional[int] = None,
        free_return: Optional[int] = None,
        enable_multi_warehouse: Optional[bool] = None,
        size_table_image: Optional[str] = None,
        recommend_size_table_image: Optional[str] = None,
        model_try_on_size_table_image: Optional[str] = None,
        enable_main_spec_image: Optional[bool] = None,
        item_short_title: Optional[str] = None,
        # Optional SKU data
        whcode: Optional[str] = None,
        price_type: Optional[int] = None,
        erp_code: Optional[str] = None,
        spec_image: Optional[str] = None,
        barcode: Optional[str] = None,
    ) -> "BaseResponse[ItemAndSkuDetail]":
        """同时更新商品和SKU (API: product.updateItemAndSku).

        在单个操作中更新商品和SKU信息，确保
        商品详情和SKU规格之间的一致性。

        Args:
            item_id (str): 商品ID标识
            sku_id (str): SKU ID标识
            name (Optional[str]): 更新的商品标题
            brand_id (Optional[int]): 更新的品牌ID
            category_id (Optional[str]): 更新的类目ID
            attributes (Optional[List[dict]]): 更新的商品属性
            images (Optional[List[str]]): 更新的商品主图
            image_descriptions (Optional[List[str]]): 更新的详情描述图片
            shipping_template_id (Optional[str]): 更新的运费模板ID
            price (Optional[int]): 更新的售价（分）
            original_price (Optional[int]): 更新的市场价（分）
            stock (Optional[int]): 更新的库存数量
            logistics_plan_id (Optional[str]): 更新的物流方案ID
            variants (Optional[List[dict]]): 更新的规格变体
            delivery_time (Optional[dict]): 更新的发货时间配置
            ename (Optional[str]): 更新的英文商品名称
            shipping_gross_weight (Optional[int]): 商品重量（克）
            variant_ids (Optional[List[str]]): 变体类型定义
            video_url (Optional[str]): 主图视频
            article_no (Optional[str]): 商品货号
            transparent_image (Optional[str]): 透明背景图片
            description (Optional[str]): 商品描述（最多500字）
            faq (Optional[List[dict]]): 常见问题
            delivery_mode (Optional[int]): 物流模式（0=普通，1=无物流）
            free_return (Optional[int]): 7天退货支持（1=是，2=否）
            enable_multi_warehouse (Optional[bool]): 启用多仓
            size_table_image (Optional[str]): 基础尺码表图片
            recommend_size_table_image (Optional[str]): 推荐尺码表
            model_try_on_size_table_image (Optional[str]): 模特试穿表
            enable_main_spec_image (Optional[bool]): 启用主规格图片
            item_short_title (Optional[str]): 短标题（6-12个汉字）
            whcode (Optional[str]): 仓库代码
            price_type (Optional[int]): 含税类型
            erp_code (Optional[str]): 商家SKU编码
            spec_image (Optional[str]): 规格图片
            barcode (Optional[str]): 商品条码

        Returns:
            BaseResponse[ItemAndSkuDetail]: 响应包含:
                - 更新的商品详情
                - 更新的SKU详情（当前价格和库存）
                - 完整的更新产品配置

        Note:
            此API确保对商品和SKU数据的原子更新，
            保持完整产品信息的一致性。
        """
        request = UpdateItemAndSkuRequest(
            item_id=item_id,
            sku_id=sku_id,
            name=name,
            brand_id=brand_id,
            category_id=category_id,
            attributes=attributes,
            images=images,
            image_descriptions=image_descriptions,
            shipping_template_id=shipping_template_id,
            price=price,
            original_price=original_price,
            stock=stock,
            logistics_plan_id=logistics_plan_id,
            variants=variants,
            delivery_time=delivery_time,
            ename=ename,
            shipping_gross_weight=shipping_gross_weight,
            variant_ids=variant_ids,
            video_url=video_url,
            article_no=article_no,
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
            item_short_title=item_short_title,
            whcode=whcode,
            price_type=price_type,
            erp_code=erp_code,
            spec_image=spec_image,
            barcode=barcode,
        )
        return self._execute(request, response_model=ItemAndSkuDetail)

    def create_sku_v2(
        self,
        item_id: str,
        price: int,
        stock: int,
        logistics_plan_id: str,
        variants: List[dict],
        delivery_time: dict,
        original_price: Optional[int] = None,
        whcode: Optional[str] = None,
        price_type: Optional[int] = None,
        erp_code: Optional[str] = None,
        spec_image: Optional[str] = None,
        barcode: Optional[str] = None,
    ) -> "BaseResponse[SkuDetail]":
        """使用V2 API创建SKU (API: product.createSkuV2) - 即将废弃.

        使用V2 API格式为现有商品创建新SKU。
        SKU定义价格、库存和变体规格。

        Args:
            item_id (str): 关联的商品ID (必填)
            price (int): 售价（分）(必填)
            stock (int): 初始库存数量 (必填)
            logistics_plan_id (str): 物流方案ID (必填)
            variants (List[dict]): 规格变体 (必填)
            delivery_time (dict): 发货时间配置 (必填)
            original_price (Optional[int]): 市场价（分）
            whcode (Optional[str]): 仓库代码
            price_type (Optional[int]): 含税类型
            erp_code (Optional[str]): 商家SKU编码
            spec_image (Optional[str]): 规格图片
            barcode (Optional[str]): 商品条码

        Returns:
            BaseResponse[SkuDetail]: 响应包含:
                - 带有分配ID的已创建SKU详情
                - 价格和库存配置
                - 变体规格

        Note:
            此API标记为即将废弃。考虑使用create_item_and_sku
            创建新产品或较新的SKU创建方法。
        """
        request = CreateSkuV3Request(
            item_id=item_id,
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
        )
        return self._execute(request, response_model=SkuDetail)

    def update_sku_v2(
        self,
        sku_id: str,
        item_id: str,
        price: Optional[int] = None,
        original_price: Optional[int] = None,
        stock: Optional[int] = None,
        logistics_plan_id: Optional[str] = None,
        variants: Optional[List[dict]] = None,
        delivery_time: Optional[dict] = None,
        whcode: Optional[str] = None,
        price_type: Optional[int] = None,
        erp_code: Optional[str] = None,
        spec_image: Optional[str] = None,
        barcode: Optional[str] = None,
    ) -> "BaseResponse[SkuDetail]":
        """使用V2 API更新SKU (API: product.updateSkuV2).

        使用V2 API格式更新SKU信息，包括价格、库存、物流
        和变体规格。

        Args:
            sku_id (str): 要更新的SKU ID (必填)
            item_id (str): 关联的商品ID (必填)
            price (Optional[int]): 更新的售价（分）
            original_price (Optional[int]): 更新的市场价（分）
            stock (Optional[int]): 更新的库存数量
            logistics_plan_id (Optional[str]): 更新的物流方案ID
            variants (Optional[List[dict]]): 更新的规格
            delivery_time (Optional[dict]): 更新的发货配置
            whcode (Optional[str]): 仓库代码
            price_type (Optional[int]): 含税类型
            erp_code (Optional[str]): 商家SKU编码
            spec_image (Optional[str]): 规格图片
            barcode (Optional[str]): 商品条码

        Returns:
            BaseResponse[SkuDetail]: 响应包含:
                - 更新的SKU详情
                - 当前价格和库存
                - 更新的变体规格

        Note:
            此API提供全面的SKU管理功能。
            仅提供需要更新的字段。
        """
        # Automatically determine updated fields based on non-None parameters
        updated_fields = []
        params = locals()
        field_names = [
            "price",
            "original_price",
            "stock",
            "logistics_plan_id",
            "variants",
            "delivery_time",
            "whcode",
            "price_type",
            "erp_code",
            "spec_image",
            "barcode",
        ]

        for field in field_names:
            if params.get(field) is not None:
                updated_fields.append(field)

        request = UpdateSkuV3Request(
            sku_id=sku_id,
            item_id=item_id,
            updated_fields=updated_fields,
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
        )
        return self._execute(request, response_model=SkuDetail)

    def delete_item_v2(
        self,
        item_id: str,
    ) -> "BaseResponse[str]":
        """使用V2 API删除商品 (API: product.deleteItemV2).

        使用V2 API格式永久删除商品及所有关联的SKU。
        此操作无法撤销。

        Args:
            item_id (str): 要删除的商品ID

        Returns:
            BaseResponse[str]: 响应包含:
                - 删除确认消息
                - 操作状态

        Warning:
            此操作将永久删除商品和所有关联的SKU。
            请确保这是预期的操作后再执行。

        Note:
            此V2 API提供增强的删除功能，具有更好的
            错误处理和验证。
        """
        request = DeleteItemV3Request(item_ids=[item_id])
        return self._execute(request)

    def delete_sku_v2(
        self,
        sku_id: str,
    ) -> "BaseResponse[str]":
        """使用V2 API删除SKU (API: product.deleteSkuV2).

        永久删除特定SKU，同时保持关联的商品完整。
        这允许删除特定的变体或配置。

        Args:
            sku_id (str): 要删除的SKU ID

        Returns:
            BaseResponse[str]: 响应包含:
                - 删除确认消息
                - 操作状态

        Warning:
            此操作将永久删除SKU。如果这是商品的最后一个
            SKU，请考虑对整个产品的影响。

        Note:
            此V2 API提供精确的SKU管理，具有增强的
            验证和错误处理。
        """
        request = DeleteSkuV3Request(sku_ids=[sku_id])
        return self._execute(request)

    def update_item_price(
        self,
        sku_id: str,
        price: Optional[List[dict]] = None,
        original_price: Optional[int] = None,
    ) -> "BaseResponse[str]":
        """修改价格 (API: product.updateSkuPrice).

        更新SKU的价格信息，包括售价和市场价。
        支持单品和组合商品。

        Args:
            sku_id (str): skuId.
            price (Optional[List[dict]]): 价格信息，组合品才是list:
                - 对于组合商品: 子商品价格列表
                - 对于单品: 单个价格条目
                - Each entry contains:
                    - skuId (str): skuId，组合品为子商品id
                    - price (int): 价格，注意单位为分
            original_price (Optional[int]): 市场价，单位为分.

        Returns:
            BaseResponse[str]: Response containing:
                - error_code (int): 错误码
                - success (bool): 是否成功
                - data (object): 返回信息

        Examples:
            >>> # Update single product price
            >>> response = client.product.update_item_price(
            ...     access_token,
            ...     sku_id="6123**5132",
            ...     price=[{"skuId": "6123**5132", "price": 8000}],
            ...     original_price=10000
            ... )

            >>> # Update combination product pricing
            >>> response = client.product.update_item_price(
            ...     access_token,
            ...     sku_id="combo123",
            ...     price=[
            ...         {"skuId": "sub1", "price": 5000},
            ...         {"skuId": "sub2", "price": 3000}
            ...     ]
            ... )

        Note:
            所有价格均以分为单位 (例如：8000 = 80.00 元)。
            对于组合商品，请为每个子商品提供价格。
        """
        request = UpdateItemPriceRequest(
            item_id=sku_id,  # First parameter is item_id, not sku_id
            price=price or [],
            original_price=original_price,
        )
        return self._execute(request)

    def update_sku_logistics_plan(
        self,
        sku_id: str,
        logistics_plan_id: str,
    ) -> "BaseResponse[dict]":
        """更新SKU物流方案 (API: product.updateSkuLogisticsPlan).

        更新特定SKU的物流方案配置，
        影响运输方式和配送选项。

        Args:
            sku_id (str): 要更新的SKU ID
            logistics_plan_id (str): 新的物流方案ID

        Returns:
            BaseResponse[dict]: 响应包含:
                - 操作结果和状态信息
                - 更新的物流配置详情

        Examples:
            >>> # 更新SKU的物流方案
            >>> response = client.product.update_sku_logistics_plan(
            ...     access_token,
            ...     sku_id="6123**5132",
            ...     logistics_plan_id="5e37***a9f0"
            ... )

        Note:
            物流方案ID可通过common.getLogisticsList API获取。
            此操作影响运费计算和配送选项。
        """
        request = UpdateSkuLogisticsPlanRequest(
            sku_id=sku_id,
            logistics_plan_id=logistics_plan_id,
        )
        return self._execute(request)

    def update_sku_price(
        self,
        sku_id: str,
        price: List[dict],
        original_price: Optional[float] = None,
        extra: Optional[dict] = None,
    ) -> "BaseResponse[str]":
        """更新SKU价格 (API: product.updateSkuPrice).

        更新特定SKU的价格信息，包括
        售价和市场价配置。

        Args:
            sku_id (str): 要更新的SKU ID
            price (List[dict]): 价格信息列表
            original_price (Optional[float]): 新的市场价
            extra (Optional[dict]): 额外的价格参数

        Returns:
            BaseResponse[str]: 响应包含:
                - 操作确认消息
                - 成功状态

        Examples:
            >>> # 更新SKU价格
            >>> response = client.product.update_sku_price(
            ...     access_token,
            ...     sku_id="6123**5132",
            ...     price=[{"skuId": "6123**5132", "price": 8500}],
            ...     original_price=10000
            ... )

        Note:
            价格以分为单位（例如：8500 = 85.00元）。
            售价应小于市场价。
        """
        request = UpdateSkuPriceRequest(
            sku_id=sku_id,
            price=price,
            original_price=original_price,
            extra=extra or {},
        )
        return self._execute(request)

    def update_sku_available(
        self,
        sku_id: str,
        available: bool,
    ) -> "BaseResponse[str]":
        """更新SKU可用性状态 (API: product.updateSkuAvailable).

        更新SKU的可用性状态，控制
        客户是否可以购买。

        Args:
            sku_id (str): 要更新的SKU ID
            available (bool): 可用性状态（True=可用，False=不可用）

        Returns:
            BaseResponse[str]: 响应包含:
                - 操作确认消息
                - 成功状态

        Examples:
            >>> # 设置SKU为可用
            >>> response = client.product.update_sku_available(
            ...     access_token,
            ...     sku_id="6123**5132",
            ...     available=True
            ... )

            >>> # 设置SKU为不可用
            >>> response = client.product.update_sku_available(
            ...     access_token,
            ...     sku_id="6123**5132",
            ...     available=False
            ... )

        Note:
            这控制商家可用性意愿。实际的可购买状态
            可能还取决于库存水平和其他平台政策。
        """
        request = UpdateSkuAvailableRequest(
            sku_id=sku_id,
            available=available,
        )
        return self._execute(request)

    def update_item_image(
        self,
        item_id: str,
        material_type: int,
        material_urls: List[str],
    ) -> "BaseResponse[str]":
        """修改商品主图、主图视频 (API: product.updateItemImage).

        更新商品的主图或主图视频。
        支持图片廊和主商品视频。

        Args:
            item_id (str): itemId (required).
            material_type (int): 素材类型，1：图片，2：视频 (required).
            material_urls (List[str]): 素材url，图片全量覆盖、视频取第一个 (required).

        Returns:
            BaseResponse[str]: Response containing:
                - error_code (int): 错误码
                - success (bool): 是否成功
                - data (object): 返回信息

        Examples:
            >>> # Update product images (complete replacement)
            >>> response = client.product.update_item_image(
            ...     access_token,
            ...     item_id="64******412f1f",
            ...     material_type=1,
            ...     material_urls=[
            ...         "https://img.example.com/image1.jpg",
            ...         "https://img.example.com/image2.jpg",
            ...         "https://img.example.com/image3.jpg"
            ...     ]
            ... )

            >>> # Update main product video
            >>> response = client.product.update_item_image(
            ...     access_token,
            ...     item_id="64******412f1f",
            ...     material_type=2,
            ...     material_urls=["https://video.example.com/main.mp4"]
            ... )

        Note:
            对于图片 (materialType=1): 所有现有图片都将被替换。
            对于视频 (materialType=2): 仅使用第一个URL作为主视频。
            确保所有URL都可访问并格式正确。
        """
        request = UpdateItemImageRequest(
            item_id=item_id,
            material_type=material_type,
            material_urls=material_urls,
        )
        return self._execute(request)

    def update_spu_image(
        self,
        spu_id: str,
        image_urls: Optional[List[str]] = None,
        extra: Optional[dict] = None,
    ) -> "BaseResponse[str]":
        """Update SPU images.

        Updates the image configuration for an SPU (Standard Product Unit),
        affecting the visual representation of the product template.

        Args:
            spu_id (str): SPU ID to update.
            image_urls (Optional[List[str]]): Updated image URLs.
            extra (Optional[dict]): Additional image configurations.

        Returns:
            BaseResponse[str]: Response containing:
                - Operation confirmation message
                - Success status

        Note:
            SPU image updates affect the template representation
            that may be inherited by associated items.
        """
        request = UpdateSpuImageRequest(
            spu_id=spu_id,
            image_urls=image_urls or [],
            extra=extra or {},
        )
        return self._execute(request)

    def update_variant_image(
        self,
        variant_id: str,
        image_url: Optional[str] = None,
        variant_type: Optional[str] = None,
        extra: Optional[dict] = None,
    ) -> "BaseResponse[str]":
        """Update variant specification images.

        Updates images associated with specific product variants or specifications,
        such as color swatches or size charts.

        Args:
            variant_id (str): Variant identification information.
            image_url (Optional[str]): Updated specification image URL.
            variant_type (Optional[str]): Type of variant being updated.
            extra (Optional[dict]): Additional variant image configurations.

        Returns:
            BaseResponse[str]: Response containing:
                - Operation confirmation message
                - Success status

        Note:
            Variant images help customers visualize different product
            specifications and make informed purchasing decisions.
        """
        request = UpdateVariantImageRequest(
            variant_id=variant_id,
            image_url=image_url,
            variant_type=variant_type,
            extra=extra or {},
        )
        return self._execute(request)
