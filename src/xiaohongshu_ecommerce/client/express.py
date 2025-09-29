"""Express management client for Xiaohongshu e-commerce API."""

from typing import Optional, List

from ..models.base import BaseResponse
from ..models.express import (
    CancelEbillOrderRequest,
    CancelEbillOrderResponse,
    CreateEbillOrdersRequest,
    CreateEbillOrdersResponse,
    ElectronicBillTradeOrderInfo,
    ElectronicBillUserInfo,
    QueryEbillOrderRequest,
    QueryEbillOrderResponse,
    QueryEbillSubscribesRequest,
    QueryEbillSubscribesResponse,
    QueryEbillTemplatesRequest,
    QueryEbillTemplatesResponse,
    UpdateEbillOrderRequest,
    UpdateEbillOrderResponse,
)
from .base import SyncSubClient


class ExpressClient(SyncSubClient):
    """Synchronous client for express and logistics management APIs.

    This client provides access to Xiaohongshu's electronic bill (e-bill) and express
    logistics management functionality including subscription management, template queries,
    order creation, updates, and cancellation.

    The express APIs support electronic waybill generation and management for various
    express delivery companies integrated with Xiaohongshu's platform.

    Supported Operations:
        - Query electronic bill subscription relationships
        - Query available electronic bill templates
        - Create electronic bill orders (batch number allocation)
        - Query electronic bill order details
        - Update electronic bill order information
        - Cancel electronic bill orders

    Note:
        All express APIs require proper authentication and valid express company
        subscription relationships before use.
    """

    def query_ebill_subscribes(
        self,
        cp_code: Optional[str] = None,
        need_usage: Optional[bool] = None,
        brand_code: Optional[str] = None,
        bill_version: Optional[int] = None,
    ) -> BaseResponse[QueryEbillSubscribesResponse]:
        """查询电子面单订购关系和使用情况 (API: express.queryEbillSubscribes).

        查询商家与快递公司的订购关系，包括网点信息、发货地址和使用统计。
        此API是在创建电子面单订单前了解可用快递选项的重要接口。

        Args:
            cp_code (Optional[str]): 快递公司编码
            need_usage (Optional[bool]): 是否需要返回使用情况，注意会影响接口性能，有些商家订购超过了100个以上的网点会该字段如果设置为true会导致接口响应时间超过3s
            brand_code (Optional[str]): 品牌编码
            bill_version (Optional[int]): 电子面单版本号，1-默认值旧版电子面单 2-新版电子面单

        Returns:
            BaseResponse[QueryEbillSubscribesResponse]: Response containing:
                - subscribeList (List[SubscribeInfo]): 订阅列表 with:
                  - cpCode (str): 快递公司编码
                  - cpName (str): 快递公司名称
                  - cpType (int): 类型，1-直营 2-加盟
                  - branchCode (str): 网点编码
                  - branchName (str): 网点名称
                  - brandCode (str): 品牌code
                  - customerCode (str): 月结卡号，仅邮政、EMS、京东、顺丰、德邦等直营快递支持
                  - senderAddressList (List): 发货地址
                  - usage (UsageInfo, optional): needUsage=true才会返回 with:
                    - quantity (int): 可用余额，直营没有这个数据默认全部返回0
                    - allocatedQuantity (int): 累计已经分配的数量
                    - cancelQuantity (int): 取消的面单数量
                    - recycledQuantity (int): 回收的面单数量，直营没有这个数据默认全部返回0
                - accountId (int): 长整型，电子面单账号ID

        Note:
            - 设置needUsage=true可能导致大商家响应时间超过3秒
            - 使用统计数据仅适用于加盟快递公司
            - 直营公司的使用量字段返回0

        Example:
            ```python
            response = client.express.query_ebill_subscribes(
                access_token=access_token,
                cp_code="zto",
                need_usage=True,
                bill_version=2
            )
            for subscribe in response.data.subscribe_list:
                print(f"Company: {subscribe.cp_name}, Branch: {subscribe.branch_name}")
            ```
        """
        request = QueryEbillSubscribesRequest(
            cp_code=cp_code,
            need_usage=need_usage,
            brand_code=brand_code,
            bill_version=bill_version,
        )
        request.method = "express.queryEbillSubscribes"
        return self._execute(request, response_model=QueryEbillSubscribesResponse)

    def query_ebill_templates(
        self,
        cp_code: Optional[str] = None,
        brand_code: Optional[str] = None,
        type: Optional[str] = None,
        template_customer_type: Optional[int] = None,
        bill_version: Optional[int] = None,
    ) -> BaseResponse[QueryEbillTemplatesResponse]:
        """查询电子面单模板列表 (API: express.queryEbillTemplates).

        查询特定快递公司的可用电子面单模板。
        模板定义了创建电子面单订单时将生成的电子运单的格式和布局。

        Args:
            cp_code (Optional[str]): 快递公司编码
            brand_code (Optional[str]): 品牌编码，当前只有顺丰快运和顺丰速运查询需要传值
            type (Optional[str]): 类型，默认不填返回标准模板列表， ark-返回小红书商家配置的模板列表
            template_customer_type (Optional[int]): 自定义类型 0-标准 1-订单号 2-商品名称/规格/数量 3-商品名称/规格/数量 + 买家留言 + 商家备注 4-订单号 + 商品名称/规格/数量 + 买家留言 + 商家  10-商家云打印系统自定义 20-自定义打印项组合
            bill_version (Optional[int]): 电子面单版本号，1-默认值旧版电子面单 2-新版电子面单

        Returns:
            BaseResponse[QueryEbillTemplatesResponse]: Response containing:
                - templateList (List[TemplateInfo]): 模板列表 with:
                  - id (int): 模板id，取号的时候传入此值
                  - cpCode (str): 快递公司编码
                  - brandCode (str): 品牌，仅部分快递支持
                  - templateType (str): 模板尺寸，76*130-一联，100*150-二联，100*180-三联
                  - templateCustomerType (int): 自定义类型 0-标准 1-订单号 2-商品名称/规格/数量 3-商品名称/规格/数量 + 买家留言 + 商家备注 4-订单号 + 商品名称/规格/数量 + 买家留言 + 商家备注  10-商家云打印系统自定义
                  - templateName (str): 模板名称
                  - templateDesc (str): 模板描述
                  - templatePreviewUrl (str): 预览URL
                  - standardTemplateUrl (str): 标准模板URL
                  - customerTemplateUrl (str): 自定义模板URL，templateCustomerType=0时该字段为空，支持的大小是76*30和100*40两种尺寸;isv可根据标记语言规则自己实现自定义区域，新版是小红书自研的标记语言，语法格式是json；旧版使用的菜鸟的标记语言，语法格式是xml
                  - customerPrintItems (object): 自定义打印项参数列表，注意格式是List<String>，示例：["order","buyerMemo"]

        Note:
            - 某些快递公司需要brandCode参数（如顺丰快递）
            - 模板尺寸：76*130（一联），100*150（二联），100*180（三联）
            - 自定义模板支持76*30和100*40尺寸
            - 新版使用JSON标记语言，旧版使用XML

        Example:
            ```python
            response = client.express.query_ebill_templates(
                access_token=access_token,
                cp_code="zto",
                type="ark",
                bill_version=2
            )
            for template in response.data.template_list:
                print(f"Template: {template.template_name} ({template.template_type})")
            ```
        """
        request = QueryEbillTemplatesRequest(
            cp_code=cp_code,
            brand_code=brand_code,
            type=type,
            template_customer_type=template_customer_type,
            bill_version=bill_version,
        )
        request.method = "express.queryEbillTemplates"
        return self._execute(request, response_model=QueryEbillTemplatesResponse)

    def query_ebill_order(
        self,
        cp_code: str,
        waybill_code: str,
        bill_version: Optional[int] = None,
    ) -> BaseResponse[QueryEbillOrderResponse]:
        """查询电子面单打印数据 (API: express.queryEbillOrder).

        使用面单号查询特定电子面单订单的打印数据。
        此API返回打印电子运单和自定义打印区域所需的格式化数据。

        Args:
            cp_code (str): 快递公司编码
            waybill_code (str): 面单号
            bill_version (Optional[int]): 电子面单版本号，1-默认值旧版电子面单 2-新版电子面单

        Returns:
            BaseResponse[QueryEbillOrderResponse]: Response containing:
                - waybillCode (str): 面单号
                - printData (str): 面单打印数据
                - parentWaybillCode (str): 子母单会返回母单
                - extraInfo (str): 扩展信息
                - cpCode (str): 快递公司编码
                - customerPrintData (str): 自定义打印数据

        Note:
            - printData包含加密的打印信息以确保安全
            - 自定义打印数据包括订单号、商品信息等
            - 对于子母单，使用母单号进行操作
            - 打印数据格式因旧版和新版面单而异

        Example:
            ```python
            response = client.express.query_ebill_order(
                access_token=access_token,
                cp_code="zto",
                waybill_code="78689455849606",
                bill_version=2
            )
            print(f"Waybill: {response.data.waybill_code}")
            print(f"Print data available: {bool(response.data.print_data)}")
            ```
        """
        request = QueryEbillOrderRequest(
            cp_code=cp_code,
            waybill_code=waybill_code,
            bill_version=bill_version,
        )
        request.method = "express.queryEbillOrder"
        return self._execute(request, response_model=QueryEbillOrderResponse)

    def create_ebill_orders(
        self,
        cp_code: str,
        sender: ElectronicBillUserInfo,
        trade_order_info_list: List[ElectronicBillTradeOrderInfo],
        seller_name: str,
        branch_code: Optional[str] = None,
        customer_code: Optional[str] = None,
        brand_code: Optional[str] = None,
        product_code: Optional[str] = None,
        bill_version: Optional[int] = None,
        pay_method: Optional[int] = None,
        call_door_pick_up: Optional[bool] = None,
        door_pick_up_time: Optional[str] = None,
        door_pick_up_end_time: Optional[str] = None,
        extra_info: Optional[str] = None,
    ) -> BaseResponse[CreateEbillOrdersResponse]:
        """批量取号 (API: express.createEbillOrders).

        为快递运输创建电子运单订单。此API处理批量运单号分配，
        并为与小红书平台集成的各种快递公司生成电子面单。

        Args:
            cp_code (str): 快递公司编码
            sender (ElectronicBillUserInfo): 寄件人地址必须和订购关系的地址保持一致 including:
                - name (str): 姓名，明文
                - address (ElectronicBillAddress): 寄件人地址 with:
                  - province (str): 省份
                  - city (str): 城市
                  - detail (str): 详细地址
                  - district (str, optional): 区县，订购关系返回了district则必须要传
                  - town (str, optional): 乡镇街道，订购关系返回了town则必须要传
                - mobile (str, optional): 手机号码，明文
                - phone (str, optional): 电话号码
            trade_order_info_list (List[ElectronicBillTradeOrderInfo]): 请求面单列表（上限0个） with:
                - object_id (str): 请求ID，最大长度40，保证一次批量请求不重复，返回结果基于该值取到对应的快递单号
                - order_info (ElectronicBillOrderInfo): Order details including:
                  - order_channels_type (str): 订单渠道，见[对接说明](https://open.xiaohongshu.com/document/developer/file/52)附录渠道列表
                  - trade_order_list (List[str]): 订单列表，如果是小红书订单并且没有传xhsOrderId参数则需要填写正确的订单号，否则可能导致用户信息解密出现问题
                  - buyer_memo (List[str], optional): 买家留言列表
                  - seller_memo (List[str], optional): 商家备注列表
                  - xhs_order_id (str, optional): 小红书订单号，如果传了值，密文解密的时候会基于这个参数来做解密
                  - xhs_order_list (List[str], optional): 合单订单号列表，合单情况下必填
                - package_info (ElectronicBillPackageInfo): Package details including:
                  - id (str): 包裹ID
                  - items (List[ElectronicBillItem]): 商品信息，上限0 with:
                    - count (int): 数量
                    - name (str): 名称
                    - specification (str, optional): 规格
                  - weight (float, optional): 重量,单位 g
                  - volume (float, optional): 体积, 单位 ml
                  - length (float, optional): 包裹长，单位厘米
                  - width (float, optional): 包裹宽，单位厘米
                  - height (float, optional): 包裹高，单位厘米
                  - total_packages_count (int, optional): 子母件包裹数，该字段大于0则表示子母件
                  - packaging_description (str, optional): 大件快运中的包装方式描述
                  - goods_description (str, optional): 大件快运中的货品描述，顺丰要求必传长度不能超过20，并且不能和商品名称相同
                  - good_value (float, optional): 物流价值，单位元
                - recipient (ElectronicBillUserInfo): 收件人信息，支持明文、密文、openAddressId + xhsOrderId三种 including:
                  - name (str, optional): 姓名，明文或者密文
                  - mobile (str, optional): 手机号码，明文或者密文，正确密文格式有4个#号：#xxxx#x##
                  - phone (str, optional): 电话号码
                  - address (ElectronicBillAddress, optional): Address with:
                    - province (str): 省份
                    - city (str): 城市
                    - district (str): 区县
                    - town (str): 乡镇街道
                    - detail (str): 详细地址
                  - open_address_id (str, optional): 非必填但是对于WMS该参数必传，长度固定是32位，该参数来自于order.getOrderDetail接口。如果收件人信息缺失，该参数用来补充查询数据，但是要求小红书渠道并且订单号要匹配一致
                - template_id (int): 电子面单模板ID，通过调用[查询电子面单模板列表express.queryEbillTemplates]接口查询得到，注意新版和旧版的ID不能混用
                - logistics_services (str, optional): 物流增值服务，见[对接说明](https://open.xiaohongshu.com/document/developer/file/52)附录物流增值服务，保价单位是元保留两位小数
                - deliver_extend_info (str, optional): 用于传递数据给下游的拓展信息字段，json字符串，特殊业务场景下使用
            seller_name (str): 店铺名称，对参数内容没有限制，不会做校验，但是要求必传
            branch_code (Optional[str]): 网点编码，加盟型快递公司要求必填，直营快递（顺丰 、邮政、京东、德邦等）传空字符
            customer_code (Optional[str]): 月结卡号，直营快递公司（顺丰、邮政、京东、德邦等）要求必填，加盟快递传空字符串
            brand_code (Optional[str]): 品牌编码，顺丰要求必填，其他快递不传或者空字符串
            product_code (Optional[str]): 产品编码，京东要求必填，顺丰不传值则默认是1-顺丰特快，仅部分快递公司支持传入，见[对接说明](https://open.xiaohongshu.com/document/developer/file/52)附录物流产品类型
            bill_version (Optional[int]): 电子面单版本号，1-默认值旧版电子面单 2-新版电子面单
            pay_method (Optional[int]): 付款方式；注意仅新版电子面单支持；顺丰，1:寄方付 2:收方付 3:第三方付；邮政（包括youzhengguonei、ems、youzhengbiaokuai）：1寄付，2-到付
            call_door_pick_up (Optional[bool]): 是否预约上门，仅顺丰支持传入
            door_pick_up_time (Optional[str]): 预约上门取件时间，'yyyy-MM-dd HH:mm:ss'，仅顺丰支持传入
            door_pick_up_end_time (Optional[str]): 预约上门取件截止时间，'yyyy-MM-dd HH:mm:ss'，仅顺丰支持传入
            extra_info (Optional[str]): 拓展信息，加盟总对总模式用到（见https://open.xiaohongshu.com/help/list/27/140的总对总模式）

        Returns:
            BaseResponse[CreateEbillOrdersResponse]: Response containing:
                - tradeOrderInfoList (List[TradeOrderResult]): 面单列表 with:
                  - objectId (str): 请求ID，一次批量请求中的唯一ID
                  - success (bool): 是否取号成功
                  - waybillCode (str): 面单号
                  - shortWaybillCode (str): Short waybill code
                  - parentWaybillCode (str): 子母单会返回母单
                  - bagAddr (str): Bag address information
                  - packageCenterCode (str): Package center code
                  - packageCenterName (str): Package center name
                  - sortCode (str): Sort code
                  - errorCode (int): 取号失败code
                  - errorMsg (str): 取号失败原因
                  - printData (str): 面单打印数据，传输给打印组件的报文contents数组的第一个元素
                  - customerPrintData (str): 自定义打印数据，可为空，如果有则是传输给打印组件报文contents数组的第二个元素
                - subErrorCode (str): 子错误码，开发者可以忽略这个值，取号异常可以联系我们定位我们

        Note:
            - 每次批量请求最多10个订单
            - 寄件人地址必须与订购关系地址保持一致
            - 不同快递公司有不同的必填参数
            - 加盟公司需要branchCode，直营公司需要customerCode
            - 加密收件人信息使用格式：#xxxx#x##作为手机号码
            - 对于小红书订单，确保tradeOrderList与实际订单号匹配

        Example:
            ```python
            from ..models.express import (
                ElectronicBillUserInfo,
                ElectronicBillAddress,
                ElectronicBillTradeOrderInfo,
                ElectronicBillOrderInfo,
                ElectronicBillPackageInfo,
                ElectronicBillItem,
            )

            sender = ElectronicBillUserInfo(
                name="发件人",
                address=ElectronicBillAddress(province="上海市", city="上海市", detail="详细地址")
            )
            trade_orders = [
                ElectronicBillTradeOrderInfo(
                    object_id="order_001",
                    order_info=ElectronicBillOrderInfo(
                        order_channels_type="XIAO_HONG_SHU",
                        trade_order_list=["P123456789"]
                    ),
                    package_info=ElectronicBillPackageInfo(
                        id="pkg_001",
                        items=[ElectronicBillItem(count=1, name="商品名称")]
                    ),
                    recipient=ElectronicBillUserInfo(name="收件人", mobile="13800138000"),
                    template_id=123456
                )
            ]
            response = client.express.create_ebill_orders(
                access_token=access_token,
                cp_code="zto",
                sender=sender,
                trade_order_info_list=trade_orders,
                seller_name="店铺名称",
                branch_code="branch_001"
            )
            for result in response.data.trade_order_info_list:
                if result.success:
                    print(f"Order {result.object_id}: {result.waybill_code}")
                else:
                    print(f"Order {result.object_id} failed: {result.error_msg}")
            ```
        """
        request = CreateEbillOrdersRequest(
            cp_code=cp_code,
            sender=sender,
            trade_order_info_list=trade_order_info_list,
            seller_name=seller_name,
            branch_code=branch_code,
            customer_code=customer_code,
            brand_code=brand_code,
            product_code=product_code,
            bill_version=bill_version,
            pay_method=pay_method,
            call_door_pick_up=call_door_pick_up,
            door_pick_up_time=door_pick_up_time,
            door_pick_up_end_time=door_pick_up_end_time,
            extra_info=extra_info,
        )
        request.method = "express.createEbillOrders"
        return self._execute(request, response_model=CreateEbillOrdersResponse)

    def update_ebill_order(
        self,
        cp_code: str,
        waybill_code: str,
        sender: Optional[ElectronicBillUserInfo] = None,
        trade_order_info_list: Optional[List[ElectronicBillTradeOrderInfo]] = None,
        extra_info: Optional[str] = None,
        customer_code: Optional[str] = None,
        brand_code: Optional[str] = None,
        product_code: Optional[str] = None,
        call_door_pick_up: Optional[bool] = None,
        door_pick_up_time: Optional[str] = None,
        door_pick_up_end_time: Optional[str] = None,
        seller_name: Optional[str] = None,
        branch_code: Optional[str] = None,
        pay_method: Optional[int] = None,
        bill_version: Optional[int] = None,
    ) -> BaseResponse[UpdateEbillOrderResponse]:
        """更新面单 (API: express.updateEbillOrder).

        更新现有电子面单订单的特定信息，如包裹详情、收件人信息和物流服务。
        注意并非所有快递公司都支持订单修改。

        Args:
            cp_code (str): 快递公司编码
            waybill_code (str): 快递单号，注意顺丰和京东不支持修改
            sender (Optional[ElectronicBillUserInfo]): 发件人信息，注意顺丰不支持更新收件人、发件人信息 including:
                - name (str, optional): 姓名，明文
                - mobile (str, optional): 手机号码，明文
                - phone (str, optional): 电话号码
            trade_order_info_list (Optional[List[ElectronicBillTradeOrderInfo]]): Updated order information including:
                - package_info (ElectronicBillPackageInfo, optional): Package details with:
                  - items (List[ElectronicBillItem], optional): 商品信息 with:
                    - count (int): 数量
                    - name (str): 名称
                    - specification (str, optional): 规格
                  - volume (float, optional): 体积, 单位 ml
                  - weight (float, optional): 重量,单位 g
                  - length (float, optional): 包裹长，单位厘米
                  - width (float, optional): 包裹宽，单位厘米
                  - height (float, optional): 包裹高，单位厘米
                - recipient (ElectronicBillUserInfo, optional): 收件人信息，注意顺丰不支持更新收件人、发件人信息 including:
                  - name (str, optional): 姓名，明文或者密文
                  - mobile (str, optional): 手机号码，明文或者密文
                  - phone (str, optional): 电话号码
                  - address (ElectronicBillAddress, optional): Address with:
                    - province (str): 省份
                    - city (str): 城市
                    - district (str): 区县
                    - town (str): 乡镇街道
                    - detail (str): 详细地址
                  - open_address_id (str, optional): 用来查询收件人详情，需要和orderId匹配使用
                - logistics_services (str, optional): 增值服务,见[对接说明](https://open.xiaohongshu.com/document/developer/file/52)附录物流增值服务
                - template_id (int, optional): 电子面单模板ID
            extra_info (Optional[str]): 扩展信息
            customer_code (Optional[str]): Customer code
            brand_code (Optional[str]): Brand code
            product_code (Optional[str]): Product code
            call_door_pick_up (Optional[bool]): Schedule door pickup
            door_pick_up_time (Optional[str]): Pickup time
            door_pick_up_end_time (Optional[str]): Pickup end time
            seller_name (Optional[str]): Seller name
            branch_code (Optional[str]): Branch code
            pay_method (Optional[int]): Payment method
            bill_version (Optional[int]): 电子面单版本号，1-默认值旧版电子面单 2-新版电子面单

        Returns:
            BaseResponse[UpdateEbillOrderResponse]: Response containing:
                - waybill (object): Updated waybill information with:
                  - objectId (str): 请求ID
                  - waybillCode (str): 面单号
                  - printData (str): 面单打印数据
                  - parentWaybillCode (str): 子母单会返回母单
                  - extraInfo (str): 扩展信息
                  - cpCode (str): 快递公司编码
                  - customerPrintData (str): 自定义打印数据
                - subErrorCode (str): 子错误码

        Note:
            - 顺丰快递和京东快递不支持运单更新
            - 某些快递公司对可更新字段有限制
            - 加密收件人信息应保持与创建时相同的格式
            - 包裹重量和尺寸更新可能影响运费
            - 并非所有公司都支持增值服务更改

        Example:
            ```python
            from ..models.express import (
                ElectronicBillTradeOrderInfo,
                ElectronicBillPackageInfo,
                ElectronicBillItem,
                ElectronicBillUserInfo,
                ElectronicBillAddress,
            )

            trade_orders = [
                ElectronicBillTradeOrderInfo(
                    package_info=ElectronicBillPackageInfo(
                        items=[ElectronicBillItem(count=2, name="更新商品名称", specification="新规格")],
                        weight=500
                    ),
                    recipient=ElectronicBillUserInfo(
                        name="新收件人",
                        mobile="13900139000",
                        address=ElectronicBillAddress(
                            province="北京市",
                            city="北京市",
                            district="朝阳区",
                            detail="新的详细地址"
                        )
                    )
                )
            ]
            response = client.express.update_ebill_order(
                access_token=access_token,
                cp_code="zto",
                waybill_code="78689455849606",
                trade_order_info_list=trade_orders
            )
            if response.data.waybill:
                print("Waybill updated successfully")
            ```
        """
        request = UpdateEbillOrderRequest(
            cp_code=cp_code,
            waybill_code=waybill_code,
            sender=sender,
            trade_order_info_list=trade_order_info_list or [],
            extra_info=extra_info,
            customer_code=customer_code,
            brand_code=brand_code,
            product_code=product_code,
            call_door_pick_up=call_door_pick_up,
            door_pick_up_time=door_pick_up_time,
            door_pick_up_end_time=door_pick_up_end_time,
            seller_name=seller_name,
            branch_code=branch_code,
            pay_method=pay_method,
            bill_version=bill_version,
        )
        request.method = "express.updateEbillOrder"
        return self._execute(request, response_model=UpdateEbillOrderResponse)

    def cancel_ebill_order(
        self,
        cp_code: str,
        waybill_code: str,
        bill_version: Optional[int] = None,
        cancel_reason: Optional[str] = None,
    ) -> BaseResponse[CancelEbillOrderResponse]:
        """取消面单 (API: express.cancelEbillOrder).

        取消现有的电子面单订单，并将运单号回收到可用池中。
        此操作通常用于在取件前需要取消运输或订单被取消时。

        Args:
            cp_code (str): 快递公司编码
            waybill_code (str): 快递单号，注意子母件要用母单号才能取消
            bill_version (Optional[int]): 电子面单版本号，1-默认值旧版电子面单 2-新版电子面单
            cancel_reason (Optional[str]): Reason for cancellation

        Returns:
            BaseResponse[CancelEbillOrderResponse]: Response containing:
                - subErrorCode (str, optional): 子错误码 if cancellation failed
                - Additional response metadata

        Note:
            - 如果包裹已经被推上，可能无法取消
            - 对于子母件，始终使用母运单号
            - 某些快递公司对取消有时间限制
            - 已取消的运单号会被回收到可用池中
            - 失败的取消将包含特定错误代码以便调试

        Example:
            ```python
            response = client.express.cancel_ebill_order(
                access_token=access_token,
                cp_code="zto",
                waybill_code="78689455849606",
                bill_version=2
            )
            if response.success:
                print(f"Waybill {waybill_code} cancelled successfully")
            else:
                print(f"Cancellation failed: {response.error_msg}")
                if response.data and response.data.sub_error_code:
                    print(f"Sub-error: {response.data.sub_error_code}")
            ```
        """
        request = CancelEbillOrderRequest(
            cp_code=cp_code,
            waybill_code=waybill_code,
            bill_version=bill_version,
            cancel_reason=cancel_reason,
        )
        request.method = "express.cancelEbillOrder"
        return self._execute(request, response_model=CancelEbillOrderResponse)
