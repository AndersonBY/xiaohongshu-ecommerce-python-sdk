"""Boutique mode management client for Xiaohongshu e-commerce API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, List

from .base import SyncSubClient
from ..models import (
    BasicBoutiqueItemData,
    BasicBoutiqueSkuData,
    CreateBoutiqueItemRequest,
    CreateBoutiqueItemResponse,
    CreateBoutiqueSkuRequest,
    CreateBoutiqueSkuResponse,
    UpdateBoutiqueItemRequest,
    UpdateBoutiqueSkuRequest,
    BoutiqueMode,
    OperationType,
    BoutiqueItemBatchInfo,
    StockOperateInfo,
)

if TYPE_CHECKING:  # pragma: no cover
    from ..models import BaseRequest, BaseResponse


class BoutiqueClient(SyncSubClient):
    """精品模式管理API的同步客户端。

    精品模式在小红书平台上启用高端商品列表和跨境电商功能。
    此客户端处理为高端商家创建和管理精品商品和SKU，具有增强的配送选项、
    税务处理和库存管理功能。
    """

    def create_item(
        self,
        spu_id: str,
        boutique_modes: Optional[List[BoutiqueMode]] = None,
        with_item_detail: bool = False,
        operation_type: Optional[OperationType] = None,
    ) -> "BaseResponse[CreateBoutiqueItemResponse]":
        """创建精品模式商品 (API: boutique.createBoutiqueItem).

        从现有SPU（标准商品单元）创建精品模式商品，
        为高端商家提供增强功能，包括跨境运输、
        税务处理和高端展示选项。

        Args:
            spu_id (str): 用于创建精品模式商品的SPU ID (必填)。
            boutique_modes (Optional[List[BoutiqueMode]]): 精品模式运输方式:
                - DOMESTIC_GENERAL_SHIPPING: 标准国内运输
                - DOMESTIC_FAST_SHIPPING: 快速国内运输
                - INCLUDE_TAX_FAST_SHIPPING: 含税快速运输
                - INTERNATIONAL_DIRECT_GENERAL_SHIPPING: 标准国际运输
                - INTERNATIONAL_DIRECT_FAST_SHIPPING: 快速国际运输
            with_item_detail (bool): 是否返回详细商品信息。
            operation_type (Optional[OperationType]): 操作类型:
                - CREATE: 创建新精品模式商品
                - UPDATE: 更新现有精品模式商品
                - DELETE: 删除精品模式商品

        Returns:
            BaseResponse[CreateBoutiqueItemResponse]: 响应包含:
                - data (Mapping[str, Any]): 已创建的精品模式商品信息

        Note:
            创建精品模式商品之前SPU必须存在。
            精品模式决定可用的运输和税务选项。
            国际运输模式需要额外的商家认证。
            操作类型可用于批量操作和更新。
        """
        request = CreateBoutiqueItemRequest(
            spu_id=spu_id,
            boutique_modes=boutique_modes,
            with_item_detail=with_item_detail,
            operation_type=operation_type,
        )
        return self._execute(request, response_model=CreateBoutiqueItemResponse)

    def update_item(
        self,
        item_id: str,
        boutique_item_batch_info: Optional[BoutiqueItemBatchInfo] = None,
        boutique_batch_id: Optional[str] = None,
        identity_id: Optional[str] = None,
        with_item_detail: bool = False,
        free_return: Optional[int] = None,
        skucode: Optional[str] = None,
        whcode: Optional[str] = None,
        qty: Optional[int] = None,
        operate_info: Optional[StockOperateInfo] = None,
    ) -> "BaseResponse[BasicBoutiqueItemData]":
        """更新精品模式商品配置 (API: boutique.updateBoutiqueItem).

        更新精品模式商品设置，包括批次信息、库存、
        免费退货政策和仓库配置，以增强客户体验
        和运营效率。

        Args:
            item_id (str): 要更新的精品模式商品ID (必填)。
            boutique_item_batch_info (Optional[BoutiqueItemBatchInfo]): 批次信息。
            boutique_batch_id (Optional[str]): 直接批次ID分配。
            identity_id (Optional[str]): 直接身份ID分配。
            with_item_detail (bool): 是否返回详细商品信息。
            free_return (Optional[int]): 免费退货政策设置。
            skucode (Optional[str]): SKU代码分配。
            whcode (Optional[str]): 仓库代码分配。
            qty (Optional[int]): 数量更新。
            operate_info (Optional[StockOperateInfo]): 库存操作详情。

        Returns:
            BaseResponse[BasicBoutiqueItemData]: 响应包含更新的商品数据。

        Note:
            批次信息用于库存跟踪和质量控制。
            免费退货政策增强对高端商品的客户信心。
            仓库代码必须有效并在系统中配置。
            操作信息被记录以供审计和合规目的。
        """
        request = UpdateBoutiqueItemRequest(
            item_id=item_id,
            boutique_item_batch_info=boutique_item_batch_info,
            boutique_batch_id=boutique_batch_id,
            identity_id=identity_id,
            with_item_detail=with_item_detail,
            free_return=free_return,
            skucode=skucode,
            whcode=whcode,
            qty=qty,
            operate_info=operate_info,
        )
        return self._execute(request, response_model=BasicBoutiqueItemData)

    def create_sku(
        self,
        item_id: str,
        boutique_modes: Optional[List[BoutiqueMode]] = None,
        with_sku_detail: bool = False,
        operation_type: Optional[OperationType] = None,
    ) -> "BaseResponse[CreateBoutiqueSkuResponse]":
        """创建精品模式SKU (API: boutique.createBoutiqueSku).

        从现有商品创建精品模式SKU，具有高端功能，
        包括高级运输模式、税务处理和增强的库存管理，
        适用于复杂的电商操作。

        Args:
            item_id (str): 用于创建精品模式SKU的商品ID (必填)。
            boutique_modes (Optional[List[BoutiqueMode]]): 精品模式运输方式。
            with_sku_detail (bool): 是否返回详细SKU信息。
            operation_type (Optional[OperationType]): 操作类型。

        Returns:
            BaseResponse[CreateBoutiqueSkuResponse]: 响应包含已创建的SKU数据。

        Note:
            创建精品模式SKU之前商品必须存在。
            多种运输模式为客户提供灵活的配送选项。
            国际运输需要适当的商家认证。
            含税模式为适用地区的客户简化定价。
        """
        request = CreateBoutiqueSkuRequest(
            item_id=item_id,
            boutique_modes=boutique_modes,
            with_sku_detail=with_sku_detail,
            operation_type=operation_type,
        )
        return self._execute(request, response_model=CreateBoutiqueSkuResponse)

    def update_sku(
        self,
        sku_id: str,
        boutique_sku_batch_info: Optional[BoutiqueItemBatchInfo] = None,
        boutique_batch_id: Optional[str] = None,
        identity_id: Optional[str] = None,
        with_sku_detail: bool = False,
        free_return: Optional[int] = None,
        sc_skucode: Optional[str] = None,
        whcode: Optional[str] = None,
        qty: Optional[int] = None,
        operate_info: Optional[StockOperateInfo] = None,
    ) -> "BaseResponse[BasicBoutiqueSkuData]":
        """更新精品模式SKU配置 (API: boutique.updateBoutiqueSku).

        更新精品模式SKU设置，包括库存管理、仓库
        分配、免费退货政策和操作跟踪，以实现高端
        电商功能。

        Args:
            sku_id (str): 要更新的精品模式SKU ID (必填)。
            boutique_sku_batch_info (Optional[BoutiqueItemBatchInfo]): 批次信息。
            boutique_batch_id (Optional[str]): 直接批次ID分配。
            identity_id (Optional[str]): 直接身份ID分配。
            with_sku_detail (bool): 是否返回详细SKU信息。
            free_return (Optional[int]): 免费退货政策设置。
            sc_skucode (Optional[str]): 小红书SKU代码分配。
            whcode (Optional[str]): 仓库代码分配。
            qty (Optional[int]): 数量更新。
            operate_info (Optional[StockOperateInfo]): 库存操作详情。

        Returns:
            BaseResponse[BasicBoutiqueSkuData]: 响应包含更新的SKU数据。

        Note:
            批次跟踪确保商品质量和可追溯性。
            免费退货政策增强对高端商品的客户信心。
            仓库代码必须为精品模式操作正确配置。
            操作跟踪维护审计跟踪以保证合规。
        """
        request = UpdateBoutiqueSkuRequest(
            sku_id=sku_id,
            boutique_sku_batch_info=boutique_sku_batch_info,
            boutique_batch_id=boutique_batch_id,
            identity_id=identity_id,
            with_sku_detail=with_sku_detail,
            free_return=free_return,
            sc_skucode=sc_skucode,
            whcode=whcode,
            qty=qty,
            operate_info=operate_info,
        )
        return self._execute(request, response_model=BasicBoutiqueSkuData)

    def create_item_v2(self, request: "BaseRequest") -> "BaseResponse[Any]":
        """创建精品模式商品V2版本 (API: boutique.createBoutiqueItemV2).

        使用增强的V2 API创建精品模式商品，提供高级功能和改进的性能。
        此API与商品模块共享请求模型以确保数据处理的一致性。

        Args:
            request (BaseRequest): V2 API请求对象，包含增强参数

        Returns:
            BaseResponse[Any]: 包含V2 API结果数据的响应

        Note:
            V2 API提供增强功能和性能改进。
            请求模型与商品模块共享以保持一致性。
            请查阅V2 API文档了解具体参数要求。
        """
        # V2 API与商品模块共享请求模型；暂时保持数据不透明。
        return self._execute(request)

    def create_sku_v2(
        self, request: "BaseRequest", access_token: str
    ) -> "BaseResponse[Any]":
        """创建精品模式SKU V2版本 (API: boutique.createBoutiqueSkuV2).

        使用增强的V2 API创建精品模式SKU，具有改进功能和更好的性能特性，
        适用于大规模操作。

        Args:
            request (BaseRequest): V2 API请求对象，包含增强参数

        Returns:
            BaseResponse[Any]: 包含V2 API结果数据的响应

        Note:
            V2 API为大批量SKU创建提供增强性能。
            与V1相比提供更好的错误处理和验证。
            请查阅V2 API文档了解参数规范。
        """
        return self._execute(request)
