"""Inventory client implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional

from .base import SyncSubClient
from ..models import (
    CreateWarehouseRequest,
    GetItemStockRequest,
    GetSkuStockRequest,
    GetSkuStockV2Request,
    GetWarehouseRequest,
    GetWarehouseResponseData,
    IncItemStockRequest,
    IncSkuStockRequest,
    ItemStockResponseData,
    ListWarehouseRequest,
    ListWarehouseResponseData,
    SetWarehouseCoverageRequest,
    SetWarehousePriorityRequest,
    SkuStockResponseData,
    SyncItemStockRequest,
    SyncSkuStockRequest,
    SyncSkuStockV2Request,
    SyncSkuStockV2ResponseData,
    UpdateWarehouseRequest,
)

if TYPE_CHECKING:  # pragma: no cover
    from ..models import BaseResponse, GetSkuStockV2ResponseData


class InventoryClient(SyncSubClient):
    """Synchronous client for inventory and warehouse management APIs.

    This client provides access to XiaoHongShu inventory management endpoints including
    SKU stock queries, inventory synchronization, warehouse management, and multi-warehouse
    operations. Essential for e-commerce inventory control and order fulfillment.
    """

    def get_item_stock(
        self,
        item_id: str,
    ) -> "BaseResponse[ItemStockResponseData]":
        """获取商品库存信息 (API: inventory.getItemStock).

        获取指定商品的库存信息，提供商品级别的汇总库存数据，
        包含该商品下所有规格的总库存情况。

        Args:
            item_id (str): 商品ID，用于检索库存信息 (必填)。

        Returns:
            BaseResponse[ItemStockResponseData]: 响应数据包含:
                - itemId (str): 商品ID
                - totalAvailable (int): 商品总可售库存（所有规格之和）
                - totalStock (int): 商品总库存（所有规格之和）
                - skuStockList (List[SkuStockInfo]): 规格级别库存信息列表
                - lastUpdateTime (int): 最后更新时间戳

        Examples:
            ```python
            # 获取商品库存信息
            response = client.inventory.get_item_stock(
                access_token, item_id="64******412f1f"
            )

            print(f"总可售库存: {response.data.totalAvailable}")
            print(f"总库存: {response.data.totalStock}")
            for sku_stock in response.data.skuStockList:
                print(f"规格 {sku_stock.skuId}: {sku_stock.available} 可售")
            ```

        说明:
            此接口提供商品级别的汇总库存数据。如需详细的规格级别库存信息，
            请使用 get_sku_stock() 或 get_sku_stock_v2()。
        """
        request = GetItemStockRequest(item_id=item_id)
        return self._execute(request, response_model=ItemStockResponseData)

    def sync_item_stock(
        self,
        item_id: str,
        total_qty: int,
        distribution_mode: Optional[str] = None,
        sku_qty_list: Optional[List] = None,
    ) -> "BaseResponse[ItemStockResponseData]":
        """同步商品库存 (API: inventory.syncItemStock).

        同步商品级别的库存数量，更新该商品下所有关联规格的库存。
        此操作影响商品的总可售库存并将变更分配给各个规格。

        Args:
            item_id (str): 要同步库存的商品ID (必填)。
            total_qty (int): 要设置的新总库存数量 (必填)。
            distribution_mode (str, optional): 如何在规格间分配库存:
                - "proportional": 按当前比例分配
                - "equal": 平均分配给所有规格
                - "manual": 使用提供的规格具体数量
            sku_qty_list (List[SkuQtyInfo], optional): 手动模式下的规格具体数量。

        Returns:
            BaseResponse[ItemStockResponseData]: 响应数据包含:
                - itemId (str): 更新的商品ID
                - totalAvailable (int): 新的总可售库存
                - totalStock (int): 新的总库存数量
                - skuStockList (List[SkuStockInfo]): 更新后的规格库存信息
                - updateTime (int): 同步时间戳

        Examples:
            ```python
            # 按比例分配同步商品库存
            response = client.inventory.sync_item_stock(
                access_token,
                item_id="64******412f1f",
                total_qty=500,
                distribution_mode="proportional"
            )

            # 手动分配规格库存
            from xiaohongshu_ecommerce.models import SkuQtyInfo
            sku_quantities = [
                SkuQtyInfo(skuId="sku1", qty=200),
                SkuQtyInfo(skuId="sku2", qty=300)
            ]
            response = client.inventory.sync_item_stock(
                access_token,
                item_id="64******412f1f",
                total_qty=500,
                distribution_mode="manual",
                sku_qty_list=sku_quantities
            )
            ```

        重要说明:
            - 此操作会更新商品下所有规格的库存
            - 分配模式决定库存如何分配给各个规格
            - 手动模式需要为所有活跃规格提供数量
            - 如果商品有待处理订单或预留库存，同步可能失败
        """
        request = SyncItemStockRequest(
            item_id=item_id,
            total_qty=total_qty,
            distribution_mode=distribution_mode,
            sku_qty_list=sku_qty_list,
        )
        return self._execute(request, response_model=ItemStockResponseData)

    def inc_item_stock(
        self,
        item_id: str,
        qty: int,
        reason: Optional[str] = None,
        reference_id: Optional[str] = None,
        distribution_mode: Optional[str] = None,
        sku_adjustments: Optional[List] = None,
    ) -> "BaseResponse[ItemStockResponseData]":
        """增减商品库存 (API: inventory.incItemStock).

        调整商品库存，通过增加或减少指定数量来修改可售库存。
        此操作修改可售库存同时保持适当的库存跟踪和审计记录。

        Args:
            item_id (str): 要调整库存的商品ID (必填)。
            qty (int): 要增加（正数）或减少（负数）的数量 (必填)。
            reason (str, optional): 库存调整原因。
            reference_id (str, optional): 外部参考ID，用于跟踪。
            distribution_mode (str, optional): 如何在规格间分配:
                - "proportional": 按当前比例分配（默认）
                - "equal": 平均分配给所有规格
                - "manual": 使用提供的规格具体调整量
            sku_adjustments (List[SkuAdjustment], optional): 手动模式下的规格具体调整量。

        Returns:
            BaseResponse[ItemStockResponseData]: 响应数据包含:
                - itemId (str): 调整的商品ID
                - totalAvailable (int): 新的总可售库存
                - totalStock (int): 新的总库存数量
                - adjustmentAmount (int): 实际应用的调整数量
                - skuStockList (List[SkuStockInfo]): 更新后的规格库存信息
                - updateTime (int): 调整时间戳

        Examples:
            ```python
            # 增加商品库存100个单位
            response = client.inventory.inc_item_stock(
                access_token,
                item_id="64******412f1f",
                qty=100,
                reason="供应商补货"
            )

            # 因损坏减少库存
            response = client.inventory.inc_item_stock(
                access_token,
                item_id="64******412f1f",
                qty=-25,
                reason="损坏商品移除",
                reference_id="DMG-2024-001"
            )

            # 手动指定规格调整量
            from xiaohongshu_ecommerce.models import SkuAdjustment
            sku_adjustments = [
                SkuAdjustment(skuId="sku1", qty=50),
                SkuAdjustment(skuId="sku2", qty=25)
            ]
            response = client.inventory.inc_item_stock(
                access_token,
                item_id="64******412f1f",
                qty=75,
                distribution_mode="manual",
                sku_adjustments=sku_adjustments,
                reason="定向补货"
            )
            ```

        使用场景:
            - 供应商补货
            - 库存更正和盘点
            - 损坏或丢失调整
            - 退货处理
            - 促销库存分配

        重要说明:
            - 负数减少库存
            - 调整不能使可售库存低于零
            - 手动分配需要指定所有受影响的规格
            - 所有调整都会记录用于审计
        """
        request = IncItemStockRequest(
            item_id=item_id,
            qty=qty,
            reason=reason,
            reference_id=reference_id,
            distribution_mode=distribution_mode,
            sku_adjustments=sku_adjustments,
        )
        return self._execute(request, response_model=ItemStockResponseData)

    def get_sku_stock(
        self,
        sku_id: str,
    ) -> "BaseResponse[SkuStockResponseData]":
        """获取商品库存 (API: inventory.getSkuStock).

        获取指定SKU的库存信息，包括可售库存、总库存、占用库存以及各渠道库存分配情况。
        提供完整的库存明细和仓库维度的库存数据。

        Args:
            sku_id (str): 规格ID (必填)。

        Returns:
            BaseResponse[SkuStockResponseData]: 响应数据包含:
                - skuId (str): 规格ID
                - apiVersion (str): 接口版本（V0未命中灰度，V1命中灰度）
                - skuStock (SkuStock): sku维度库存数据（所有仓之和）包含:
                    - available (int): 可售库存
                    - total (int): 总库存
                    - occupiedQuantity (int): 占用库存（该商品可售库存被用户下单，处于未支付状态下导致的库存占用）
                    - productChannelQuantity (int): 商品渠道可售库存（该商品衍生的渠道品，分配给其独立库存中的可售部分）
                    - productChannelOccupiedQuantity (int): 商品渠道占用库存（该商品衍生的渠道品，分配给其独立库存中的订单占用部分）
                    - activityChannelQuantity (int): 活动渠道可售库存（该商品分配给活动渠道的独立库存中的可售部分）
                    - activityChannelOccupiedQuantity (int): 活动渠道占用库存（该商品分配给活动渠道的独立库存中的订单占用部分）
                    - reserved (int): 废弃字段
                    - standalone (int): 废弃字段
                - skuStockInfoWithWhcode (List[SkuStockInfoWithWhcode]): 仓维度库存数据:
                    - skuId (str): 规格ID
                    - whcode (str): 仓库编码
                    - skuStock (SkuStock): 仓维度库存数据

        Examples:
            ```python
            # 获取SKU库存信息
            response = client.inventory.get_sku_stock(
                access_token, sku_id="66ee****873d"
            )

            stock_data = response.data
            print(f"规格ID: {stock_data.skuId}")
            print(f"可售库存: {stock_data.skuStock.available}")
            print(f"总库存: {stock_data.skuStock.total}")
            print(f"占用库存: {stock_data.skuStock.occupiedQuantity}")

            # 查看仓库维度库存信息
            for warehouse_stock in stock_data.skuStockInfoWithWhcode:
                print(f"仓库 {warehouse_stock.whcode}: {warehouse_stock.skuStock.available} 可售")
            ```

        库存组成说明:
            - **可售库存**: 可以销售的库存数量
            - **总库存**: 包含所有分配的完整库存
            - **占用库存**: 被未支付订单占用的库存
            - **商品渠道库存**: 分配给渠道品的独立库存
            - **活动渠道库存**: 分配给促销活动的独立库存

        多仓库支持:
            - 每个仓库返回独立的库存数据
            - 汇总数据为所有仓库库存之和
            - 仓库编码标识具体存储位置

        重要说明:
            - V1接口版本包含增强的库存跟踪功能
            - reserved和standalone字段已废弃
            - 可售库存 = 总库存 - 占用库存 - 渠道分配
            - 仓库级别数据有助于履约优化
        """
        request = GetSkuStockRequest(sku_id=sku_id)
        return self._execute(request, response_model=SkuStockResponseData)

    def sync_sku_stock(
        self,
        sku_id: str,
        qty: int,
    ) -> "BaseResponse[SkuStockResponseData]":
        """同步库存 (API: inventory.syncSkuStock).

        同步SKU库存，通过设置总库存数量来自动计算可售库存。系统会根据总库存减去
        占用库存和渠道分配来计算可售库存。

        Args:
            sku_id (str): 规格ID（限定为未开启多仓区域库存的普通品）(必填)。
            qty (int): qty是需要同步的sku总库存数，其总库存数包含了普通品本身库存+渠道品独立库存+活动独立库存+待支付订单占用库存。接口逻辑会用qty与现在sku的总库存数进行差值计算，去设置可售库存 (必填)。

        Returns:
            BaseResponse[SkuStockResponseData]: 响应数据包含:
                - skuId (str): 规格ID
                - apiVersion (str): 接口版本（V0未命中灰度，V1命中灰度）
                - skuStock (SkuStock): sku维度库存数据（所有仓之和）包含:
                    - available (int): 可售库存
                    - total (int): 总库存
                    - occupiedQuantity (int): 占用库存（该商品可售库存被用户下单，处于未支付状态下导致的库存占用）
                    - 渠道分配详细信息
                - skuStockInfoWithWhcode (List): 仓维度库存数据
                - response (Response): 操作结果包含:
                    - success (bool): 是否成功
                    - message (str): 提示信息
                    - code (int): 状态码

        Examples:
            ```python
            # 同步SKU库存到100个单位
            response = client.inventory.sync_sku_stock(
                access_token, sku_id="66ee****873d", qty=100
            )

            if response.data.response.success:
                print(f"库存同步成功")
                print(f"可售库存: {response.data.skuStock.available}")
                print(f"总库存: {response.data.skuStock.total}")
            else:
                print(f"同步失败: {response.data.response.message}")

            # 处理带警告的部分同步
            response = client.inventory.sync_sku_stock(
                access_token, sku_id="66ee****873d", qty=50
            )

            if response.data.response.code == -9028:
                print("同步成功，但有占用库存未扣减，请检查独立库存占用情况和用户待支付订单占用库存情况")
                print(f"提示信息: {response.data.response.message}")
            ```

        计算逻辑:
            系统使用以下公式计算可售库存:
            ```
            可售库存 = 总库存 - 占用库存 - 商品渠道占用 - 活动渠道占用
            ```

        常见响应码:
            - 0: 成功
            - -9028: 同步成功，但有占用库存未扣减

        限制条件:
            - 仅适用于未开启多仓区域库存的普通品
            - 不能用于复杂仓库配置的商品
            - 多仓商品请使用 sync_sku_stock_v2()

        重要说明:
            - qty表示完整的总库存数，包含所有分配
            - 系统自动处理占用库存扣减
            - 如果占用库存无法完全扣减可能返回警告
            - 请检查响应消息了解同步状态和警告
        """
        request = SyncSkuStockRequest(sku_id=sku_id, qty=qty)
        return self._execute(request, response_model=SkuStockResponseData)

    def inc_sku_stock(
        self,
        sku_id: str,
        qty: int,
    ) -> "BaseResponse[SkuStockResponseData]":
        """增减库存 (API: inventory.incSkuStock).

        增减SKU库存，通过增加或减少指定数量来调整可售库存。此操作直接修改可售库存
        并维护适当的库存跟踪和审计记录。

        Args:
            sku_id (str): 规格ID（限定为未开启多仓区域库存的普通品）(必填)。
            qty (int): qty是需要增减的sku可售库存数，接口逻辑会将现在sku的可售库存数加上设置的qty，以操作可售库存的增减 (必填)。
                注意: 正数增加库存，负数减少库存

        Returns:
            BaseResponse[SkuStockResponseData]: 响应数据包含:
                - skuId (str): 规格ID
                - apiVersion (str): 接口版本（V0未命中灰度，V1命中灰度）
                - skuStock (SkuStock): sku维度库存数据（所有仓之和）包含:
                    - available (int): 可售库存
                    - total (int): 总库存
                    - occupiedQuantity (int): 占用库存（该商品可售库存被用户下单，处于未支付状态下导致的库存占用）
                    - 渠道分配详细信息
                - skuStockInfoWithWhcode (List): 仓维度库存数据
                - response (Response): 操作结果包含成功状态

        Examples:
            ```python
            # 增加可售库存50个单位
            response = client.inventory.inc_sku_stock(
                access_token, sku_id="66ee****873d", qty=50
            )

            print(f"新的可售库存: {response.data.skuStock.available}")
            print(f"总库存: {response.data.skuStock.total}")

            # 因损坏减少库存（负数量）
            response = client.inventory.inc_sku_stock(
                access_token, sku_id="66ee****873d", qty=-10
            )

            if response.data.response.success:
                print(f"库存减少10个单位")
                print(f"剩余可售: {response.data.skuStock.available}")
            ```

        调整逻辑:
            - 正数qty: 同时增加可售库存和总库存
            - 负数qty: 同时减少可售库存和总库存
            - 无法将可售库存减少到零以下
            - 调整同时影响总库存

        使用场景:
            - 快速库存调整
            - 损坏或损失记录
            - 手动库存更正
            - 退货处理
            - 盘点调整

        限制条件:
            - 仅适用于未开启多仓区域库存的普通品
            - 无法调整占用库存或渠道分配库存
            - 多仓商品请使用其他库存管理方法

        重要说明:
            - 直接修改可售库存，与设置总库存的sync_sku_stock不同
            - 负调整不能超过当前可售数量
            - 可售库存和总库存都会按调整数量更新
            - 所有调整都会记录用于审计
        """
        request = IncSkuStockRequest(sku_id=sku_id, qty=qty)
        return self._execute(request, response_model=SkuStockResponseData)

    def get_sku_stock_v2(
        self,
        sku_id: str,
        inventory_type: Optional[int] = None,
    ) -> "BaseResponse[GetSkuStockV2ResponseData]":
        """获取商品库存V2 (API: inventory.getSkuStockV2).

        获取三方商家库存的增强版本，支持多仓库存管理。提供全面的库存数据，
        包含仓库维度明细和高级库存类型筛选。

        Args:
            sku_id (str): 规格ID (必填)。
            inventory_type (int, optional): 库存类型:
                - 1: 普通库存（默认）
                - 2: 渠道库存
                - 3: 活动库存

        Returns:
            BaseResponse[GetSkuStockV2ResponseData]: 响应数据包含:
                - response (Response): 响应体
                - apiVersion (str): 接口版本（V0未命中灰度，V1命中灰度）
                - skuStockInfo (SkuStockInfoV2): sku维度库存数据包含:
                    - skuId (str): 规格ID
                    - skuStockInfo (SkuStockV2): 库存数据:
                        - available (int): 可售库存
                        - total (int): 总库存
                        - occupiedQuantity (int): 占用库存（该商品可售库存被用户下单，处于未支付状态下导致的库存占用）
                        - productChannelQuantity (int): 商品渠道可售库存（该商品衍生的渠道品，分配给其独立库存中的可售部分）
                        - productChannelOccupiedQuantity (int): 商品渠道占用库存（该商品衍生的渠道品，分配给其独立库存中的订单占用部分）
                        - activityChannelQuantity (int): 活动渠道可售库存（该商品分配给活动渠道的独立库存中的可售部分）
                        - activityChannelOccupiedQuantity (int): 活动渠道占用库存（该商品分配给活动渠道的独立库存中的订单占用部分）
                        - reserved (int): 废弃字段
                        - standalone (int): 废弃字段
                - skuStockInfoWithWhcode (List[SkuStockInfoWithWhcodeV2]): 仓维度库存数据:
                    - skuId (str): 规格ID
                    - whcode (str): 仓库编号 (如: "zhejiang", "yunnan")
                    - skuStockInfo (SkuStockV2): 仓维度库存数据

        Examples:
            ```python
            # 获取SKU普通库存
            response = client.inventory.get_sku_stock_v2(
                access_token, sku_id="6706****52bc", inventory_type=1
            )

            stock_info = response.data.skuStockInfo
            print(f"规格ID: {stock_info.skuId}")
            print(f"总可售库存: {stock_info.skuStockInfo.available}")
            print(f"总库存: {stock_info.skuStockInfo.total}")

            # 查看多仓库分布
            for warehouse in response.data.skuStockInfoWithWhcode:
                print(f"仓库 {warehouse.whcode}:")
                print(f"  可售库存: {warehouse.skuStockInfo.available}")
                print(f"  总库存: {warehouse.skuStockInfo.total}")

            # 获取渠道库存信息
            response = client.inventory.get_sku_stock_v2(
                access_token, sku_id="6706****52bc", inventory_type=2
            )
            ```

        多仓库功能:
            - 支持区域仓库库存跟踪
            - 每个仓库维护独立的库存水平
            - 汇总数据为所有仓库之和
            - 仓库编号标识具体位置 (如: "zhejiang", "yunnan")

        库存类型:
            - **普通库存 (1)**: 标准商品库存
            - **渠道库存 (2)**: 渠道专属分配库存
            - **活动库存 (3)**: 促销活动分配库存

        V2版本增强:
            - 多仓区域库存支持
            - 增强的库存类型筛选
            - 改进的仓库维度数据结构
            - 更好地支持复杂库存场景

        重要说明:
            - V2接口支持多仓库存配置
            - 适用于区域仓库分布的商品
            - 提供更精细的仓库级库存控制
            - 在高级库存管理场景中取代V1接口
        """
        from ..models import GetSkuStockV2ResponseData

        request = GetSkuStockV2Request(sku_id=sku_id, inventory_type=inventory_type)
        return self._execute(request, response_model=GetSkuStockV2ResponseData)

    def sync_sku_stock_v2(
        self,
        sku_id: str,
        qty_with_whcode: Dict[str, int],
    ) -> "BaseResponse[SyncSkuStockV2ResponseData]":
        """同步库存V2 (API: inventory.syncSkuStockV2).

        同步三方商家库存的高级版本，支持多仓配置。允许按仓库设置库存数量，
        处理复杂的区域库存分布场景。

        Args:
            sku_id (str): 规格ID (必填)。
            qty_with_whcode (Dict[str, int]): 传参为map类型，多仓区域库存传需要修改的仓数据，"qtyWithWhcode": {"yunnan": 100, "zhejiang": 100}。非多仓区域库存使用默认仓，"qtyWithWhcode": {"CPartner": 100} (必填)。
                格式: {"仓库编码": 数量, ...}
                示例:
                - 多仓库: {"yunnan": 100, "zhejiang": 100}
                - 单仓库: {"CPartner": 100}

        Returns:
            BaseResponse[SyncSkuStockV2ResponseData]: 响应数据包含:
                - response (Response): 响应体
                - apiVersion (str): 接口版本（V0未命中灰度，V1命中灰度）
                - skuStockInfo (SkuStockInfoV2): sku维度库存数据
                - data (Dict): 仓维度库存数据，该值map类型，key为仓库编码，value为库存数据
                    键: 仓库编码, 值: 仓库库存信息
                    示例结构:
                    ```
                    {
                        "zhejiang": {
                            "skuId": "67064f2b980e2f00016052bc",
                            "whcode": "zhejiang",
                            "skuStockInfo": {
                                "available": 80,
                                "total": 100,
                                "occupiedQuantity": 20,
                                "productChannelQuantity": 0,
                                ...
                            }
                        },
                        "yunnan": {...}
                    }
                    ```

        Examples:
            ```python
            # 同步多仓库库存
            warehouse_quantities = {
                "yunnan": 150,
                "zhejiang": 200
            }
            response = client.inventory.sync_sku_stock_v2(
                access_token,
                sku_id="6706****52bc",
                qty_with_whcode=warehouse_quantities
            )

            if response.data.response.success:
                print("多仓库同步成功")
                print(f"总可售库存: {response.data.skuStockInfo.skuStockInfo.available}")

                # 查看仓库维度结果
                for warehouse, stock_data in response.data.data.items():
                    print(f"仓库 {warehouse}: {stock_data['skuStockInfo']['available']} 可售")

            # 同步单仓库（非多仓商品）
            response = client.inventory.sync_sku_stock_v2(
                access_token,
                sku_id="6706****52bc",
                qty_with_whcode={"CPartner": 300}
            )

            # 仅更新指定仓库
            response = client.inventory.sync_sku_stock_v2(
                access_token,
                sku_id="6706****52bc",
                qty_with_whcode={"zhejiang": 250}  # 仅更新浙江仓库
            )
            ```

        多仓库配置:
            - **多仓商品**: 使用区域仓库编码 ("yunnan", "zhejiang", 等)
            - **单仓商品**: 使用默认仓库编码 ("CPartner")
            - 可以一次更新所有仓库或单独更新特定仓库

        仓库编码:
            - 区域编码: "yunnan", "zhejiang", "guangdong", 等
            - 默认编码: "CPartner" (非多仓商品)
            - 商家配置的自定义仓库编码

        同步逻辑:
            - 每个仓库数量代表该位置的总库存
            - 系统通过减去占用数量计算可售库存
            - 跨所有仓库重新计算汇总总数

        错误处理:
            - -1009005: 类目没有销售属性
            - -1009003: 类目没有对应属性
            - 无效的仓库编码将被拒绝

        重要说明:
            - V2接口用于所有多仓库存操作
            - 支持区域和单仓库配置
            - 仅更新指定的仓库，其他仓库保持不变
            - 仓库编码必须与配置的仓库设置匹配
        """
        request = SyncSkuStockV2Request(sku_id=sku_id, qty_with_whcode=qty_with_whcode)
        return self._execute(request, response_model=SyncSkuStockV2ResponseData)

    def create_warehouse(
        self,
        code: str,
        name: str,
        zone_code: str,
        address: str,
        contact_name: Optional[str] = None,
        contact_tel: Optional[str] = None,
    ) -> "BaseResponse[str]":
        """创建仓库 (API: warehouse.create).

        创建新的仓库用于库存管理和区域分发。仓库可以实现多位置库存跟踪，
        根据与客户的地理距离优化履约。

        Args:
            code (str): 仓库编码，不可重复，创建后不可修改，只能是数字、字母和下划线，长度限制24 (必填)。
            name (str): 仓库名称，长度限制50 (必填)。
            zone_code (str): 城镇/街道对应的行政地区编码，需要选到最末级地区编码 (必填)。
            address (str): 详细地址 (必填)。
            contact_name (str, optional): 联系人。
            contact_tel (str, optional): 联系人电话。

        Returns:
            BaseResponse[str]: 响应数据包含:
                - success (bool): 是否成功
                - error_code (int): 错误编码 (0成功)
                - error_msg (str): 错误信息

        Examples:
            ```python
            # 创建基本仓库
            response = client.inventory.create_warehouse(
                access_token,
                code="test_01",
                name="测试仓库01",
                zone_code="310105004000",
                address="详细地址***"
            )

            if response.success:
                print("仓库创建成功")
            else:
                print(f"仓库创建失败: {response.error_msg}")

            # 创建包含联系信息的仓库
            response = client.inventory.create_warehouse(
                access_token,
                code="wh_beijing_001",
                name="北京配送中心",
                zone_code="110108023000",
                address="海淀区物流大道123号",
                contact_name="张三",
                contact_tel="1234567"
            )
            ```

        重要说明:
            - 仓库编码创建后不可更改
            - 仓库编码不可重复，只能是数字、字母和下划线
            - 必须选择最细粒度的行政级别（乡镇/街道）
            - 地区编码影响运费计算和配送路由
            - 新仓库初始库存为零
        """
        request = CreateWarehouseRequest(
            code=code,
            name=name,
            zone_code=zone_code,
            address=address,
            contact_name=contact_name,
            contact_tel=contact_tel,
        )
        return self._execute(request, response_model=str)

    def update_warehouse(
        self,
        code: str,
        name: Optional[str] = None,
        zone_code: Optional[str] = None,
        address: Optional[str] = None,
        contact_name: Optional[str] = None,
        contact_tel: Optional[str] = None,
    ) -> "BaseResponse[str]":
        """修改仓库 (API: warehouse.update).

        更新仓库信息，包括名称、位置和联系详细信息。允许修改除仓库编码外的所有仓库属性，
        仓库编码在创建后保持不可变。

        Args:
            code (str): 仓库编码 (必填，不可变标识符)。
            name (str, optional): 仓库名称，长度限制50。
            zone_code (str, optional): 城镇/街道对应的行政地区编码，需要选到最末级地区编码。
            address (str, optional): 详细地址。
            contact_name (str, optional): 联系人。
            contact_tel (str, optional): 联系人电话。

        Returns:
            BaseResponse[str]: 响应数据包含:
                - success (bool): 是否成功
                - error_code (int): 错误编码 (0成功)
                - error_msg (str): 错误信息

        Examples:
            ```python
            # 更新仓库名称和联系信息
            response = client.inventory.update_warehouse(
                access_token,
                code="test_01",
                name="测试仓库01",
                contact_name="张三",
                contact_tel="1234567"
            )

            if response.success:
                print("仓库更新成功")
            else:
                print(f"更新失败: {response.error_msg}")

            # 更新仓库位置
            response = client.inventory.update_warehouse(
                access_token,
                code="test_01",
                zone_code="310105004000",  # 新地区编码
                address="详细地址***"
            )

            # 仅更新特定字段
            response = client.inventory.update_warehouse(
                access_token,
                code="test_01",
                contact_tel="1234567"  # 仅更新电话号码
            )
            ```

        重要说明:
            - 仓库编码不可修改，作为永久标识符
            - 仅更新提供的字段，省略的字段保持当前值
            - 位置更改可能影响覆盖区域和运费计算
            - 更新立即应用于所有仓库操作
        """
        request = UpdateWarehouseRequest(
            code=code,
            name=name,
            zone_code=zone_code,
            address=address,
            contact_name=contact_name,
            contact_tel=contact_tel,
        )
        return self._execute(request, response_model=str)

    def list_warehouse(
        self,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        code: Optional[str] = None,
        name: Optional[str] = None,
    ) -> "BaseResponse[ListWarehouseResponseData]":
        """仓库列表 (API: warehouse.list).

        获取分页的仓库列表，可选择按仓库编码和名称过滤。提供全面的仓库信息，
        包括位置详细信息和联系信息。

        Args:
            page_no (int, optional): 页码，默认1。
            page_size (int, optional): 每页数量，默认10，限制100。
            code (str, optional): 仓库编码。
            name (str, optional): 仓库名称。

        Returns:
            BaseResponse[ListWarehouseResponseData]: 响应数据包含:
                - data (WarehouseListData): 仓库列表数据包含:
                    - total (int): 符合筛选条件的仓库总数
                    - warehouseList (List[WarehouseInfo]): 仓库信息列表:
                        - code (str): 仓库编码
                        - name (str): 仓库名称
                        - province (str): 省
                        - provinceCode (str): 省编码
                        - city (str): 市
                        - cityCode (str): 市编码
                        - area (str): 区/县
                        - areaCode (str): 区/县编码
                        - town (str): 街道/镇
                        - townCode (str): 街道/镇编码
                        - address (str): 详细地址
                        - contactName (str): 联系人
                        - contactTel (str): 联系电话
                - success (bool): 是否成功
                - error_code (int): 错误编码 (0成功)
                - error_msg (str): 错误信息

        Examples:
            ```python
            # 获取所有仓库（默认分页）
            response = client.inventory.list_warehouse(access_token)

            if response.success:
                warehouses = response.data.warehouseList
                print(f"仓库总数: {response.data.total}")
                for warehouse in warehouses:
                    print(f"编码: {warehouse.code}, 名称: {warehouse.name}")
                    print(f"位置: {warehouse.province} {warehouse.city} {warehouse.area}")
                    print(f"联系: {warehouse.contactName} - {warehouse.contactTel}")
                    print("---")

            # 按编码搜索特定仓库
            response = client.inventory.list_warehouse(
                access_token, code="test_01"
            )

            if response.data.total > 0:
                warehouse = response.data.warehouseList[0]
                print(f"找到仓库: {warehouse.name}")
                print(f"完整地址: {warehouse.province} {warehouse.city} {warehouse.area}")
                print(f"           {warehouse.town} {warehouse.address}")

            # 按名称搜索并分页
            response = client.inventory.list_warehouse(
                access_token,
                name="测试",  # 部分名称匹配
                page_no=1,
                page_size=20
            )

            # 获取所有仓库（大分页尺寸）
            response = client.inventory.list_warehouse(
                access_token, page_size=100
            )
            ```

        重要说明:
            - 空筛选条件返回所有仓库
            - 建议对拥有多个仓库的账户使用分页
            - 位置编码对应中国行政区划
            - 如果创建时未提供，联系信息可能为空
        """
        request = ListWarehouseRequest(
            page_no=page_no, page_size=page_size, code=code, name=name
        )
        return self._execute(request, response_model=ListWarehouseResponseData)

    def get_warehouse(
        self,
        code: str,
    ) -> "BaseResponse[GetWarehouseResponseData]":
        """仓库详情 (API: warehouse.info).

        获取指定仓库的详细信息，包括位置详细信息、联系信息和覆盖区域配置。
        提供完整的仓库档案，用于管理和运营目的。

        Args:
            code (str): 仓库编码 (必填)。

        Returns:
            BaseResponse[GetWarehouseResponseData]: 响应数据包含:
                - success (bool): 是否成功
                - error_code (int): 错误编码 (0成功)
                - error_msg (str): 错误信息
                - data (WarehouseDetailInfo): 仓库详细信息包含:
                    - code (str): 仓库编码
                    - name (str): 仓库名称
                    - province (str): 省
                    - provinceCode (str): 省行政编码
                    - city (str): 市
                    - cityCode (str): 市行政编码
                    - area (str): 区/县
                    - areaCode (str): 区/县行政编码
                    - town (str): 街道/镇 (可选)
                    - townCode (str): 街道/镇行政编码 (可选)
                    - address (str): 详细地址
                    - contactName (str): 联系人
                    - contactTel (str): 联系电话
                    - coverageList (List[CoverageArea]): 仓库覆盖区域包含:
                        - province (str): 覆盖省名
                        - provinceCode (str): 覆盖省编码
                        - city (str): 覆盖市名 (可选)
                        - cityCode (str): 覆盖市编码 (可选)
                        - area (str): 覆盖区名 (可选)
                        - areaCode (str): 覆盖区编码 (可选)

        Examples:
            ```python
            # 获取仓库详细信息
            response = client.inventory.get_warehouse(
                access_token, code="test_01"
            )

            if response.success:
                warehouse = response.data
                print(f"仓库: {warehouse.name} ({warehouse.code})")
                print(f"位置: {warehouse.province} {warehouse.city} {warehouse.area}")
                print(f"地址: {warehouse.address}")
                print(f"联系: {warehouse.contactName} - {warehouse.contactTel}")

                # 显示覆盖区域
                print("\n覆盖区域:")
                for coverage in warehouse.coverageList:
                    coverage_desc = coverage.province
                    if coverage.city:
                        coverage_desc += f" > {coverage.city}"
                    if coverage.area:
                        coverage_desc += f" > {coverage.area}"
                    print(f"  - {coverage_desc}")
            else:
                print(f"获取仓库失败: {response.error_msg}")

            # 检查仓库是否服务特定区域
            response = client.inventory.get_warehouse(
                access_token, code="test_01"
            )

            if response.success:
                # 检查是否覆盖上海
                covers_shanghai = any(
                    coverage.provinceCode == "310000"  # 上海省编码
                    for coverage in response.data.coverageList
                )
                print(f"是否覆盖上海: {covers_shanghai}")
            ```

        重要说明:
            - 返回完整的仓库档案包含覆盖配置
            - 覆盖列表决定仓库服务的区域
            - 联系信息对物流协调至关重要
            - 行政编码用于精确的地理定位
        """
        request = GetWarehouseRequest(code=code)
        return self._execute(request, response_model=GetWarehouseResponseData)

    def set_warehouse_coverage(
        self,
        wh_code: str,
        zone_code_list: List[str],
    ) -> "BaseResponse[str]":
        """设置仓库覆盖地区 (API: warehouse.setCoverage).

        配置仓库可以为订单履约服务的地理区域。
        覆盖区域决定仓库将处理哪些地区的货物运输，
        影响运费、交付时间和自动仓库选择。

        Args:
            wh_code (str): 仓库编码 (必填)。
            zone_code_list (List[str]): 行政地区编码列表，只能是一级、二级或三级地区编码 (必填)。
                - 一级（省）、二级（市）或三级（区/县）编码
                - 示例: ["310000", "320000"] 上海和江苏省
                - 示例: ["310101", "310102"] 上海特定区县

        Returns:
            BaseResponse[str]: 响应数据包含:
                - success (bool): 是否成功
                - error_code (int): 错误编码 (0成功)
                - error_msg (str): 错误信息

        Examples:
            ```python
            # 设置省级覆盖（服务整个省份）
            zone_codes = [
                "310000",  # 上海
                "320000",  # 江苏省
                "330000"   # 浙江省
            ]
            response = client.inventory.set_warehouse_coverage(
                access_token,
                wh_code="test_01",
                zone_code_list=zone_codes
            )

            if response.success:
                print("覆盖区域更新成功")
            else:
                print(f"更新覆盖失败: {response.error_msg}")

            # 设置市级覆盖（服务特定城市）
            city_codes = [
                "310100",  # 上海市
                "320100",  # 南京市
                "330100"   # 杭州市
            ]
            response = client.inventory.set_warehouse_coverage(
                access_token,
                wh_code="test_01",
                zone_code_list=city_codes
            )

            # 设置区级覆盖（服务特定区县）
            district_codes = [
                "310101",  # 黄浦区，上海
                "310104",  # 徐汇区，上海
                "310105"   # 长宁区，上海
            ]
            response = client.inventory.set_warehouse_coverage(
                access_token,
                wh_code="test_01",
                zone_code_list=district_codes
            )
            ```

        重要说明:
            - 覆盖区域完全替换现有配置
            - 使用 get_warehouse() 检查更新前的当前覆盖
            - 无效的地区编码将导致操作失败
            - 覆盖更改立即影响未来订单路由
        """
        request = SetWarehouseCoverageRequest(
            wh_code=wh_code, zone_code_list=zone_code_list
        )
        return self._execute(request, response_model=str)

    def set_warehouse_priority(
        self,
        zone_code: str,
        warehouse_priority_list: List[Dict[str, str]],
    ) -> "BaseResponse[str]":
        """设置仓库优先级 (API: warehouse.setPriority).

        为特定地区配置仓库的优先级顺序。当多个仓库服务同一区域时，
        优先级决定了订单履约时首先选择哪个仓库进行库存分配和货物运输。

        Args:
            zone_code (str): 地区编码，只支持一级、二级或三级地区编码 (必填)。
                - 支持一级（省）、二级（市）或三级（区/县）编码
                - 示例: "310000" 上海，"310101" 黄浦区
            warehouse_priority_list (List[Dict[str, str]]): 仓库优先级列表，优先级高的在前 (必填)。
                - 按优先级从高到低排序
                - 每个条目包含: {"whCode": "仓库编码"}
                - 示例: [{"whCode": "wh_primary"}, {"whCode": "wh_backup"}]

        Returns:
            BaseResponse[str]: 响应数据包含:
                - success (bool): 是否成功
                - error_code (int): 错误编码 (0成功)
                - error_msg (str): 错误信息

        Examples:
            ```python
            # 为上海省设置仓库优先级
            priority_list = [
                {"whCode": "test_01"},     # 最高优先级
                {"whCode": "wh_backup"},   # 第二优先级
                {"whCode": "wh_regional"}  # 最低优先级
            ]
            response = client.inventory.set_warehouse_priority(
                access_token,
                zone_code="310000",  # 上海省
                warehouse_priority_list=priority_list
            )

            if response.success:
                print("上海仓库优先级更新成功")
            else:
                print(f"更新优先级失败: {response.error_msg}")

            # 为特定区县设置优先级（更细粒度控制）
            priority_list = [
                {"whCode": "wh_downtown_express"},  # 最快交付
                {"whCode": "wh_city_center"},       # 标准交付
                {"whCode": "wh_suburban_hub"}       # 备用选项
            ]
            response = client.inventory.set_warehouse_priority(
                access_token,
                zone_code="310101",  # 黄浦区，上海
                warehouse_priority_list=priority_list
            )

            # 为地区设置单个仓库为主要仓库
            response = client.inventory.set_warehouse_priority(
                access_token,
                zone_code="320100",  # 南京市
                warehouse_priority_list=[{"whCode": "test_01"}]
            )
            ```

        重要说明:
            - 优先级顺序完全替换该地区的现有配置
            - 所有列出的仓库必须对指定地区有覆盖
            - 优先级影响订单处理期间的自动仓库选择
            - 更高粒度（区/县）优于更广泛（省）设置
            - 更改对新订单立即生效
        """
        request = SetWarehousePriorityRequest(
            zone_code=zone_code, warehouse_priority_list=warehouse_priority_list
        )
        return self._execute(request, response_model=str)
