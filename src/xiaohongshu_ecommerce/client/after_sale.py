"""After-sale client implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from .base import SyncSubClient
from ..models import (
    AuditReturnsReceiverInfo,
    AuditReturnsRequest,
    ConfirmReceiveRequest,
    GetAfterSaleDetailRequest,
    GetAfterSaleDetailResponse,
    GetAfterSaleInfoRequest,
    GetAfterSaleInfoResponse,
    GetAfterSaleListRequest,
    GetAfterSaleListResponse,
    ListAfterSaleInfosRequest,
    ListAfterSaleInfosResponse,
    ListReturnRejectReasonRequest,
    ListReturnRejectReasonResponse,
    ReceiveAndShipRequest,
    ReturnsAbnormalRequest,
)

if TYPE_CHECKING:  # pragma: no cover
    from ..models import BaseResponse


class AfterSaleClient(SyncSubClient):
    """同步访问售后服务端点。

    此客户端提供全面的售后管理功能，包括列出售后请求、处理退货/换货、
    管理审批和处理售后操作的物流。
    """

    def list_after_sale_infos(
        self,
        page_no: int,
        page_size: int,
        order_id: Optional[str] = None,
        statuses: Optional[List[int]] = None,
        return_types: Optional[List[int]] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        time_type: Optional[int] = None,
    ) -> "BaseResponse[ListAfterSaleInfosResponse]":
        """获取售后列表（新）(API: afterSale.listAfterSaleInfos).

        获取售后列表的新版本API，提供更丰富的筛选功能和详细信息。

        Args:
            page_no (int): 页数，从1开始
            page_size (int): 页大小大于0小于等于100  pageNo*pageSize 最大值不能超过50000
            order_id (Optional[str]): 包裹号，包裹号和时间类型至少传一个
            statuses (Optional[List[int]]): 售后状态列表 1-待审核  2-待用户寄回  3-待商家收货  4-已完成  5-已取消6-已关闭  9-商家审核拒绝  9001-商家收货拒绝12-换货待商家发货  13-换货待用户确认收货  14-平台介入中
            return_types (Optional[List[int]]): 售后类型列表 1-退货  2-换货  4-已发货仅退款  5-未发货仅退款 6-保价
            start_time (Optional[int]): 时间起点（毫秒，包含），选择时间类型后必传
            end_time (Optional[int]): 时间终点（毫秒，包含）  时间终点应当大于时间起点，选择时间类型后必传
            time_type (Optional[int]): 时间类型  1-创建时间，范围不大于24小时  2-更新时间，范围不大于30分钟，包裹号和时间类型至少传一个

        Returns:
            BaseResponse[ListAfterSaleInfosResponse]: 响应包含:
                - afterSaleBasicInfos (List[AfterSaleBasicInfo]): 售后列表信息:
                    - returnsId (str): 售后id
                    - returnType (int): 售后类型 1-退货  2-换货  4-已发货仅退款  5-未发货仅退款
                    - reasonId (int): 申请售后的原因id
                    - reasonNameZh (str): 申请售后的原因名称
                    - status (int): 售后状态 1-待审核  2-待用户寄回  3-待商家收货  4-已完成  5-已取消6-已关闭  9-商家审核拒绝  9001-商家收货拒绝12-换货待商家发货  13-换货待用户确认收货  14-平台介入中
                    - userId (str): 用户id
                    - orderId (str): 包裹id
                    - applyTime (int): 售后申请时间（毫秒）
                    - updatedAt (int): 更新时间（毫秒）
                    - expireTime (int): 售后逾期时间（只提供待商家处理状态下的，其余的状态为-1)
                    - desc (str): 用户申请售后的备注
                    - returnsTag (int): 售后自动流程标记  1-命中平台极速退款  2-命中商家极速退款3-命中售后助手策略4-七天无理由自动审核32-命中发货后极速退款  35-命中发货后极速退款+售后助手策略36-命中发货后极速退款+七天无理由审核
                    - expectedRefundAmountYuan (float): 本次售后预期退的钱总额，元
                - totalCount (int): 当前条件下的售后总数
                - pageNo (int): 查询的页数
                - pageSize (int): 查询页的大小

        Examples:
            ```python
            # 获取所有待审核的售后请求
            response = client.after_sale.list_after_sale_infos(
                access_token,
                page_no=1,
                page_size=50,
                statuses=[1],  # 待审核
                time_type=1,
                start_time=1617724800000,
                end_time=1617811200000
            )

            # 获取特定包裹的售后请求
            response = client.after_sale.list_after_sale_infos(
                access_token,
                page_no=1,
                page_size=20,
                order_id="P617****941"
            )

            # 按售后类型和状态筛选
            response = client.after_sale.list_after_sale_infos(
                access_token,
                page_no=1,
                page_size=30,
                statuses=[1, 2, 3],  # 待处理状态
                return_types=[1, 2],  # 退货和换货
                time_type=2,
                start_time=1617724800000,
                end_time=1617726600000  # 更新时间30分钟范围
            )
            ```

        Note:
            这是新版本的售后列表API。包裹号和时间类型参数至少需要提供一个。
            使用时间类型1（创建时间）时，时间范围不能超过24小时。
            使用时间类型2（更新时间）时，时间范围不能超过30分钟。
        """
        request = ListAfterSaleInfosRequest(
            page_no=page_no,
            page_size=page_size,
            order_id=order_id,
            statuses=statuses,
            return_types=return_types,
            start_time=start_time,
            end_time=end_time,
            time_type=time_type,
        )
        return self._execute(request, response_model=ListAfterSaleInfosResponse)

    def get_after_sale_info(
        self,
        returns_id: str,
        need_negotiate_record: Optional[bool] = None,
    ) -> "BaseResponse[GetAfterSaleInfoResponse]":
        """获取售后详情（新）(API: afterSale.getAfterSaleInfo).

        获取售后详情的新版本API，提供更全面的售后信息和协商记录。

        Args:
            returns_id (str): 售后单号
            need_negotiate_record (Optional[bool]): 是否需要协商记录

        Returns:
            BaseResponse[GetAfterSaleInfoResponse]: 响应包含:
                - afterSaleInfo (AfterSaleInfo): 详细售后信息包括:
                    - returnsId (str): 售后id
                    - returnType (int): 售后类型
                    - reasonId (int): 申请售后的原因id
                    - reasonNameZh (str): 申请售后的原因名称
                    - status (int): 售后状态
                    - userId (str): 用户id
                    - orderId (str): 包裹id
                    - applyTime (int): 售后申请时间
                    - updatedAt (int): 更新时间
                    - expireTime (int): 售后逾期时间（只提供待商家处理状态下的，其余的状态为-1)
                    - returnAddress (dict): 退货地址信息:
                        - province (str): 省份
                        - city (str): 城市
                        - county (str): 区/县
                        - town (str): 镇/街道名称
                        - street (str): 镇/街道之下的详细地址
                        - phone (str): 手机
                        - name (str): 姓名
                        - fullAddress (str): 完整地址字符串
                    - proofPhotos (List[str]): 用户申请售后上传的图片列表
                    - desc (str): 用户申请售后的备注
                    - supportCarriageInsurance (bool): 是否支持运费险
                    - openAddressId (str): 提供给openapi的用户地址md5
                    - skus (List[dict]): 用户申请售后的商品:
                        - skuId (str): 商品id
                        - skuName (str): 商品名称
                        - image (str): 商品图片
                        - price (float): sku单价
                        - boughtCount (int): 购买件数
                        - appliedCount (int): 用户申请件数
                        - appliedTotalAmountYuan (float): 用户申请售后商品的钱
                        - scskucode (str): 小红书编码
                        - barcode (str): 条形码
                        - variants (List[dict]): 规格
                        - skuERPCode (str): 商品ERPCode
                    - exchangeSKUs (List[dict]): 用户换货的商品
                    - closeReasonZh (str): 商家拒绝售后的原因
                    - returnsTag (int): 0-未命中极速退款，1-命中平台极速退款，2-命中商家极速退款，3-命中售后助手
                    - appliedShipFeeAmountYuan (float): 用户申请售后运费金额，元
                    - appliedSkusAmountYuan (float): 用户申请售后商品金额，元
                    - expectedRefundAmountYuan (float): 本次售后预期退的钱总额，元
                    - refundAmountYuan (float): 实际已退款总额，包括定金，元
                    - refundStatus (int): 退款状态 108触发退款 1退款中 3退款失败 2退款成功 401已取消 101已创建 201待审核 301审核通过 302审核不通过 402自动关闭
                    - cargoStatus (int): 已发货仅退款申请时 选择的货物状态 0:未选择 1：未收到货 2:已收到货
                    - refundTime (int): 退款完成时间
                - logisticsInfo (dict): 物流信息包括:
                    - afterSale: 用户退货物流
                    - exchange: 商家换货物流
                    - order: 原订单物流
                - negotiateRecords (List[dict]): 售后协商记录（如果请求）

        Examples:
            ```python
            # 获取基本售后详情
            response = client.after_sale.get_after_sale_info(
                access_token, returns_id="R7488183140002901"
            )

            # 获取包含协商记录的详情
            response = client.after_sale.get_after_sale_info(
                access_token,
                returns_id="R7488183140002901",
                need_negotiate_record=True
            )

            # 访问详细信息
            after_sale = response.data.afterSaleInfo
            print(f"状态: {after_sale.status}")
            print(f"预期退款: {after_sale.expectedRefundAmountYuan} 元")
            for sku in after_sale.skus:
                print(f"商品: {sku.skuName} x{sku.appliedCount}")
            ```

        Note:
            这是新版本的售后详情API，提供完整的售后信息。
            设置need_negotiate_record=True可以包含完整的协商时间线和状态变更。
            响应包括详细的商品信息、物流跟踪和财务详情。
        """
        request = GetAfterSaleInfoRequest(
            returns_id=returns_id,
            need_negotiate_record=need_negotiate_record,
        )
        return self._execute(request, response_model=GetAfterSaleInfoResponse)

    def list_return_reject_reasons(
        self,
        returns_id: str,
        reject_reason_type: int,
    ) -> "BaseResponse[ListReturnRejectReasonResponse]":
        """获取售后拒绝原因 (API: afterSale.rejectReasons).

        获取特定售后请求的可用拒绝原因列表。
        该API提供预定义的拒绝原因，商家可在拒绝售后申请或收货确认时使用。

        Args:
            returns_id (str): 售后单ID
            reject_reason_type (int): 拒绝原因类型 1：审核拒绝 2：收货拒绝

        Returns:
            BaseResponse[ListReturnRejectReasonResponse]: 响应包含:
                - rejectReasons (List[RejectReason]): 拒绝原因列表包括:
                    - reasonType (int): 拒绝理由类型 0：拒绝售后 1：拒绝收货
                    - reasonId (int): 拒绝原因ID
                    - reasonName (str): 拒绝原因名称

        Examples:
            ```python
            # 获取审核拒绝原因
            response = client.after_sale.list_return_reject_reasons(
                access_token,
                returns_id="R7488183140002901",
                reject_reason_type=1
            )

            # 获取收货拒绝原因
            response = client.after_sale.list_return_reject_reasons(
                access_token,
                returns_id="R7488183140002901",
                reject_reason_type=2
            )

            # 处理拒绝原因
            for reason in response.data.rejectReasons:
                print(f"原因 {reason.reasonId}: {reason.reasonName}")
            ```

        Note:
            在调用audit_returns()或confirm_receive()进行拒绝操作之前，
            使用此API获取有效的拒绝原因ID。返回的reasonId值必须在后续拒绝操作中使用。
        """
        request = ListReturnRejectReasonRequest(
            returns_id=returns_id,
            reject_reason_type=reject_reason_type,
        )
        return self._execute(request, response_model=ListReturnRejectReasonResponse)

    def list_after_sale(
        self,
        start_time: int,
        end_time: int,
        time_type: int,
        status: Optional[int] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        use_has_next: Optional[bool] = None,
        reason_id: Optional[int] = None,
        return_type: Optional[int] = None,
    ) -> "BaseResponse[GetAfterSaleListResponse]":
        """获取售后列表（旧）(API: afterSale.listAfterSaleApi).

        使用旧版API格式获取售后请求列表。
        这是较旧版本的售后列表API，为了兼容性而保留。对于新实现，建议使用list_after_sale_infos()。

        Args:
            start_time (int): 查询时间起点
            end_time (int): 查询时间终点
            time_type (int): 时间类型，1：根据创建时间查询 end-start<=24h；2：根据更新时间查询 end-start<=30min
            status (Optional[int]): 售后状态 1：待审核；2:待用户寄回；3:待收货；4:完成；5:取消；6:关闭；9:拒绝；9001：商家收货拒绝；11：换货转退款；12:订单商家已确认收货，等待商家发货；13:订单商家已发货，等待用户确认收货。不传默认全部；14：平台介入中
            page_no (Optional[int]): 返回页码 默认 1，页码从 1 开始 PS：当前采用分页返回，数量和页数会一起传，如果不传，则采用 默认值
            page_size (Optional[int]): 返回数量，默认50最大100
            use_has_next (Optional[bool]): 是否返回所有数据,true 不返会total 返回 hasNext = true 表示仍有数据，false 返回total
            reason_id (Optional[int]): 编号
            return_type (Optional[int]): 售后类型 不传/0:全部；1:退货退款；2:换货；3:仅退款(old) 4:仅退款(new) 理论上不会有3出现；5:未发货仅退款

        Returns:
            BaseResponse[GetAfterSaleListResponse]: 响应包含:
                - total (int): 查询到的总数，useHasNext=true时为0
                - pageNo (int): 当前页数
                - pageSize (int): 页大小
                - haxNext (bool): 是否有下一页
                - simpleAfterSaleList (List[SimpleAfterSaleDTO]): 售后信息列表:
                    - returnsId (str): 售后ID
                    - returnType (int): 售后类型
                    - reasonId (int): 售后原因ID
                    - reason (str): 售后原因
                    - status (int): 售后状态 1：待审核；2:待用户寄回；3:待收货；4:完成；5:取消；6:关闭；9:拒绝；9001：商家收货拒绝；11：换货转退款；12:订单商家已确认收货，等待商家发货；13:订单商家已发货，等待用户确认收货。不传默认全部；14：平台介入中
                    - subStatus (int): 售后子状态 301-待审核 302-快递已签收 304-收货异常
                    - receiveAbnormalType (int): 收货异常类型 1:商家已开工单 2:仓库质检异常 3:收货地异常 4:寄回订单物流超时 5:仓库反向创建退货 6:快递轨迹异常 7:拒收退仓超时 8:退款金额超限 9:收货地不一致 10:仓库质检假货 11:已退款，未收货 21:未收到货 22:退货数量不符 23:退货商品不符 24:退货质检异常 25:其他
                    - orderId (str): 订单ID
                    - exchangeOrderId (str): 换货订单ID
                    - userId (str): 用户ID
                    - createdTime (int): 售后创建时间戳（毫秒）
                    - returnExpressNo (str): 售后快递单号
                    - returnExpressCompany (str): 售后快递公司
                    - returnExpressCompanyCode (str): 退货快递公司编号
                    - returnAddress (str): 售后退货地址
                    - shipNeeded (int): 是否需要寄回 1-需要 0-不需要
                    - refunded (bool): 是否已退款
                    - refundStatus (int): 退款状态 108触发退款 1退款中 3退款失败 2退款成功 401已取消 101已创建 201待审核 301审核通过 302审核不通过 402自动关闭
                    - autoReceiveDeadline (int): 自动确认收货时间
                    - useFastRefund (bool): 是否急速退款，已经废弃
                    - updateTime (int): 售后更新时间戳（毫秒）
                    - expectedRefundAmount (float): 预期退款金额，单位元
                - maxPageNo (int): 最大页码数

        Examples:
            ```python
            # 按创建时间获取所有售后请求
            response = client.after_sale.list_after_sale(
                access_token,
                start_time=1617724800000,
                end_time=1617811200000,
                time_type=1,
                page_no=1,
                page_size=50
            )

            # 按状态和类型筛选
            response = client.after_sale.list_after_sale(
                access_token,
                start_time=1617724800000,
                end_time=1617728400000,
                time_type=2,  # 更新时间
                status=1,    # 待审核
                return_type=1,  # 退货退款
                use_has_next=True
            )
            ```

        Note:
            这是旧版本的售后列表API。时间约束适用：
            - 创建时间查询：最多24小时范围
            - 更新时间查询：最多30分钟范围
            对于新实现，建议使用list_after_sale_infos()，它提供增强功能和更详细的信息。
        """
        request = GetAfterSaleListRequest(
            start_time=start_time,
            end_time=end_time,
            time_type=time_type,
            status=status,
            page_no=page_no,
            page_size=page_size,
            use_has_next=use_has_next,
            reason_id=reason_id,
            return_type=return_type,
        )
        return self._execute(request, response_model=GetAfterSaleListResponse)

    def confirm_receive(
        self,
        returns_id: str,
        action: int,
        reason: Optional[int] = None,
        description: Optional[str] = None,
    ) -> "BaseResponse[str]":
        """售后确认收货（新）(API: afterSale.confirmReceive).

        处理商家对收到的退货商品的决定。
        此API允许商家确认收货、拒绝收货或请求延期。

        Args:
            returns_id (str): 售后id
            action (int): 操作类型，1：确认收货；2：拒绝；3：延期
            reason (Optional[int]): 拒绝时必填，需要通过afterSale.rejectReasons获取原因传参，非法参数将拦截请求
            description (Optional[str]): 拒绝原因描述

        Returns:
            BaseResponse[str]: 响应包含:
                - 操作确认消息
                - 成功状态指示

        Examples:
            ```python
            # 确认收到退货商品
            response = client.after_sale.confirm_receive(
                access_token,
                returns_id="R7488183140002901",
                action=1  # 确认收货
            )

            # 带原因拒绝收货
            # 首先获取有效拒绝原因
            reasons_response = client.after_sale.list_return_reject_reasons(
                access_token,
                returns_id="R7488183140002901",
                reject_reason_type=2  # 收货拒绝原因
            )
            reason_id = reasons_response.data.rejectReasons[0].reasonId

            # 然后使用有效原因拒绝
            response = client.after_sale.confirm_receive(
                access_token,
                returns_id="R7488183140002901",
                action=2,  # 拒绝
                reason=reason_id,
                description="商品与原订单不符"
            )

            # 请求延期
            response = client.after_sale.confirm_receive(
                access_token,
                returns_id="R7488183140002901",
                action=3  # 请求延期
            )
            ```

        Note:
            当拒绝收货(action=2)时，必须提供有效的原因ID，
            该ID需从 list_return_reject_reasons() 中获取（reject_reason_type=2）。
            无效的原因ID将导致请求被拒绝。此操作将影响售后流程并触发给客户的通知。
        """
        request = ConfirmReceiveRequest(
            returns_id=returns_id,
            action=action,
            reason=reason,
            description=description,
        )
        return self._execute(request)

    def audit_returns(
        self,
        returns_id: str,
        action: int,
        reason: Optional[int] = None,
        description: Optional[str] = None,
        message: Optional[str] = None,
        receiver_info: Optional[AuditReturnsReceiverInfo] = None,
    ) -> "BaseResponse[str]":
        """售后审核（新）(API: afterSale.auditReturns).

        处理商家对售后申请的审核决定。此API允许商家同意直接退款、同意退货或拒绝售后请求，
        并可以配置适当的拒绝原因和退货地址。

        Args:
            returns_id (str): 售后订单ID
            action (int): 操作类型，1：同意直接退款 (退货退款、换货不适用)；2：同意寄回(仅退款不适用)；3：拒绝
            reason (Optional[int]): 拒绝原因, 需要通过afterSale.rejectReasons获取原因传参，非法参数将拦截请求
            description (Optional[str]): 拒绝原因描述, 当拒绝原因为"其他"时必填
            message (Optional[str]): 给用户留言, 当操作类型为"同意寄回"时字段有效
            receiver_info (Optional[dict]): 寄回地址信息, 同意寄回时必填:
                - sellerAddressRecordId (int): 商家地址库Id，同意寄回时必填，通过common.getAddressRecord获取
                - 其他地址字段已废弃，但可以为兼容性而包含

        Returns:
            BaseResponse[str]: 响应包含:
                - 操作确认消息
                - 成功状态指示

        Examples:
            ```python
            # 同意直接退款
            response = client.after_sale.audit_returns(
                access_token,
                returns_id="R7488183140002901",
                action=1  # 同意直接退款
            )

            # 同意退货并提供地址
            receiver_info = {
                "sellerAddressRecordId": 123456
            }
            response = client.after_sale.audit_returns(
                access_token,
                returns_id="R7488183140002901",
                action=2,  # 同意寄回
                message="请仔细包装并使用原包装。",
                receiver_info=receiver_info
            )

            # 拒绝售后请求
            # 首先获取有效拒绝原因
            reasons_response = client.after_sale.list_return_reject_reasons(
                access_token,
                returns_id="R7488183140002901",
                reject_reason_type=1  # 审核拒绝原因
            )
            reason_id = reasons_response.data.rejectReasons[0].reasonId

            # 然后使用有效原因拒绝
            response = client.after_sale.audit_returns(
                access_token,
                returns_id="R7488183140002901",
                action=3,  # 拒绝
                reason=reason_id,
                description="请求不符合退货政策要求"
            )
            ```

        Note:
            - 当同意退货(action=2)时，需要提供包含有效sellerAddressRecordId的receiver_info。
              通过common.getAddressRecord API获取商家地址。
            - 当拒绝(action=3)时，使用从 list_return_reject_reasons() 获取的有效原因ID（reject_reason_type=1）。
            - 直接退款(action=1)不适用于需要实物退货的退货/换货请求。
            - message字段仅对同意退货的情况有效。
        """
        request = AuditReturnsRequest(
            returns_id=returns_id,
            action=action,
            reason=reason,
            description=description,
            message=message,
            receiver_info=receiver_info,
        )
        return self._execute(request)

    def get_after_sale_detail(
        self,
        after_sale_id: str,
    ) -> "BaseResponse[GetAfterSaleDetailResponse]":
        """售后详情（旧）(API: afterSale.getAfterSaleDetail).

        使用旧版API格式获取特定售后请求的详细信息。
        这是较旧版本的售后详情API。对于新实现，建议使用get_after_sale_info()，它提供增强的信息。

        Args:
            after_sale_id (str): 售后id

        Returns:
            BaseResponse[GetAfterSaleDetailResponse]: 响应包含详细售后信息:
                - returnsId (str): 售后id
                - returnType (int): 退货类型 1-退货退款, 2-换货, 3:仅退款(old) 4:仅退款(new) 理论上不会有3出现 5:未发货仅退款
                - reasonId (int): 售后原因id
                - reason (str): 售后原因说明
                - status (int): 售后状态 1：待审核；2:待用户寄回；3:待收货；4:完成；5:取消；6:关闭；9:拒绝；9001：商家收货拒绝；11：换货转退款；12:包裹商家已确认收货，等待商家发货；13:包裹商家已发货，等待用户确认收货。不传默认全部；14：平台介入中
                - subStatus (int): 售后子状态 301-待审核 302-快递已签收 304-收货异常
                - receiveAbnormalType (int): 收货异常类型 1:商家已开工单 2:仓库质检异常 3:收货地异常 4:寄回包裹物流超时 5:仓库反向创建退货 6:快递轨迹异常 7:拒收退仓超时 8:退款金额超限 9:收货地不一致 10:仓库质检假货 11:已退款，未收货 21:未收到货 22:退货数量不符 23:退货商品不符 24:退货质检异常 25:其他
                - orderId (str): 订单id
                - exchangeOrderId (str): 换货订单id
                - userId (str): 用户id
                - createdAt (int): 创建时间
                - returnExpressNo (str): 售后订单快递单号
                - returnExpressCompany (str): 售后订单快递公司
                - returnAddress (str): 售后寄回地址
                - shipNeeded (int): 是否需要寄回 0-否 1-是 -1-全部
                - refunded (bool): 是否已退款
                - refundStatus (int): 退款状态
                - autoReceiveDeadline (int): 超时自动确认收货的时间
                - useFastRefund (bool): 是否急速退款 0-否 1-是 -1-全部
                - proofPhotos (List[str]): 照片凭证
                - desc (str): 描述
                - note (str): 备注
                - refundTime (int): 退款时间
                - fillExpressTime (int): 填写退货快递单时间
                - expressSignTime (int): 退货快递签收时间
                - skus (List[dict]): 售后商品列表及相关信息
                - 其他包括用户信息、订单详情、物流信息、退款状态和时间戳的字段

        Examples:
            ```python
            # 获取售后详情
            response = client.after_sale.get_after_sale_detail(
                access_token, after_sale_id="R7488183140002901"
            )

            # 访问基本信息
            detail = response.data
            print(f"退货类型: {detail.returnType}")
            print(f"状态: {detail.status}")
            print(f"原因: {detail.reason}")
            ```

        Note:
            这是旧版本的售后详情API。对于新实现，
            建议使用get_after_sale_info()，它提供更全面的信息，
            包括协商记录、增强的物流详情和更好的结构化响应数据。
        """
        request = GetAfterSaleDetailRequest(after_sale_id=after_sale_id)
        return self._execute(request, response_model=GetAfterSaleDetailResponse)

    def set_returns_abnormal(
        self,
        returns_id: str,
        abnormal_type: Optional[int] = None,
        abnormal_note: Optional[str] = None,
    ) -> "BaseResponse[str]":
        """设置退货异常状态 (API: afterSale.setReturnsAbnormal).

        在退货过程中发现问题时，标记售后退货为异常状态。
        此API用于报告和处理售后流程中的异常情况。

        Args:
            returns_id (str): 售后id
            abnormal_type (Optional[int]): 异常类型编码，具体类型编码应从平台文档或支持团队获取，因业务场景而异
            abnormal_note (Optional[str]): 异常情况的详细说明

        Returns:
            BaseResponse[str]: 响应包含:
                - 操作确认消息
                - 成功状态指示

        Examples:
            ```python
            # 报告带类型和说明的异常退货
            response = client.after_sale.set_returns_abnormal(
                access_token,
                returns_id="R7488183140002901",
                abnormal_type=1,
                abnormal_note="包裹在退货运输过程中损坏"
            )

            # 仅报告带说明的异常退货
            response = client.after_sale.set_returns_abnormal(
                access_token,
                returns_id="R7488183140002901",
                abnormal_note="退货包裹中缺少商品"
            )
            ```

        Note:
            此API用于标记售后退货过程中的异常情况。
            常见场景包括包裹损坏、商品缺失、退货商品质量问题或物流问题。
            异常状态有助于跟踪和解决可能影响正常售后流程的问题。
            具体的abnormal_type编码请联系平台支持获取，因业务场景而异。
        """
        request = ReturnsAbnormalRequest(
            returns_id=returns_id,
            abnormal_type=abnormal_type,
            abnormal_note=abnormal_note,
        )
        return self._execute(request)

    def receive_and_ship(
        self,
        returns_id: str,
        express_company_code: str,
        express_no: str,
    ) -> "BaseResponse[str]":
        """售后换货确认收货并发货 (API: afterSale.receiveAndShip).

        处理换货流程，确认收到退货并立即发送替换商品。
        此API将收货确认和换货发货操作结合起来以提高效率。

        Args:
            returns_id (str): 售后id
            express_company_code (str): 物流公司编码
            express_no (str): 物流单号

        Returns:
            BaseResponse[str]: 响应包含:
                - error_code (int): 错误码（0表示成功）
                - success (bool): 是否成功
                - data (object): 返回信息

        Examples:
            ```python
            # 确认收货并发送换货商品
            response = client.after_sale.receive_and_ship(
                access_token,
                returns_id="R7488183140002901",
                express_company_code="YTO",
                express_no="YT1234567890123"
            )

            # 检查操作结果
            if response.success:
                print("换货发货处理成功")
            else:
                print(f"错误: {response.error_code}")
            ```

        Note:
            此API专用于换货订单，商家需要确认收到退货并同时发送替换商品。
            express_company_code和express_no都是必填字段。
            物流公司编码必须是平台支持的有效编码。
            使用common.get_express_company_list()获取有效的物流公司编码。
        """
        request = ReceiveAndShipRequest(
            returns_id=returns_id,
            express_company_code=express_company_code,
            express_no=express_no,
        )
        return self._execute(request)
