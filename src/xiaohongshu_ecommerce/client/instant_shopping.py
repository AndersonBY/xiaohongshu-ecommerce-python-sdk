"""Instant shopping management client for Xiaohongshu e-commerce API."""

from typing import Optional, List

from ..models.base import BaseResponse
from ..models.instant_shopping import (
    UpdateInstantShoppingTrackRequest,
    UpdateRiderLocationRequest,
    InstantShoppingTrackingDTO,
    AddressLocation,
)
from .base import SyncSubClient


class InstantShoppingClient(SyncSubClient):
    """即时零售配送管理API的同步客户端。

    即时零售为小红书电商订单提供实时配送服务。
    此客户端处理配送跟踪更新、配送员位置更新和即时配送服务的实时物流信息。
    """

    def update_instant_shopping_track(
        self,
        xhs_order_id: str,
        express_company_code: str,
        express_no: str,
        traces: List[InstantShoppingTrackingDTO],
    ) -> BaseResponse[str]:
        """近场轨迹推送 (API: express.instantshopping.updateInstantShoppingTrack).

        更新即时零售订单的配送跟踪状态和位置信息。
        此API允许商家向客户推送实时配送进度更新。

        Args:
            xhs_order_id (str): 小红书订单ID (必需)
            express_company_code (str): 快递公司编码 (必需)
            express_no (str): 快递跟踪号 (必需)
            traces (List[InstantShoppingTrackingDTO]): 跟踪事件列表 (必需):
                - xhs_order_id (str): 此跟踪事件的订单ID
                - express_company_code (str): 快递公司编码
                - express_no (str): 快递跟踪号
                - leaf_node_type (str): 跟踪事件类型 (例如: "SIGNED_SIGNED")
                - event_at (str): 事件时间戳 (格式: "YYYY-MM-DD HH:mm:ss")
                - event_desc (str): 事件描述 (例如: "已签收")
                - current_location (AddressLocation, 可选): 当前配送位置:
                    - longitude (str): 经度坐标
                    - latitude (str): 纬度坐标
                    - address (str, 可选): 人类可读地址
                - exception_code (str, 可选): 异常码（如有问题）
                - exception_reason (str, 可选): 异常原因描述
                - courier_name (str, 可选): 配送员姓名
                - courier_phone (str, 可选): 配送员电话号码
                - courier_phone_type (str, 可选): 电话类型指示符
                - expect_arrival_time (str, 可选): 预计到达时间
                - delivery_distance (str, 可选): 剩余配送距离
                - ext (str, 可选): 扩展字段

        Returns:
            BaseResponse[str]: 响应包含:
                - success (bool): 是否成功
                - error_code (int): 错误码 (成功时为0)
                - error_msg (str): 信息

        Examples:
            >>> # 更新带位置的配送跟踪
            >>> from xiaohongshu_ecommerce.models.instant_shopping import (
            ...     InstantShoppingTrackingDTO,
            ...     AddressLocation
            ... )
            >>>
            >>> # 创建位置信息
            >>> location = AddressLocation(
            ...     longitude="116.397477",
            ...     latitude="39.916668"
            ... )
            >>>
            >>> # 创建跟踪事件
            >>> tracking_event = InstantShoppingTrackingDTO(
            ...     xhs_order_id="P732676080389468281",
            ...     express_company_code="meituan",
            ...     express_no="1717124279363001636",
            ...     leaf_node_type="PICKUP_PICKUP",
            ...     event_at="2024-05-31 15:30:00",
            ...     event_desc="配送员已取货",
            ...     current_location=location,
            ...     courier_name="张三",
            ...     courier_phone="13800138000",
            ...     expect_arrival_time="2024-05-31 16:00:00"
            ... )
            >>>
            >>> # 更新跟踪
            >>> response = client.instant_shopping.update_instant_shopping_track(
            ...     access_token=access_token,
            ...     xhs_order_id="P732676080389468281",
            ...     express_company_code="meituan",
            ...     express_no="1717124279363001636",
            ...     traces=[tracking_event]
            ... )

            >>> # 更新多个跟踪事件
            >>> events = [
            ...     InstantShoppingTrackingDTO(
            ...         xhs_order_id="P732676080389468281",
            ...         express_company_code="meituan",
            ...         express_no="1717124279363001636",
            ...         leaf_node_type="PICKUP_PICKUP",
            ...         event_at="2024-05-31 15:30:00",
            ...         event_desc="配送员已取货",
            ...         courier_name="张三"
            ...     ),
            ...     InstantShoppingTrackingDTO(
            ...         xhs_order_id="P732676080389468281",
            ...         express_company_code="meituan",
            ...         express_no="1717124279363001636",
            ...         leaf_node_type="SIGNED_SIGNED",
            ...         event_at="2024-05-31 15:48:58",
            ...         event_desc="已签收",
            ...         courier_name="张三"
            ...     )
            ... ]
            >>> response = client.instant_shopping.update_instant_shopping_track(
            ...     access_token=access_token,
            ...     xhs_order_id="P732676080389468281",
            ...     express_company_code="meituan",
            ...     express_no="1717124279363001636",
            ...     traces=events
            ... )

        Note:
            此API用于实时配送跟踪更新。确保跟踪事件
            按时间顺序发送以获得最佳客户体验。
            坐标系统应与您的配送服务使用的标准匹配。
        """
        request = UpdateInstantShoppingTrackRequest(
            xhs_order_id=xhs_order_id,
            express_company_code=express_company_code,
            express_no=express_no,
            traces=traces,
        )
        request.method = "express.instantshopping.updateInstantShoppingTrack"
        return self._execute(request, response_model=str)

    def update_rider_location(
        self,
        xhs_order_id: str,
        express_no: str,
        express_company_code: str,
        courier_name: Optional[str] = None,
        courier_phone: Optional[str] = None,
        current_location: Optional[AddressLocation] = None,
        status: Optional[str] = None,
        status_desc: Optional[str] = None,
    ) -> BaseResponse[str]:
        """更新骑手位置信息 (API: express.instantshopping.updateRiderLocation).

        更新即时零售订单配送骑手的实时位置。
        这为客户提供对配送员位置的实时追踪。

        Args:
            xhs_order_id (str): 小红书订单ID (必需)
            express_no (str): 快递跟踪号 (必需)
            express_company_code (str): 快递公司编码 (必需)
            courier_name (Optional[str]): 配送员姓名
            courier_phone (Optional[str]): 配送员电话号码
            current_location (Optional[AddressLocation]): 骑手当前位置:
                - longitude (str): 经度坐标
                - latitude (str): 纬度坐标
                - address (str, 可选): 人类可读地址
            status (Optional[str]): 当前配送状态
            status_desc (Optional[str]): 状态描述

        Returns:
            BaseResponse[str]: 响应包含:
                - success (bool): 位置更新是否成功
                - error_code (int): 错误码 (成功时为0)
                - error_msg (str): 错误消息（如有）

        Examples:
            >>> # 更新骑手位置
            >>> from xiaohongshu_ecommerce.models.instant_shopping import (
            ...     AddressLocation
            ... )
            >>>
            >>> # 创建当前位置
            >>> current_location = AddressLocation(
            ...     longitude="116.397477",
            ...     latitude="39.916668",
            ...     address="北京市朝阳区建国门外大街1号"
            ... )
            >>>
            >>> # 更新位置
            >>> response = client.instant_shopping.update_rider_location(
            ...     access_token=access_token,
            ...     xhs_order_id="P732676080389468281",
            ...     express_no="1717124279363001636",
            ...     express_company_code="meituan",
            ...     courier_name="张三",
            ...     courier_phone="13800138000",
            ...     current_location=current_location,
            ...     status="delivering",
            ...     status_desc="正在配送中"
            ... )

            >>> # 仅更新位置而不包含其他详情
            >>> location_only = AddressLocation(
            ...     longitude="116.400000",
            ...     latitude="39.920000"
            ... )
            >>> response = client.instant_shopping.update_rider_location(
            ...     access_token=access_token,
            ...     xhs_order_id="P732676080389468281",
            ...     express_no="1717124279363001636",
            ...     express_company_code="meituan",
            ...     current_location=location_only
            ... )

        Note:
            位置更新频率应足够高以提供流畅的跟踪体验，
            但不能高到压倒系统的程度。活跃配送期间的典型更新间隔为
            30秒到2分钟。
            确保位置坐标准确并使用适当的坐标系统。
        """
        request = UpdateRiderLocationRequest(
            xhs_order_id=xhs_order_id,
            express_no=express_no,
            express_company_code=express_company_code,
            courier_name=courier_name,
            courier_phone=courier_phone,
            current_location=current_location,
            status=status,
            status_desc=status_desc,
        )
        request.method = "express.instantshopping.updateRiderLocation"
        return self._execute(request, response_model=str)
