"""Order management client for Xiaohongshu e-commerce API."""

from typing import Optional, List

from ..models.base import BaseResponse
from ..models.order import (
    BatchApproveSubscribeOrdersRequest,
    BatchBindOrderSkuIdentifyCodeInfoRequest,
    BatchBindOrderSkuIdentifyCodeInfoResponse,
    BondedPaymentRecordRequest,
    CreateTransferBatchRequest,
    CreateTransferBatchResponse,
    GetCustomInfoRequest,
    GetCustomsInfoResponse,
    GetKosDataRequest,
    GetKosDataResponse,
    GetOrderDeclareRequest,
    GetOrderDeclareInfoResponse,
    GetOrderDetailRequest,
    GetOrderDetailResponse,
    GetOrderListRequest,
    GetOrderListResponse,
    GetOrderReceiverInfoRequest,
    GetOrderReceiverInfoResponse,
    GetOrderTrackRequest,
    GetOrderTrackingResponse,
    GetSupportedPortListRequest,
    GetSupportedPortListResponse,
    ModifyCustomsStatusRequest,
    ModifyOrderExpressRequest,
    ModifySellerMarkRequest,
    OrderDeliverRequest,
    SyncCustomsInfoRequest,
)
from .base import SyncSubClient


class OrderClient(SyncSubClient):
    """Synchronous client for order APIs."""

    def get_order_list(
        self,
        start_time: int,
        end_time: int,
        time_type: int,
        order_type: Optional[int] = None,
        order_status: Optional[int] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> BaseResponse[GetOrderListResponse]:
        """订单列表 (API: order.getOrderList).

        获取订单列表，支持分页和筛选功能。
        此API提供订单管理和处理所需的基本订单信息。

        Args:
            start_time (int): 时间范围起点 (Unix时间戳，必填)。
            end_time (int): 时间范围终点 (Unix时间戳，必填)。
            time_type (int): startTime/endTime对应的时间类型，1 创建时间 限制 end-start<=24h、2 更新时间 限制 end-start<=30min 倒序拉取 最后一页到第一页 (必填)。
            order_type (Optional[int]): 订单类型，0/null 全部 1 现货 normal 2 定金预售 3 全款预售(废弃) 4 全款预售(新) 5 换货补发。
            order_status (Optional[int]): 订单状态，0全部 1已下单待付款 2已支付处理中 3清关中 4待发货 5部分发货 6待收货 7已完成 8已关闭 9已取消 10换货申请中。
            page_no (Optional[int]): 页码，默认1，限制100。
            page_size (Optional[int]): 查询总数，默认50，限制100。

        Returns:
            BaseResponse[GetOrderListResponse]: 响应包含:
                - total (int): 订单总数
                - pageNo (int): 当前页数 请求参数中的值
                - pageSize (int): 页大小 请求参数中的值
                - maxPageNo (int): 最大页码数 方便 直接从最后一页拉数据
                - orderList (List[OrderSimpleDetail]): 订单信息列表，包含:
                    - orderId (str): 订单号
                    - orderType (int): 订单类型，1普通 2定金预售 3全款预售(废弃) 4全款预售(新) 5换货补发
                    - orderStatus (int): 订单状态，1已下单待付款 2已支付处理中 3清关中 4待发货 5部分发货 6待收货 7已完成 8已关闭 9已取消 10换货申请中
                    - orderAfterSalesStatus (int): 售后状态，1无售后 2售后处理中 3售后完成 4售后拒绝 5售后关闭 6平台介入中 7售后取消
                    - cancelStatus (int): 申请取消状态，0未申请取消 1取消处理中
                    - createdTime (int): 创建时间 单位ms
                    - paidTime (int): 支付时间 单位ms
                    - updateTime (int): 更新时间 单位ms
                    - deliveryTime (int): 订单发货时间 单位ms
                    - cancelTime (int): 订单取消时间 单位ms
                    - finishTime (int): 订单完成时间 单位ms
                    - promiseLastDeliveryTime (int): 承诺最晚发货时间 单位ms
                    - planInfoId (str): 物流方案id
                    - planInfoName (str): 物流方案名称
                    - receiverCountryId/Name (str): 收件人国家id/目前仅 中国
                    - receiverProvinceId/Name (str): 收件人省份id/收件人省份
                    - receiverCityId/Name (str): 收件人城市id/收件人城市
                    - receiverDistrictId/Name (str): 收件人区县id/收件人区县名称
                    - customerRemark (str): 用户备注
                    - sellerRemark (str): 商家标记备注
                    - sellerRemarkFlag (int): 商家标记优先级，ark订单列表展示旗子颜色 1灰旗 2红旗 3黄旗 4绿旗 5蓝旗 6紫旗
                    - originalOrderId (str): 原始订单编号，换货订单的原订单
                    - logistics (str): 物流模式red_express三方备货直邮(备货海外仓),red_domestic_trade(三方备货内贸),red_standard(三方备货保税仓),red_auto(三方自主发货),red_box(三方小包),red_bonded(三方保税)
                    - orderTagList (List[str]): 订单标签列表 NEW_YEAR 新年礼 PLATFORM_DECLARE 平台报备 SELLER_DECLARE 商家报备 CONSULT 协商发货 MODIFIED_ADDR 已改地址 MODIFIED_PRICE 已改价 NO_LOGISTICS_SHIP 无物流发货 PRINTED 部分打单/已打单 URGENT_SHIP 催发货 QIC QIC质检 SAMPLE 拿样 HOME_DELIVERY 送货上门 LACK_GOOD 缺货 EXPLODE 发生现货爆单的订单 EXEMPT 发生现货爆单享受豁免 CERTIFICATION_WAREHOUSE 认证仓 COUNTRY_SUBSIDY: 国家补贴 CITY_SUBSIDY:城市补贴 BUY_AGENT:代购

        Examples:
            >>> # Get orders by creation time
            >>> response = client.order.get_order_list(
            ...     access_token,
            ...     start_time=1612518379,
            ...     end_time=1612604779,
            ...     time_type=1,
            ...     order_status=4,  # Pending shipment
            ...     page_no=1,
            ...     page_size=50
            ... )

            >>> # Get recently updated orders
            >>> response = client.order.get_order_list(
            ...     access_token,
            ...     start_time=1612518379,
            ...     end_time=1612520179,  # 30 min window
            ...     time_type=2,  # Update time
            ...     page_no=1,
            ...     page_size=100
            ... )

        Note:
            使用timeType=2（更新时间）时，时间范围限制为30分钟，
            结果按倒序返回（从最后一页到第一页）。
            对于创建时间查询（timeType=1），最大范围为24小时。
        """
        request = GetOrderListRequest(
            start_time=start_time,
            end_time=end_time,
            time_type=time_type,
            order_type=order_type,
            order_status=order_status,
            page_no=page_no,
            page_size=page_size,
        )
        request.method = "order.getOrderList"
        return self._execute(request, response_model=GetOrderListResponse)

    def get_order_detail(
        self,
        order_id: Optional[str] = None,
        order_no: Optional[str] = None,
    ) -> BaseResponse[GetOrderDetailResponse]:
        """获取订单详情 (API: order.getOrderDetail).

        获取完整的订单信息，包括商品、价格、物流、
        及所有订单相关的元数据。

        Args:
            order_id (Optional[str]): 订单号。
            order_no (Optional[str]): 订单号。

        Returns:
            BaseResponse[GetOrderDetailResponse]: 响应包含完整订单详情:
                - orderId (str): 订单号
                - orderType (int): 订单类型，1现货 2定金预售 3全款预售(废弃) 4全款预售(新) 5补发
                - orderStatus (int): 订单状态，1已下单待付款 2已支付处理中 3清关中 4待发货 5部分发货 6待收货 7已完成 8已关闭 9已取消 10换货申请中
                - orderAfterSalesStatus (int): 售后状态，1无售后 2售后处理中 3售后完成 4售后拒绝 5售后关闭 6平台介入中 7售后取消
                - cancelStatus (int): 申请取消状态，0未申请取消 1取消处理中
                - createdTime (int): 创建时间 单位ms
                - paidTime (int): 支付时间 单位ms
                - updateTime (int): 更新时间 单位ms
                - deliveryTime (int): 订单发货时间 单位ms
                - cancelTime (int): 订单取消时间 单位ms
                - finishTime (int): 订单完成时间 单位ms
                - promiseLastDeliveryTime (int): 承诺最晚发货时间 单位ms
                - planInfoId (str): 物流方案id
                - planInfoName (str): 物流方案名称
                - receiverCountryId/Name (str): 收件人国家id/目前仅 中国
                - receiverProvinceId/Name (str): 收件人省份id/收件人省份
                - receiverCityId/Name (str): 收件人城市id/收件人城市
                - receiverDistrictId/Name (str): 收件人区县id/收件人区县名称
                - customerRemark (str): 用户备注
                - sellerRemark (str): 商家标记备注
                - sellerRemarkFlag (int): 商家标记优先级，ark订单列表展示旗子颜色 1灰旗 2红旗 3黄旗 4绿旗 5蓝旗 6紫旗
                - presaleDeliveryStartTime/EndTime (int): 预售最早/最晚发货时间 单位ms
                - skuList (List[OrderSkuDTOV3]): sku列表 相同sku聚合 金额为价格总和 单位 分，包含详细商品信息:
                    - skuId (str): 商品id
                    - skuName (str): 商品名称
                    - erpcode (str): 商家编码(若为组合品，暂不支持组合品的商家编码，但skuDetailList会返回子商品商家编码)
                    - skuSpec (str): 规格
                    - skuImage (str): 商品图片url
                    - skuQuantity (int): 商品数量
                    - skuDetailList (List[OrderSkuDetailDTO]): 商品sku信息列表,单品非渠道商品为自身信息，组合品为子商品信息，多包组和渠道商品为其对应非渠道单品信息
                    - totalPaidAmount (int): 总支付金额（考虑总件数）商品总实付
                    - totalMerchantDiscount (int): 商家承担总优惠
                    - totalRedDiscount (int): 平台承担总优惠
                    - totalTaxAmount (int): 商品税金
                    - totalNetWeight (int): 商品总净重
                    - skuTag (int): 是否赠品，1 赠品 0 普通商品
                    - isChannel (bool): 是否是渠道商品
                    - deliveryMode (int): 是否支持无物流发货, 1: 支持无物流发货 0：不支持无物流发货
                    - kolId/kolName (str): 达人id/达人名称(通过直播间下单 或者达人主页小清单下单才有值,直播间商品加到购物车下单 此字段为空)
                    - skuAfterSaleStatus (int): Sku售后状态 1无售后 2售后处理中 3售后完成 4售后拒绝 5售后关闭 6平台介入中 7售后取消
                    - skuIdentifyCodeInfo (object): 商品序列号等信息，仅部分类目的国补订单存在
                    - itemId/itemName (str): 商品ID/商品名称
                - originalOrderId (str): 原始关联订单号(退换订单的原订单)
                - totalNetWeightAmount (int): 订单商品总净重 单位g
                - totalPayAmount (int): 订单实付金额(包含运费和定金) 单位分
                - totalShippingFree (int): 订单实付运费 单位分
                - unpack (bool): 是否拆包 true已拆包 false未拆包
                - expressTrackingNo (str): 快递单号
                - expressCompanyCode (str): 快递公司编码
                - receiverName/Phone/Address (str): 收件人姓名/收件人手机/收件人地址 暂不返回 详情通过getOrderReceiverInfo获取
                - boundExtendInfo (object): 三方保税节点 金额单位 分
                - transferExtendInfo (object): 小包转运节点
                - openAddressId (str): 收件人姓名+手机+地址等计算得出，用来查询收件人详情
                - simpleDeliveryOrderList (List): 拆包信息节点
                - logistics (str): 物流模式red_express三方备货直邮(备货海外仓),red_domestic_trade(三方备货内贸),red_standard(三方备货保税仓),red_auto(三方自主发货),red_box(三方小包),red_bonded(三方保税)
                - totalDepositAmount (int): 订单定金 单位分
                - totalMerchantDiscount (int): 商家承担总优惠金额 单位分
                - totalRedDiscount (int): 平台承担总优惠金额 单位分
                - merchantActualReceiveAmount (int): 商家实收(=用户支付金额+定金+平台优惠) 单位分
                - totalChangePriceAmount (int): 改价总金额 单位分
                - paymentType (int): 支付方式 1：支付宝 2：微信 3：apple 内购 4：apple pay 5：花呗分期 7：支付宝免密支付 8：云闪付 -1：其他
                - shopId/shopName (str): 店铺id/店铺名称
                - whcode (str): 仓code
                - userId (str): 用户id
                - orderTagList (List[str]): 订单标签列表
                - logisticsMode (int): 物流模式 1: 普通内贸 2：保税bbc 3: 直邮bc 4:行邮cc
                - customsCode (str): 口岸code
                - outPromotionAmount (int): 支付渠道优惠金额 单位分
                - outTradeNo (str): 三方支付渠道单号
                - subsidySupplierId/Name (str): 国补供应商id/国补供应商名称
                - subsidyWpServiceCode (str): 国补顺丰微派任务编码
                - subsidySkuIdentifyCodeRequiredInfo (object): 国补商品标识信息发货必传条件

        Examples:
            >>> # Get order details by order ID
            >>> response = client.order.get_order_detail(
            ...     access_token, order_id="P194****4183"
            ... )
            >>> order_detail = response.data
            >>> print(f"Order status: {order_detail.orderStatus}")
            >>> print(f"Total amount: {order_detail.totalPayAmount / 100} yuan")

        Note:
            收件人个人信息（姓名、手机、地址）在此API中不返回。
            请使用 get_order_receiver_info() 获取敏感的收件人信息。
            所有金额以分为单位（除以100得到元金额）。
        """
        request = GetOrderDetailRequest(
            order_id=order_id,
            order_no=order_no,
        )
        request.method = "order.getOrderDetail"
        return self._execute(request, response_model=GetOrderDetailResponse)

    def batch_bind_sku_identify_info(
        self,
        order_sku_identify_code_info_list: List[dict],
    ) -> BaseResponse[BatchBindOrderSkuIdentifyCodeInfoResponse]:
        """批量上传国补订单序列号等信息 (API: order.batchBindSkuIdentifyInfo).

                为政府补贴订单批量上传商品识别信息，包括序列号、条形码、
        IMEI等代码。特定商品类别在补贴项目中为必需。

                Args:
                    order_sku_identify_code_info_list (List[dict]): 订单商品信息列表 (必填):
                        每个项目包含:
                        - packageId (str): 订单号
                        - skuIdentifyCodeInfo (dict): 商品身份信息 (必填):
                            - sNCode (str): 序列号 (必填)
                            - barCode (str): 条形码 (必填)
                            - iMEI2Code (str): i1码 (必填)
                            - iMEI1Code (str, optional): i1码

                Returns:
                    BaseResponse[BatchBindOrderSkuIdentifyCodeInfoResponse]: 响应包含:
                        - error_msg (str): 错误信息
                        - error_code (int): 错误码（0为成功）
                        - success (bool): 整体操作是否成功
                        - data (object): 结果数据:
                            - res (List): 每个订单的结果:
                                - packageId (str): 订单号
                                - success (bool): 该订单是否成功
                                - msg (str): 失败时的错误描述

                Examples:
                    >>> # Upload identification codes for single order
                    >>> identify_info = {
                    ...     "sNCode": "sncode测试001",
                    ...     "barCode": "barcode测试001",
                    ...     "iMEI1Code": "imei1code测试001",
                    ...     "iMEI2Code": "imei2code测试001"
                    ... }
                    >>> order_info = {
                    ...     "packageId": "P763821122427443521",
                    ...     "skuIdentifyCodeInfo": identify_info
                    ... }
                    >>> response = client.order.batch_bind_sku_identify_info(
                    ...     access_token, order_sku_identify_code_info_list=[order_info]
                    ... )
                    >>>
                    >>> for result in response.data.res:
                    ...     if result.success:
                    ...         print(f"Order {result.packageId}: Success")
                    ...     else:
                    ...         print(f"Order {result.packageId}: Failed - {result.msg}")

                    >>> # Upload for multiple orders
                    >>> orders_info = [
                    ...     {
                    ...         "packageId": "P763821122427443521",
                    ...         "skuIdentifyCodeInfo": {
                    ...             "sNCode": "SN001",
                    ...             "barCode": "BC001",
                    ...             "iMEI2Code": "IMEI2_001"
                    ...         }
                    ...     },
                    ...     {
                    ...         "packageId": "P763821122427443522",
                    ...         "skuIdentifyCodeInfo": {
                    ...             "sNCode": "SN002",
                    ...             "barCode": "BC002",
                    ...             "iMEI2Code": "IMEI2_002"
                    ...         }
                    ...     }
                    ... ]
                    >>> response = client.order.batch_bind_sku_identify_info(
                    ...     access_token, order_sku_identify_code_info_list=orders_info
                    ... )

                Common Error Messages:
                    - "已完结的国补订单禁止上传商品序列号等信息": 已完成的补贴订单不能上传识别代码
                    - 订单状态必须允许上传识别代码

                Note:
                    - 仅适用于政府补贴订单
                    - 特定商品类别为必需（电子产品、家电）
                    - 必须在订单完成前上传
                    - 序列号必须唯一有效
                    - 手机设备需要IMEI码
        """
        request = BatchBindOrderSkuIdentifyCodeInfoRequest(
            order_sku_identify_code_info_list=order_sku_identify_code_info_list
        )
        request.method = "order.batchBindSkuIdentifyInfo"
        return self._execute(
            request, response_model=BatchBindOrderSkuIdentifyCodeInfoResponse
        )

    def resend_bonded_payment_record(
        self,
        order_id: str,
        customs_type: str,
    ) -> BaseResponse[str]:
        """跨境重推支付单 (API: order.resendBondedPaymentRecord).

        为初次海关申报失败的跨境保税仓订单
        重新发送支付记录信息到海关系统。

        Args:
            order_id (str): 订单号 (必填)。
            customs_type (str): 海关类型 (必填):
                - "zongshu": 总署海关
                - "local": 地方海关

        Returns:
            BaseResponse[str]: 响应包含:
                - success (bool): 是否成功
                - msg (str): 返回信息或错误描述

        Examples:
            >>> # Resend to General Administration of Customs
            >>> response = client.order.resend_bonded_payment_record(
            ...     access_token,
            ...     order_id="P61***941",
            ...     customs_type="zongshu"
            ... )
            >>> if response.data.success:
            ...     print("Payment record resent successfully")
            ... else:
            ...     print(f"Failed to resend: {response.data.msg}")

            >>> # Resend to local customs
            >>> response = client.order.resend_bonded_payment_record(
            ...     access_token,
            ...     order_id="P61***942",
            ...     customs_type="local"
            ... )

        Note:
            - 仅适用于跨境保税仓订单
            - 订单必须有有效的支付信息
            - 海关类型必须与原始申报一致
            - 可能需要特定的商家授权
            - 仅在海关清关待处理时可使用
        """
        request = BondedPaymentRecordRequest(
            order_id=order_id,
            customs_type=customs_type,
        )
        request.method = "order.resendBondedPaymentRecord"
        return self._execute(request, response_model=str)

    def sync_item_customs_info(
        self,
        item_id: str,
        barcode: str,
        customs_info: dict,
    ) -> BaseResponse[str]:
        """同步商品海关信息 (API: order.syncItemCustomsInfo).

        将商品海关信息同步到平台海关数据库，确保跨境申报所需的
        海关数据准确且最新。

        Args:
            item_id (str): 商品ID (必填)。
            barcode (str): 商品条形码 (必填)。
            customs_info (dict): 海关信息 (必填):
                - hsCode (str): HS编码（海关税则号）
                - customsName (str): 海关申报名称
                - netWeight (float): 净重（克）
                - grossWeight (float): 毛重（克）
                - unit (str): 计量单位
                - taxRate (float): 税率（小数格式）
                - originCountry (str): 原产国
                - brand (str): 品牌
                - model (str): 型号
                - specifications (str): 规格

        Returns:
            BaseResponse[str]: 响应包含:
                - error_code (int): 错误码，0表示成功
                - success (bool): 同步是否成功
                - data (object): 同步操作结果信息

        Note:
            - 跨境商品销售前必需同步海关信息
            - 海关信息必须准确完整
            - HS编码必须符合国际标准
            - 重量以克为单位
            - 法规变化时可能需要定期更新
        """
        request = SyncCustomsInfoRequest(
            item_id=item_id,
            barcode=barcode,
            customs_info=customs_info,
        )
        request.method = "order.syncItemCustomsInfo"
        return self._execute(request, response_model=str)

    def get_customs_info(
        self,
        barcode: str,
    ) -> BaseResponse[GetCustomsInfoResponse]:
        """跨境商品备案信息查询 (API: order.getCustomsInfo).

        获取商品的海关备案信息，包括HS编码、
        税率和跨境申报所需的法规详情。

        Args:
            barcode (str): 商品条形码 (必填)。

        Returns:
            BaseResponse[GetCustomsInfoResponse]: 响应包含:
                - providerSyncCustomsInfoV3List (List[ProviderSyncCustomsInfoV3]): 备案信息列表:
                    - barcode (str): 商品条形码
                    - customsName (str): 口岸编码，取值为三方保税支持口岸接口返回的口岸编码集合中的某个值
                    - hsCode (str): HS编码，即海关税则号
                    - generalTaxRate (float): 税率 (例如 0.1 = 10%)
                    - quantity1 (float): 法一数量
                    - quantity2 (float): 法二数量

        Important Notes:
            - 仅返回已备案商品（并非所有商品都有海关备案）
            - 条形码必须与备案商品完全匹配
            - 不同口岸可能有不同的备案状态
            - 备案信息受海关法规变化影响
            - 某些敏感商品可能有访问限制
        """
        request = GetCustomInfoRequest(barcode=barcode)
        request.method = "order.getCustomsInfo"
        return self._execute(request, response_model=GetCustomsInfoResponse)

    def get_order_receiver_info(
        self,
        receiver_queries: List[dict],
        is_return: bool,
    ) -> BaseResponse[GetOrderReceiverInfoResponse]:
        """订单收件人信息 (API: order.getOrderReceiverInfo).

        获取敏感的收件人信息，包括姓名、电话和详细地址。
        应在发货前调用此API以确保收件人信息准确性，
        避免用户修改导致的不一致。

        Args:
            receiver_queries (List[dict]): 收件人详情查询列表，请务必在发货前调用一次避免用户修改导致不一致 (必填):
                每个项目包含:
                - orderId (str): 订单号，待发货才可以拉到收件人信息
                - openAddressId (str): 详情接口返回，标识此单收件人信息
            is_return (bool): 是否是换货单 (必填)。

        Returns:
            BaseResponse[GetOrderReceiverInfoResponse]: 响应包含:
                - receiverInfos (List[OrderReceiverInfo]): 收件人信息列表:
                    - orderId (str): 订单号 用来对应
                    - matched (bool): 当前openAddressId是否与传入的相符，不相符时不返回相关信息，且需要重新 拉取订单详情
                    - receiverProvinceName (str): 收件人省份
                    - receiverCityName (str): 收件人城市
                    - receiverDistrictName (str): 收件人区县
                    - receiverTownName (str): 收件人镇/街道
                    - receiverName (str): 收件人姓名
                    - receiverPhone (str): 收件人电话
                    - receiverAddress (str): 收件人详细地址
                    - location (str): 收件人POI坐标 (经度,纬度)

        Examples:
            >>> # Get receiver info for single order
            >>> queries = [{
            ...     "orderId": "P132***4125",
            ...     "openAddressId": "1948201"
            ... }]
            >>> response = client.order.get_order_receiver_info(
            ...     access_token,
            ...     receiver_queries=queries,
            ...     is_return=False
            ... )
            >>>
            >>> for receiver_info in response.data.receiverInfos:
            ...     if receiver_info.matched:
            ...         print(f"Receiver: {receiver_info.receiverName}")
            ...         print(f"Phone: {receiver_info.receiverPhone}")
            ...         print(f"Address: {receiver_info.receiverAddress}")
            ...     else:
            ...         print("Address changed, need to re-fetch order detail")

            >>> # Get receiver info for multiple orders
            >>> queries = [
            ...     {"orderId": "P132***4125", "openAddressId": "1948201"},
            ...     {"orderId": "P132***4126", "openAddressId": "1948202"}
            ... ]
            >>> response = client.order.get_order_receiver_info(
            ...     access_token,
            ...     receiver_queries=queries,
            ...     is_return=False
            ... )

        Important:
            - 只有待发货状态的订单才能获取收件人信息
            - 在发货前始终调用此API以避免地址不一致
            - 如果matched=false，说明收件人已修改地址；重新获取订单详情
            - openAddressId来自订单详情响应
            - 此API提供敏感个人信息；遵循适当的数据保护措施

        Security Note:
            收件人信息包含个人数据。确保适当的数据保护，
            仅在订单履约必需时访问。
        """
        request = GetOrderReceiverInfoRequest(
            receiver_queries=receiver_queries,
            is_return=is_return,
        )
        request.method = "order.getOrderReceiverInfo"
        return self._execute(request, response_model=GetOrderReceiverInfoResponse)

    def modify_order_express_info(
        self,
        order_id: str,
        express_no: str,
        express_company_code: str,
        express_company_name: Optional[str] = None,
        delivery_order_index: Optional[int] = None,
        old_express_no: Optional[str] = None,
    ) -> BaseResponse[str]:
        """修改运单 (API: order.modifyOrderExpressInfo).

        修改已发货订单的快递跟踪号和公司信息。
        支持普通订单和拆包修改。

        Args:
            order_id (str): 订单号 (必填)。
            express_no (str): 快递单号 (必填)。
            express_company_code (str): 快递公司编码 (必填)。
            express_company_name (Optional[str]): 快递公司名称。
            delivery_order_index (Optional[int]): 修改拆包订单快递单号必传。
            old_express_no (Optional[str]): 旧快递单号,非必填,优先级高于deliveryOrderIndex,只传oldExpressNo,会修改订单号下面所有快递单号为oldExpressNo的包裹(可能更新多个);oldExpressNo和deliveryOrderIndex同时传,只会修改一个包裹。

        Returns:
            BaseResponse[str]: 响应包含:
                - error_code (int): 错误码（0为成功）
                - success (bool): 是否成功
                - data (object): 操作结果信息

        Parameter Priority:
            - oldExpressNo优先级高于deliveryOrderIndex
            - 同时提供时，只修改一个包裹
            - 只提供oldExpressNo时，更新所有匹配跟踪号的包裹

        Important Notes:
            - 订单必须处于已发货状态才能修改跟踪信息
            - 对于拆包，使用deliveryOrderIndex或oldExpressNo指定特定包裹
            - 快递公司编码应匹配标准物流服务商编码
            - 跟踪号修改会影响客户跟踪体验
        """
        request = ModifyOrderExpressRequest(
            order_id=order_id,
            express_no=express_no,
            express_company_code=express_company_code,
            express_company_name=express_company_name,
            delivery_order_index=delivery_order_index,
            old_express_no=old_express_no,
        )
        request.method = "order.modifyOrderExpressInfo"
        return self._execute(request, response_model=str)

    def order_deliver(
        self,
        order_id: str,
        express_no: str,
        express_company_code: str,
        express_company_name: Optional[str] = None,
        delivering_time: Optional[int] = None,
        unpack: Optional[bool] = None,
        sku_id_list: Optional[List[str]] = None,
        return_address_id: Optional[str] = None,
        sku_identify_code_info: Optional[dict] = None,
    ) -> BaseResponse[str]:
        """订单发货 (API: order.orderDeliver).

        标记订单为已发货并提供物流信息。支持传统快递
        和无物流发货模式。

        Args:
            order_id (str): 订单号 (必填)。
            express_no (str): 快递单号（如使用的是无物流发货，expressNo为发货内容） (必填)。
            express_company_code (str): 快递公司编码（如使用无物流发货，expressCompanyCode为selfdelivery） (必填)。
            express_company_name (Optional[str]): 快递公司名称(如传入，则以传入为准，如未传入，则根据expressCompanyCode进行匹配)。
            delivering_time (Optional[int]): 发货时间 不传默认当前时间（ms）。
            unpack (Optional[bool]): 是否拆包发货 true 拆包发货 false正常发货。
            sku_id_list (Optional[List[str]]): 拆包发货时 必填。
            return_address_id (Optional[str]): 退货地址id 非必填。
            sku_identify_code_info (Optional[dict]): 国补订单序列号等信息 非必填，仅部分类目国补订单需要:
                - sNCode (str): 序列号
                - barCode (str): 商品条码
                - iMEI1Code (str): IMEI1
                - iMEI2Code (str): IMEI2

        Returns:
            BaseResponse[str]: 响应包含:
                - error_code (int): 错误码（0为成功）
                - success (bool): 是否成功
                - data (object): 操作结果信息

        Important Notes:
            - 对于无物流发货，使用expressCompanyCode="selfdelivery"
            - 对于拆包发货（unpack=True），skuIdList为必填
            - 某些补贴订单需要序列号信息（skuIdentifyCodeInfo）
            - 调用此API前确保订单处于"待发货"状态
            - 快递公司编码应匹配标准物流服务商编码
        """
        request = OrderDeliverRequest(
            order_id=order_id,
            express_no=express_no,
            express_company_code=express_company_code,
            express_company_name=express_company_name,
            delivering_time=delivering_time,
            unpack=unpack,
            sku_id_list=sku_id_list,
            return_address_id=return_address_id,
            sku_identify_code_info=sku_identify_code_info,
        )
        request.method = "order.orderDeliver"
        return self._execute(request, response_model=str)

    def modify_seller_mark_info(
        self,
        order_id: str,
        seller_mark_note: str,
        operator: str,
        seller_mark_priority: int,
    ) -> BaseResponse[str]:
        """修改订单备注 (API: order.modifySellerMarkInfo).

        更新商家备注和优先级标记，用于订单管理和内部跟踪。
        这些标记帮助商家组织和优先处理订单。

        Args:
            order_id (str): 订单号 (必填)。
            seller_mark_note (str): 商家备注内容 (必填)。
            operator (str): 操作人名称 (必填)。
            seller_mark_priority (int): 商家标记优先级，ark订单列表展示旗子颜色 1灰旗 2红旗 3黄旗 4绿旗 5蓝旗 6紫旗 (必填)。

        Returns:
            BaseResponse[str]: 响应包含:
                - error_code (int): 错误码（0为成功）
                - success (bool): 是否成功
                - data (object): 操作结果信息

        Note:
            旗子颜色帮助商家在ARK系统中直观地组织订单:
            - 红旗通常表示紧急订单
            - 黄旗表示需要特别关注
            - 绿旗表示准备发货或已验证的订单
            - 蓝/紫旗用于自定义分类
            - 灰旗表示标准处理
        """
        request = ModifySellerMarkRequest(
            order_id=order_id,
            seller_mark_note=seller_mark_note,
            operator=operator,
            seller_mark_priority=seller_mark_priority,
        )
        request.method = "order.modifySellerMarkInfo"
        return self._execute(request, response_model=str)

    def get_order_tracking(
        self,
        order_id: str,
    ) -> BaseResponse[GetOrderTrackingResponse]:
        """订单物流轨迹 (API: order.getOrderTracking).

        获取综合物流跟踪信息，包括小红书内部处理阶段
        和快递公司配送跟踪。

        Args:
            order_id (str): 订单号 (必填)。

        Returns:
            BaseResponse[GetOrderTrackingResponse]: 响应包含:
                - orderTrackInfos (List[OrderTrackInfo]): 物流轨迹列表:
                    - orderId (str): 订单号
                    - deliveryOrderId (str): 发货订单id
                    - currentStatusDesc (str): 订单当前状态描述（待付款、已支付、海关申报中、海关通过、待配货、配货中、仓库作业中、已发货、待揽件、已揽件、运输中、已签收、已完成、已关闭、取消发货）
                    - expressCompanyCode (str): 快递公司编码
                    - expressCompanyName (str): 快递公司名称
                    - expressNo (str): 快递单号
                    - records (List[TrackingRecord]): 快递轨迹（包括小红书对订单的处理流程节点以及发货后快递公司产生的路由轨迹）:
                        - eventAt (str): 路由时间发生时间
                        - eventDesc (str): 路由发生事件描述
                        - trackingPartnerSyncAt (str): 小红书系统同步到该路由的时间
                        - nodeId (int): 轨迹系统 5:轨迹来自交易系统 6:轨迹来自履约系统 8:轨迹来自仓库系统 35:轨迹来自快递公司
                        - subNodeId (int): 每个系统下的子节点，例如nodeid=35,subNodeid=10表示轨迹来自快递公司，轨迹类型为揽收
                        - trackingStatus (int): 轨迹状态 每一条轨迹都会被对应到一个唯一的状态编码，1010：订单已创建，1015：订单已支付，1019：信息待补充，2010/2011/2012：海关申报中，2015：海关申报完成，3010：商家处理中，3015：商家打包中，3020：商家已发货，3050：仓库处理中，3055：an仓库分拣中，3060：仓库打包中，3065：仓库已发出，6020：快递运输中
                        - trackingStatusDesc (str): 轨迹状态编码的描述
                        - location (ExpressLocation): 轨迹发生的地点:
                            - provinceName (str): 省
                            - cityName (str): 市

        Current Status Descriptions:
            - "待付款": Pending payment
            - "已支付": Paid
            - "海关申报中": Customs declaration
            - "海关通过": Customs cleared
            - "待配货": Pending allocation
            - "配货中": Allocating
            - "仓库作业中": Warehouse processing
            - "已发货": Shipped
            - "待揽件": Pending pickup
            - "已揽件": Picked up
            - "运输中": In transit
            - "已签收": Delivered
            - "已完成": Completed
            - "已关闭": Closed
            - "取消发货": Shipping cancelled

        Tracking Record Sources:
            - 内部阶段 (nodeId 5,6,8): 小红书系统处理
            - 快递阶段 (nodeId 35): 快递公司跟踪
            - 每个源提供不同类型的跟踪事件
        """
        request = GetOrderTrackRequest(order_id=order_id)
        request.method = "order.getOrderTracking"
        return self._execute(request, response_model=GetOrderTrackingResponse)

    def get_order_declare_info(
        self,
        order_id: str,
    ) -> BaseResponse[GetOrderDeclareInfoResponse]:
        """海关申报信息 (API: order.getOrderDeclareInfo).

        获取跨境订单的海关申报信息，包括申报人身份详情，
        用于跨境电商海关清关。

        Args:
            order_id (str): 订单号 (必填)。

        Returns:
            BaseResponse[GetOrderDeclareInfoResponse]: 响应包含:
                - orderDeclareInfos (List[OrderDeclareInfo]): 申报信息列表:
                    - orderId (str): 订单号
                    - idName (str): 申报人姓名
                    - idNumber (str): 申报人身份证号
                    - linkPhone (str): 申报人联系电话
                    - frontUrl (str): 身份证正面照片URL
                    - backUrl (str): 身份证背面照片URL
                    - type (str): 申报人类型（"收货人"/"订购人"）
                        - "收货人": 收货人（商家自发货场景）
                        - "订购人": 下单人

        Note:
            - 仅适用于需要海关申报的跨境订单
            - 包含敏感个人信息（身份证号、照片）
            - 照片URL可能为空（如客户未提供）
            - 跨境场景海关清关必需
            - 个人数据处理需遵循隐私法规
        """
        request = GetOrderDeclareRequest(order_id=order_id)
        request.method = "order.getOrderDeclareInfo"
        return self._execute(request, response_model=GetOrderDeclareInfoResponse)

    def get_supported_port_list(
        self,
    ) -> BaseResponse[GetSupportedPortListResponse]:
        """跨境清关支持口岸 (API: order.getSupportedPortList).

        获取小红书平台和当前商家支持的跨境电商
        海关申报清关口岸列表。

        Args:

        Returns:
            BaseResponse[GetSupportedPortListResponse]: 响应包含:
                - platSupportCustoms (List[BondedCustomsInfo]): 平台支持口岸:
                    - customs_name (str): 口岸名称
                    - customs_code (str): 口岸编码
                - sellerSupportCustoms (List[BondedCustomsInfo]): 商家支持口岸:
                    - customs_name (str): 口岸名称
                    - customs_code (str): 口岸编码

        Note:
            - 仅适用于跨境电商订单
            - 商家口岸访问权取决于业务资质
            - 口岸可用性可能因法规更新而变化
            - 选择离发货地最近的口岸提高效率
        """
        request = GetSupportedPortListRequest()
        request.method = "order.getSupportedPortList"
        return self._execute(request, response_model=GetSupportedPortListResponse)

    def create_transfer_batch(
        self,
        orders: List[dict],
        plan_info_id: str,
    ) -> BaseResponse[CreateTransferBatchResponse]:
        """小包批次创建 (API: order.createTransferBatch).

        创建转运批次以整合多个订单，实现高效的物流处理，
        通常用于国际运输或仓库整合场景。

        Args:
            orders (List[dict]): 转运订单信息列表 (必填):
                每个项目包含:
                - orderId (str): 订单号
                - weight (int): 订单重量（克）
            plan_info_id (str): 物流方案ID (必填)。

        Returns:
            BaseResponse[CreateTransferBatchResponse]: 响应包含:
                - batchNo (str): 生成的批次号用于跟踪
                - message (str): 发生问题时的错误信息
                - successTotal (int): 成功添加到批次的订单数
                - total (int): 尝试添加的订单总数

        Note:
            - 订单必须处于合适状态才能批量处理
            - 重量限制可能根据物流方案适用
            - 批次创建可能有时间窗口
            - 批次一旦创建无法修改
        """
        request = CreateTransferBatchRequest(
            orders=orders,
            plan_info_id=plan_info_id,
        )
        request.method = "order.createTransferBatch"
        return self._execute(request, response_model=CreateTransferBatchResponse)

    def get_kos_data(
        self,
        start_date: str,
        end_date: str,
        page_no: int,
        page_size: int,
    ) -> BaseResponse[GetKosDataResponse]:
        """获取KOS员工数据 (API: businessdata.getKosData).

        获取KOS（重点意见销售）员工的销售业绩数据，包括订单详情、
        客户信息和销售指标，用于业务分析和提成计算。

        Args:
            start_date (str): 开始日期，yyyy-MM-dd格式 (必填)。
            end_date (str): 结束日期，yyyy-MM-dd格式 (必填)。
            page_no (int): 页码 (必填)。
            page_size (int): 分页大小，最大1000条记录 (必填)。

        Returns:
            BaseResponse[GetKosDataResponse]: 响应包含:
                - code (int): 响应码
                - msg (str): 响应消息
                - success (bool): 操作成功状态
                - data (object): KOS数据:
                    - count (int): 记录总数
                    - data (List): KOS员工销售数据:
                        - packageId (str): 订单包裹ID
                        - skuId (str): 商品SKU ID
                        - skuName (str): 商品SKU名称
                        - itemId (str): 商品ID
                        - itemName (str): 商品名称
                        - payDate (str): 支付日期
                        - accountUserId (str): 小红书用户ID
                        - accountUserName (str): KOS员工名称
                        - accountType (str): 账户类型
                        - newCarrierNameGroup (str): 载体组
                        - entranceChannel (str): 销售渠道
                        - carrierId (str): 载体ID
                        - carrierName (str): 载体标题/名称
                        - carrierCreateTime (str): 载体创建/开始时间
                        - goodsTotal (int): 购买商品数量
                        - payGmv (float): 支付金额（GMV）
                        - redAccountUserId (str): 社区用户ID

        Note:
            - 日期范围影响数据可用性
            - 每页最多1000条记录
            - 包含敏感员工和客户数据
            - 支付日期使用平台时区
            - GMV包含所有费用和税收
        """
        request = GetKosDataRequest(
            start_date=start_date,
            end_date=end_date,
            page_no=page_no,
            page_size=page_size,
        )
        request.method = "businessdata.getKosData"
        return self._execute(request, response_model=GetKosDataResponse)

    def modify_customs_status(
        self,
        order_id: str,
        customs_status: str,
        customs_remark: Optional[str] = None,
        operator_id: Optional[str] = None,
    ) -> BaseResponse[str]:
        """修改海关清关状态 (API: order.modifycustomstatus).

        更新跨境订单的海关清关状态，以便进行适当的
        海关处理和合规跟踪。

        Args:
            order_id (str): 订单号 (必填)。
            customs_status (str): 新的海关状态 (必填)。
            customs_remark (Optional[str]): 海关处理备注。
            operator_id (Optional[str]): 执行修改的操作员ID。

        Returns:
            BaseResponse[str]: 响应包含:
                - error_code (int): 错误码，0表示成功
                - success (bool): 操作是否成功
                - data (object): 操作结果信息

        Note:
            - 仅适用于跨境订单
            - 状态变更必须遵循逻辑顺序
            - 某些状态变更可能触发自动化流程
            - 维护审计跟踪以保证合规
            - 可能影响订单交付时间表
        """
        request = ModifyCustomsStatusRequest(
            order_id=order_id,
            customs_status=customs_status,
            customs_remark=customs_remark,
            operator_id=operator_id,
        )
        request.method = "order.modifycustomstatus"
        return self._execute(request, response_model=str)

    def batch_approve_subscribe_orders(
        self,
        order_ids: List[str],
        approval_reason: Optional[str] = None,
        operator_id: Optional[str] = None,
        approval_notes: Optional[str] = None,
    ) -> BaseResponse[str]:
        """物流服务批量审批订阅订单 (API: logisticservice.batchApproveSubscribeOrders).

        批量审批多个订阅物流服务的订单，简化高订单量
        商家的审批流程。

        Args:
            order_ids (List[str]): 待审批的订单ID列表 (必填)。
            approval_reason (Optional[str]): 批量审批原因。
            operator_id (Optional[str]): 执行审批的操作员ID。
            approval_notes (Optional[str]): 附加审批备注。

        Returns:
            BaseResponse[str]: 响应包含:
                - error_code (int): 错误码，0表示成功
                - success (bool): 批量操作是否成功
                - data (object): 批量审批结果信息

        Note:
            - 只有授权操作员才能执行批量审批
            - 审批不能轻易撤销
            - 批次中所有订单必须符合审批条件
            - 失败的审批可能需要单独处理
            - 维护审计日志以保证责任制
        """
        request = BatchApproveSubscribeOrdersRequest(
            order_ids=order_ids,
            approval_reason=approval_reason,
            operator_id=operator_id,
            approval_notes=approval_notes,
        )
        request.method = "logisticservice.batchApproveSubscribeOrders"
        return self._execute(request, response_model=str)
