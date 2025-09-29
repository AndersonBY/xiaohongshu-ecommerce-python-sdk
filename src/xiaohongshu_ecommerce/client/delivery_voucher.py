"""Delivery voucher management client for Xiaohongshu e-commerce API."""

from typing import Optional, List

from ..models.base import BaseResponse
from ..models.delivery_voucher import (
    BindOrderDeliveryVoucherRequest,
    DeliveryVoucherActionRequest,
    DeliveryVoucherInfoDTO,
)
from .base import SyncSubClient


class DeliveryVoucherClient(SyncSubClient):
    """配送优惠券管理API的同步客户端。

    配送优惠券是可用于小红书电商平台配送折扣或免费配送的数字优惠券。
    此客户端处理优惠券与订单的绑定和优惠券生命周期管理操作。
    """

    def bind_delivery_voucher(
        self,
        action_time: int,
        trace_id: str,
        order_id: str,
        voucher_infos: List[DeliveryVoucherInfoDTO],
        feature: Optional[str] = None,
    ) -> BaseResponse[str]:
        """绑定配送优惠券 (API: order.bindDeliveryVoucher).

        将配送优惠券与特定订单和SKU关联，以提供
        运输折扣或免费配送。此操作必须在订单履约之前
        执行以应用优惠券益处。

        Args:
            action_time (int): 操作时间戳（毫秒）(必填)。
            trace_id (str): 此操作的唯一跟踪ID (必填)。
            order_id (str): 要绑定优惠券的订单ID (必填)。
            voucher_infos (List[DeliveryVoucherInfoDTO]): 优惠券绑定信息 (必填):
                - skuId (str): 适用优惠券的SKU ID
                - deliveryVouchers (List[DeliveryVoucherDTO]): 要绑定的优惠券列表:
                    - id (str): 优惠券ID
                    - no (str): 优惠券号码/代码
                    - startTime (int): 优惠券有效期开始时间（Unix时间戳，毫秒）
                    - endTime (int): 优惠券有效期结束时间（Unix时间戳，毫秒）
            feature (Optional[str]): 额外功能标志。

        Returns:
            BaseResponse[str]: 响应包含:
                - 操作状态和确认信息
                - 绑定失败时的错误信息

        Note:
            优惠券必须在订单履约之前绑定才能生效。
            每张优惠券只能使用一次，并必须在有效期内。
            跟踪ID应为每次绑定操作唯一，以便跟踪目的。
        """
        request = BindOrderDeliveryVoucherRequest(
            action_time=action_time,
            trace_id=trace_id,
            order_id=order_id,
            voucher_infos=voucher_infos,
            feature=feature,
        )
        request.method = "order.bindDeliveryVoucher"
        return self._execute(request, response_model=str)

    def delivery_voucher_action(
        self,
        order_id: str,
        voucher_id: str,
        voucher_no: str,
        trace_id: str,
        action_time: int,
        action_type: str,
        express_no: Optional[str] = None,
        express_company_code: Optional[str] = None,
        express_company_name: Optional[str] = None,
        receiver_name: Optional[str] = None,
        receiver_mobile: Optional[str] = None,
        receiver_address: Optional[str] = None,
    ) -> BaseResponse[str]:
        """执行配送优惠券操作 (API: order.deliveryVoucherAction).

        对配送优惠券执行生命周期管理操作，如激活、
        使用、取消或过期。此API在订单履约过程中
        跟踪优惠券状态变化。

        Args:
            order_id (str): 与优惠券关联的订单ID (必填)。
            voucher_id (str): 优惠券ID (必填)。
            voucher_no (str): 优惠券号码/代码 (必填)。
            trace_id (str): 此操作的唯一跟踪ID (必填)。
            action_time (int): 操作时间戳（毫秒）(必填)。
            action_type (str): 要执行的操作类型 (必填):
                - "ACTIVATE": 激活优惠券
                - "USE": 标记优惠券为已使用
                - "CANCEL": 取消优惠券
                - "EXPIRE": 标记优惠券为已过期
            express_no (Optional[str]): 快递跟踪号。
            express_company_code (Optional[str]): 快递公司代码。
            express_company_name (Optional[str]): 快递公司名称。
            receiver_name (Optional[str]): 收件人姓名。
            receiver_mobile (Optional[str]): 收件人电话号码。
            receiver_address (Optional[str]): 收件人地址。

        Returns:
            BaseResponse[str]: 响应包含:
                - 操作执行状态和确认
                - 操作失败时的错误信息

        Note:
            操作类型必须与当前优惠券状态匹配才能成功执行。
            在运输期间将优惠券标记为已使用时需要快递信息。
            每个操作应有唯一的跟踪ID以便适当跟踪和审计。
            优惠券操作不可逆，因此在执行之前确保操作类型正确。
        """
        request = DeliveryVoucherActionRequest(
            order_id=order_id,
            voucher_id=voucher_id,
            voucher_no=voucher_no,
            trace_id=trace_id,
            action_time=action_time,
            action_type=action_type,
            express_no=express_no,
            express_company_code=express_company_code,
            express_company_name=express_company_name,
            receiver_name=receiver_name,
            receiver_mobile=receiver_mobile,
            receiver_address=receiver_address,
        )
        request.method = "order.deliveryVoucherAction"
        return self._execute(request, response_model=str)
