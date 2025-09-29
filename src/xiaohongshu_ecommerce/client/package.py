"""Package management client for Xiaohongshu e-commerce API."""

from typing import List, Optional

from ..models.base import BaseResponse
from ..models.package import (
    AddDeclarePortRequest,
    AuditCancelApplyRequest,
    CreateTransferBatchRequest,
    CreateTransferBatchResponse,
    GetCancelApplyListRequest,
    GetCancelApplyListResponse,
    GetItemCustomInfoRequest,
    GetItemCustomsInfoResponse,
    GetPackageDeclareRequest,
    GetPackageDeclareResponse,
    GetPackageDetailRequest,
    GetPackageDetailResponse,
    GetPackageListRequest,
    GetPackagesListResponse,
    GetPackageTrackRequest,
    GetPackageTrackResponse,
    GetReceiverInfoRequest,
    GetReceiveInfoResponse,
    GetSupportedPortListRequest,
    GetSupportedPortListResponse,
    ModifyPackageExpressRequest,
    ModifySellerMarkRequest,
    PackageDeliverRequest,
    ResendBondedPaymentRequest,
    SyncItemCustomsRequest,
    UpdateProxyPackageWeightRequest,
)
from .base import SyncSubClient


class PackageClient(SyncSubClient):
    """包裹和跨境物流管理API的同步客户端。

    包裹系统为小红书电商平台提供全面的物流管理服务，包括国内外运输、
    海关申报、包裹跟踪和跨境电商业务。此客户端提供从创建到配送的
    完整包裹生命周期管理。
    """

    def get_package_list(
        self,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        time_type: Optional[int] = None,
        package_type: Optional[int] = None,
        package_status: Optional[int] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> BaseResponse[GetPackagesListResponse]:
        """包裹列表 (API: package.getPackageList).

        获取分页的包裹列表，支持各种筛选条件，
        包括状态、日期范围、包裹类型和运输信息。
        包裹管理和跟踪操作的必要功能。

        Args:
            start_time (Optional[int]): 开始时间筛选（Unix时间戳，毫秒）。
            end_time (Optional[int]): 结束时间筛选（Unix时间戳，毫秒）。
            time_type (Optional[int]): 时间类型筛选。
            package_type (Optional[int]): 包裹类型筛选。
            package_status (Optional[int]): 包裹状态筛选:
                - 1: 已创建
                - 2: 运输中
                - 3: 已送达
                - 4: 已取消
                - 5: 异常
            page_no (Optional[int]): 页码（默认: 1）。
            page_size (Optional[int]): 页大小（默认: 20，最大: 100）。

        Returns:
            BaseResponse[GetPackagesListResponse]: 响应包含:
                - packages (List[PackageInfo]): 包裹信息列表
                - total (int): 包裹总数
                - current_page (int): 当前页码
                - total_pages (int): 总页数

        Note:
            对于大型数据集使用分页以提高性能。
            日期筛选使用Unix时间戳（毫秒）。
            包裹状态码可能因地区和服务类型而异。
        """
        request = GetPackageListRequest(
            start_time=start_time,
            end_time=end_time,
            time_type=time_type,
            package_type=package_type,
            package_status=package_status,
            page_no=page_no,
            page_size=page_size,
        )
        request.method = "package.getPackageList"
        return self._execute(request, response_model=GetPackagesListResponse)

    def get_package_detail(
        self,
        package_id: Optional[str] = None,
        package_no: Optional[str] = None,
    ) -> BaseResponse[GetPackageDetailResponse]:
        """包裹详情 (API: package.getPackageDetail).

        获取特定包裹的详细信息，包括运输详情、
        海关信息、跟踪历史和当前状态。

        Args:
            package_id (Optional[str]): 包裹ID。
            package_no (Optional[str]): 包裹编号。

        Returns:
            BaseResponse[GetPackageDetailResponse]: 响应包含:
                - package_info (PackageDetail): 完整包裹信息:
                    - package_id (str): 包裹标识符
                    - order_id (str): 关联订单ID
                    - package_status (int): 当前包裹状态
                    - express_company (str): 运输公司信息
                    - tracking_number (str): 包裹跟踪号
                    - sender_info (dict): 发件人信息
                    - receiver_info (dict): 收件人信息
                    - package_items (List): 包裹内物品
                    - customs_info (dict): 海关申报详情
                    - tracking_history (List): 包裹运动历史
                    - create_time (int): 包裹创建时间戳
                    - update_time (int): 最后更新时间戳

        Note:
            跟踪历史可能因运输公司能力而有限。
            海关信息适用于国际包裹。
            包裹详情在状态变化时实时更新。
        """
        request = GetPackageDetailRequest(
            package_id=package_id,
            package_no=package_no,
        )
        request.method = "package.getPackageDetail"
        return self._execute(request, response_model=GetPackageDetailResponse)

    def resend_bonded_payment_record(
        self,
        package_id: Optional[str] = None,
        payment_no: Optional[str] = None,
    ) -> BaseResponse[str]:
        """重发保税支付记录 (API: package.resendBondedPaymentRecord).

        向海关部门重新发送跨境电商包裹的保税支付记录。
        通常在初始支付通知失败或需要重新处理海关清关时使用。

        Args:
            package_id (Optional[str]): 包裹ID。
            payment_no (Optional[str]): 支付交易号。

        Returns:
            BaseResponse[str]: 响应包含:
                - 操作状态和确认信息
                - 重发失败时的错误信息

        Note:
            此操作专门针对跨境电商包裹。
            在尝试重发之前必须存在支付记录。
            海关编码必须对目标国家/地区有效。
        """
        request = ResendBondedPaymentRequest(
            package_id=package_id,
            payment_no=payment_no,
        )
        request.method = "package.resendBondedPaymentRecord"
        return self._execute(request, response_model=str)

    def sync_item_customs_info(
        self,
        package_id: Optional[str] = None,
        customs_items: Optional[List] = None,
    ) -> BaseResponse[str]:
        """同步商品海关信息 (API: package.syncItemCustomsInfo).

        更新和同步跨境包裹中商品的海关申报信息。
        确保准确的海关处理和遵守国际贸易法规。

        Args:
            package_id (Optional[str]): 包裹ID。
            customs_items (Optional[List]): 海关商品信息列表。

        Returns:
            BaseResponse[str]: 响应包含:
                - 同步状态和确认
                - 同步失败时的错误信息

        Note:
            HS编码必须准确以便正确的海关分类。
            海关名称对海关部门应清晰和描述性。
            价格信息影响关税和税收计算。
            原产国必须符合贸易协定要求。
        """
        request = SyncItemCustomsRequest(
            package_id=package_id,
            customs_items=customs_items or [],
        )
        request.method = "package.syncItemCustomsInfo"
        return self._execute(request, response_model=str)

    def get_item_customs_info(
        self,
        package_id: Optional[str] = None,
    ) -> BaseResponse[GetItemCustomsInfoResponse]:
        """商品海关申报信息 (API: package.getItemCustomsInfo).

        获取跨境运输中使用的商品海关申报信息。
        此信息对海关清关和国际贸易合规至关重要。

        Args:
            package_id (Optional[str]): 包裹ID。

        Returns:
            BaseResponse[GetItemCustomsInfoResponse]: 响应包含:
                - customs_info (ItemCustomsInfo): 完整海关信息:
                    - item_id (str): 商品标识符
                    - hs_code (str): 海关编码（商品编码）
                    - customs_name (str): 海关申报名称
                    - customs_name_en (str): 英文海关申报名称
                    - unit_price (float): 海关估价单价
                    - currency (str): 价格货币代码
                    - origin_country (str): 原产国
                    - brand (str): 商品品牌
                    - model (str): 商品型号
                    - specification (str): 商品规格
                    - net_weight (float): 净重（克）
                    - gross_weight (float): 毛重（克）
                    - customs_status (int): 海关处理状态
                    - create_time (int): 信息创建时间戳
                    - update_time (int): 最后更新时间戳
                - history (List, optional): 海关信息变更历史

        Note:
            所有跨境运输都需要海关信息。
            HS编码决定关税税率和进口限制。
            准确的申报可防止海关延误和罚款。
        """
        request = GetItemCustomInfoRequest(
            package_id=package_id,
        )
        request.method = "package.getItemCustomsInfo"
        return self._execute(request, response_model=GetItemCustomsInfoResponse)

    def get_package_receiver_info(
        self,
        package_id: Optional[str] = None,
    ) -> BaseResponse[GetReceiveInfoResponse]:
        """包裹收件人信息 (API: package.getPackageReceiverInfo).

        获取包裹配送的详细收件人信息，包括地址、
        联系方式和任何特殊配送指示。对于准确的
        包裹配送和客户沟通至关重要。

        Args:
            package_id (Optional[str]): 包裹ID。

        Returns:
            BaseResponse[GetReceiveInfoResponse]: 响应包含:
                - receiver_info (ReceiverInfo): 完整收件人信息:
                    - name (str): 收件人姓名
                    - phone (str): 联系电话
                    - address (str): 完整配送地址
                    - postal_code (str): 邮政编码
                    - province (str): 省/州
                    - city (str): 城市
                    - district (str): 区/县
                    - detailed_address (str): 详细地址
                    - delivery_notes (str): 特殊配送指示
                    - identity_number (str): 身份验证号
                    - is_encrypted (bool): 数据是否加密

        Note:
            敏感数据解密需要适当权限。
            收件人信息用于配送协调。
            个人数据访问适用隐私保护措施。
        """
        request = GetReceiverInfoRequest(
            package_id=package_id,
        )
        request.method = "package.getPackageReceiverInfo"
        return self._execute(request, response_model=GetReceiveInfoResponse)

    def modify_package_express_info(
        self,
        package_id: Optional[str] = None,
        express_company: Optional[str] = None,
        express_no: Optional[str] = None,
    ) -> BaseResponse[str]:
        """修改包裹快递信息 (API: package.modifyPackageExpressInfo).

        更新包裹的快递运输详情，包括承运商变更、
        跟踪号更新和运输方式修改。适用于纠正
        运输信息或更新承运商详情。

        Args:
            package_id (Optional[str]): 包裹ID。
            express_company (Optional[str]): 快递公司名称。
            express_no (Optional[str]): 快递跟踪号。

        Returns:
            BaseResponse[str]: 响应包含:
                - 操作状态和确认信息
                - 修改失败时的错误信息

        Note:
            修改可能影响配送估算和跟踪。
            某些变更可能需要额外验证或审批。
            跟踪号格式必须符合快递公司要求。
        """
        request = ModifyPackageExpressRequest(
            package_id=package_id,
            express_company=express_company,
            express_no=express_no,
        )
        request.method = "package.modifyPackageExpressInfo"
        return self._execute(request, response_model=str)

    def package_deliver(
        self,
        package_id: Optional[str] = None,
        express_company: Optional[str] = None,
        express_no: Optional[str] = None,
        delivery_time: Optional[int] = None,
    ) -> BaseResponse[str]:
        """包裹发货 (API: package.packageDeliver).

        将包裹状态更新为已发货并记录发货确认详情。
        此操作完成运输生命周期并触发发货后流程，
        如客户通知和订单完成。

        Args:
            package_id (Optional[str]): 包裹ID。
            express_company (Optional[str]): 快递公司名称。
            express_no (Optional[str]): 快递跟踪号。
            delivery_time (Optional[int]): 实际发货时间戳。

        Returns:
            BaseResponse[str]: 响应包含:
                - 发货确认状态
                - 更新的包裹信息
                - 发货记录失败时的错误信息

        Note:
            此操作通常由配送人员或系统执行。
            发货确认触发客户通知和订单更新。
            发货证明（照片、签名）增强客户信心。
        """
        request = PackageDeliverRequest(
            package_id=package_id,
            express_company=express_company,
            express_no=express_no,
            delivery_time=delivery_time,
        )
        request.method = "package.packageDeliver"
        return self._execute(request, response_model=str)

    def modify_seller_mark_info(
        self,
        package_id: Optional[str] = None,
        seller_mark: Optional[str] = None,
    ) -> BaseResponse[str]:
        """修改商家标记信息 (API: package.modifySellerMarkInfo).

        更新包裹上的商家特定标记或标签信息。
        这可以包括特殊处理指示、商家识别或
        物流管理的自定义标记要求。

        Args:
            package_id (Optional[str]): 包裹ID。
            seller_mark (Optional[str]): 商家标记信息。

        Returns:
            BaseResponse[str]: 响应包含:
                - 修改确认状态
                - 更新的标记信息
                - 修改失败时的错误详情

        Note:
            商家标记帮助物流供应商适当处理包裹。
            某些标记可能影响运输成本或配送方式。
            自定义标记应遵守承运商和法规要求。
        """
        request = ModifySellerMarkRequest(
            package_id=package_id,
            seller_mark=seller_mark,
        )
        request.method = "package.modifySellerMarkInfo"
        return self._execute(request, response_model=str)

    def get_package_tracking(
        self,
        package_id: Optional[str] = None,
        express_no: Optional[str] = None,
    ) -> BaseResponse[GetPackageTrackResponse]:
        """包裹跟踪信息 (API: package.getPackageTracking).

        获取包裹的实时跟踪信息，包括当前位置、
        运动历史、配送状态和预计配送时间。
        对于客户服务和物流监控至关重要。

        Args:
            package_id (Optional[str]): 包裹ID。
            express_no (Optional[str]): 快递跟踪号。

        Returns:
            BaseResponse[GetPackageTrackResponse]: 响应包含:
                - tracking_info (PackageTrackingInfo): 当前跟踪信息:
                    - package_id (str): 包裹标识符
                    - tracking_number (str): 快递跟踪号
                    - current_status (int): 当前包裹状态
                    - current_location (str): 当前包裹位置
                    - last_update_time (int): 最后跟踪更新时间戳
                    - estimated_delivery (int): 预计配送时间戳
                    - delivery_attempts (int): 配送尝试次数
                - tracking_history (List[TrackingEvent]): 运动历史:
                    - event_time (int): 事件时间戳
                    - event_type (str): 跟踪事件类型
                    - location (str): 事件位置
                    - description (str): 事件描述
                    - operator (str): 处理操作员/设施
                - delivery_estimates (dict): 配送时间估算

        Note:
            跟踪准确性取决于承运商报告能力。
            实时更新可能与实际包裹运动有轻微延迟。
            国际包裹在某些地区可能跟踪有限。
        """
        request = GetPackageTrackRequest(
            package_id=package_id,
            express_no=express_no,
        )
        request.method = "package.getPackageTracking"
        return self._execute(request, response_model=GetPackageTrackResponse)

    def get_package_declare_info(
        self,
        package_id: Optional[str] = None,
    ) -> BaseResponse[GetPackageDeclareResponse]:
        """包裹海关申报信息 (API: package.getPackageDeclareInfo).

        获取跨境包裹的海关申报详情，包括申报价值、
        商品分类和国际运输所需的法规合规信息。

        Args:
            package_id (Optional[str]): 包裹ID。

        Returns:
            BaseResponse[GetPackageDeclareResponse]: 响应包含:
                - declaration_info (PackageDeclaration): 申报详情:
                    - package_id (str): 包裹标识符
                    - declaration_id (str): 海关申报ID
                    - declaration_status (int): 申报处理状态
                    - total_value (float): 申报总价值
                    - currency (str): 申报货币
                    - customs_office (str): 处理海关
                    - declaration_date (int): 申报提交时间戳
                    - clearance_status (int): 海关清关状态
                - item_declarations (List[ItemDeclaration]): 商品级申报:
                    - item_id (str): 商品标识符
                    - hs_code (str): 海关编码
                    - declared_name (str): 海关申报名称
                    - quantity (int): 申报数量
                    - unit_value (float): 单位申报价值
                    - total_value (float): 商品总价值
                - documents (List[DeclarationDocument]): 支持文件

        Note:
            申报信息对海关清关至关重要。
            准确的申报可防止延误和额外费用。
            某些国家需要特定的文件格式。
        """
        request = GetPackageDeclareRequest(
            package_id=package_id,
        )
        request.method = "package.getPackageDeclareInfo"
        return self._execute(request, response_model=GetPackageDeclareResponse)

    def get_supported_port_list(
        self,
        customs_code: Optional[str] = None,
    ) -> BaseResponse[GetSupportedPortListResponse]:
        """支持的海关口岸列表 (API: package.getSupportedPortList).

        获取跨境包裹处理支持的海关口岸和入境点列表。
        此信息对规划国际运输和海关申报至关重要。

        Args:
            customs_code (Optional[str]): 海关编码筛选口岸。

        Returns:
            BaseResponse[GetSupportedPortListResponse]: 响应包含:
                - ports (List[PortInfo]): 支持的口岸列表:
                    - port_code (str): 口岸标识码
                    - port_name (str): 口岸名称
                    - port_name_en (str): 英文口岸名称
                    - country_code (str): 国家代码
                    - city (str): 口岸城市
                    - port_type (int): 口岸类型
                    - is_active (bool): 口岸是否当前活跃
                    - processing_time (str): 典型处理时间
                    - contact_info (dict): 口岸联系信息
                - total_count (int): 支持的口岸总数

        Note:
            口岸可用性可能因法规更新而变化。
            根据包裹类型和目的地选择适当的口岸。
            某些口岸可能有特定要求或限制。
        """
        request = GetSupportedPortListRequest(
            customs_code=customs_code,
        )
        request.method = "package.getSupportedPortList"
        return self._execute(request, response_model=GetSupportedPortListResponse)

    def get_cancel_apply_list(
        self,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        status: Optional[int] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> BaseResponse[GetCancelApplyListResponse]:
        """取消申请列表 (API: package.getCancelApplyList).

        获取需要审查或处理的包裹取消请求列表。
        用于管理取消工作流并确保适当处理运输中断。

        Args:
            start_time (Optional[int]): 开始时间筛选（Unix时间戳）。
            end_time (Optional[int]): 结束时间筛选（Unix时间戳）。
            status (Optional[int]): 取消状态筛选:
                - 1: 待审查
                - 2: 已批准
                - 3: 已拒绝
                - 4: 处理中
            page_no (Optional[int]): 页码（默认: 1）。
            page_size (Optional[int]): 页大小（默认: 20）。

        Returns:
            BaseResponse[GetCancelApplyListResponse]: 响应包含:
                - applications (List[CancelApplication]): 取消申请:
                    - application_id (str): 申请标识符
                    - package_id (str): 包裹ID
                    - apply_reason (str): 取消原因
                    - apply_time (int): 申请时间戳
                    - status (int): 当前申请状态
                    - reviewer (str): 分配的审查员
                    - review_time (int): 审查时间戳
                    - review_notes (str): 审查评论
                    - refund_amount (float): 退款金额（如适用）
                - total_count (int): 申请总数
                - page_info (dict): 分页信息

        Note:
            取消申请需要及时审查以保持服务质量。
            某些取消可能根据运输阶段产生费用。
            已批准的取消触发退款和通知流程。
        """
        request = GetCancelApplyListRequest(
            start_time=start_time,
            end_time=end_time,
            status=status,
            page_no=page_no,
            page_size=page_size,
        )
        request.method = "package.getCancelApplyList"
        return self._execute(request, response_model=GetCancelApplyListResponse)

    def audit_cancel_apply(
        self,
        apply_id: Optional[str] = None,
        audit_result: Optional[int] = None,
        audit_reason: Optional[str] = None,
    ) -> BaseResponse[str]:
        """审核取消申请 (API: package.auditCancelApply).

        通过批准或拒绝请求来审查和处理包裹取消申请。此操作控制取消工作流程
        并确保运输中断的适当授权。

        Args:
            apply_id (Optional[str]): 取消申请ID。
            audit_result (Optional[int]): 审核决定:
                - 1: 批准取消
                - 2: 拒绝取消
            audit_reason (Optional[str]): 审核决定原因。

        Returns:
            BaseResponse[str]: 响应包含:
                - 审核完成状态
                - 更新的申请信息
                - 审核失败时的错误详情

        Examples:
            >>> # 批准取消申请
            >>> response = client.package.audit_cancel_apply(
            ...     access_token,
            ...     apply_id="cancel_app_123",
            ...     audit_result=1,  # 批准
            ...     audit_reason="取消理由有效"
            ... )

            >>> # 拒绝取消申请
            >>> response = client.package.audit_cancel_apply(
            ...     access_token,
            ...     apply_id="cancel_app_456",
            ...     audit_result=2,  # 拒绝
            ...     audit_reason="包裹已发货"
            ... )

        Note:
            审核决定会触发自动流程，如退款或通知。
            拒绝的取消应包含对客户的明确解释。
            根据运输阶段和公司政策可能会产生处理费用。
        """
        request = AuditCancelApplyRequest(
            apply_id=apply_id,
            audit_result=audit_result,
            audit_reason=audit_reason,
        )
        request.method = "package.auditCancelApply"
        return self._execute(request, response_model=str)

    def add_declare_port(
        self,
        package_id: Optional[str] = None,
        port_code: Optional[str] = None,
    ) -> BaseResponse[str]:
        """新增申报口岸 (API: package.addDeclarePort).

        将新的海关口岸添加到跨境包裹处理的支持申报点列表中。
        这使商家能够通过其他海关设施申报包裹。

        Args:
            package_id (Optional[str]): 要添加申报口岸的包裹ID。
            port_code (Optional[str]): 要添加的口岸代码。

        Returns:
            BaseResponse[str]: 响应包含:
                - 口岸添加确认状态
                - 分配的口岸配置详情
                - 添加失败时的错误信息

        Examples:
            >>> # 为包裹添加新申报口岸
            >>> response = client.package.add_declare_port(
            ...     access_token,
            ...     package_id="pkg_123456789",
            ...     port_code="PVG_EXPRESS"
            ... )

        Note:
            新口岸在生效前需要审批和配置。
            口岸代码必须唯一并遵循标准命名约定。
            联系信息应准确以便运营协调。
        """
        request = AddDeclarePortRequest(
            package_id=package_id,
            port_code=port_code,
        )
        request.method = "package.addDeclarePort"
        return self._execute(request, response_model=str)

    def update_proxy_package_weight(
        self,
        package_id: Optional[str] = None,
        weight: Optional[float] = None,
    ) -> BaseResponse[str]:
        """更新代理包裹重量信息 (API: package.updateProxyPackageWeight).

        更新通过代理运输服务处理的包裹重量信息。这对于准确的运费计算
        和跨境操作中的海关申报合规至关重要。

        Args:
            package_id (Optional[str]): 要更新重量的包裹ID。
            weight (Optional[float]): 包裹重量（克）。

        Returns:
            BaseResponse[str]: 响应包含:
                - 重量更新确认状态
                - 更新的包裹重量信息
                - 更新失败时的错误详情

        Examples:
            >>> # 更新包裹重量
            >>> response = client.package.update_proxy_package_weight(
            ...     access_token,
            ...     package_id="pkg_123456789",
            ...     weight=1250.5
            ... )

        Note:
            准确的重量信息对运费计算至关重要。
            如果体积重量高于实际重量，可能使用体积重量定价。
            重量更新可能会触发运费重新计算。
        """
        request = UpdateProxyPackageWeightRequest(
            package_id=package_id,
            weight=weight,
        )
        request.method = "package.updateProxyPackageWeight"
        return self._execute(request, response_model=str)

    def create_transfer_batch(
        self,
        package_ids: Optional[List[str]] = None,
        batch_type: Optional[int] = None,
    ) -> BaseResponse[CreateTransferBatchResponse]:
        """创建包裹转运批次 (API: package.createTransferBatch).

        创建用于在设施、仓库或物流中心之间转移多个包裹的批次。
        此操作将包裹分组以实现高效的批量处理和跟踪。

        Args:
            package_ids (Optional[List[str]]): 要包含在批次中的包裹ID列表。
            batch_type (Optional[int]): 转运批次类型:
                - 1: 仓库到仓库
                - 2: 仓库到配送中心
                - 3: 配送中心到配送站点
                - 4: 跨境转运

        Returns:
            BaseResponse[CreateTransferBatchResponse]: 响应包含:
                - batch_info (TransferBatch): 已创建的批次信息:
                    - batch_id (str): 生成的批次标识符
                    - batch_name (str): 批次名称
                    - status (int): 批次状态
                    - package_count (int): 批次中包裹数量
                    - total_weight (float): 所有包裹的总重量
                    - source_facility (str): 源设施
                    - destination_facility (str): 目标设施
                    - create_time (int): 批次创建时间戳
                    - scheduled_time (int): 计划转运时间
                - package_status (List[dict]): 批次中各个包裹的状态

        Examples:
            >>> # 创建仓库转移批次
            >>> response = client.package.create_transfer_batch(
            ...     access_token,
            ...     package_ids=[
            ...         "pkg_123456789",
            ...         "pkg_987654321",
            ...         "pkg_456789123"
            ...     ],
            ...     batch_type=1  # 仓库到仓库
            ... )

            >>> # 创建跨境转运批次
            >>> response = client.package.create_transfer_batch(
            ...     access_token,
            ...     package_ids=["pkg_001", "pkg_002", "pkg_003"],
            ...     batch_type=4  # 跨境转运
            ... )

        Note:
            批次转运提高物流效率和跟踪准确性。
            批次中的所有包裹必须符合指定转运类型的条件。
            跨境批次可能需要额外的文档和审批。
        """
        request = CreateTransferBatchRequest(
            package_ids=package_ids or [],
            batch_type=batch_type,
        )
        request.method = "package.createTransferBatch"
        return self._execute(request, response_model=CreateTransferBatchResponse)
