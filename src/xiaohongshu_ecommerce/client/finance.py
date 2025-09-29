"""Finance management client for Xiaohongshu e-commerce API."""

from typing import Optional, List

from ..models.base import BaseResponse
from ..models.finance import (
    DownloadStatementRequest,
    DownloadStatementResponse,
    PageQueryExpenseRequest,
    PageQueryExpenseResponse,
    PageQueryTransactionRequest,
    PageQueryTransactionResponse,
    QueryCpsSettleRequest,
    QueryCpsSettleResponse,
    QuerySellerAccountRecordsRequest,
    QuerySellerAccountRecordsResponse,
)
from .base import SyncSubClient


class FinanceClient(SyncSubClient):
    """Synchronous client for finance APIs."""

    def query_cps_settle(
        self,
        order_id: str,
    ) -> BaseResponse[QueryCpsSettleResponse]:
        """带货达人侧详情查询 (API: bill.queryCpsSettle)。

        查询特定订单的CPS佣金结算详情，包含佣金计算、结算状态等信息。

        Args:
            order_id (str): 订单号 (required).

        Returns:
            BaseResponse[QueryCpsSettleResponse]: Response containing:
                - cpsUserSettleDetails (List[CpsUserSettleDetail]): 订单结算明细列表 with:
                    - packageId (str): 订单号
                    - returnIds (List[str]): 退款单号列表
                    - goodsId (str): 商品id
                    - goodsName (str): 商品名称
                    - goodsTotal (int): 原始下单的商品数量
                    - sellerId (str): 商家id
                    - kolUserId (str): 推广达人id
                    - kolUserName (str): 达人昵称
                    - dealTotalAmount (int): 商品实付金额，单位分
                    - returnTotalAmount (int): 商品实退金额，单位分
                    - taxTotalAmount (int): 商品税金，单位分
                    - carryingTotalAmount (int): 带货金额=实付金额-实退金额-2B税金，单位分
                    - sellerRate (int): 商家在推广计划中设置的cps推广佣金率，商家支付的佣金比率，单位万分比
                    - kolUserShareRatio (int): 达人佣金分成比例，单位万分比，固定为8000，也就是80%
                    - kolUserRate (int): 达人CPS佣金率=商家CPS佣金率*达人分成比例，单位万分比
                    - kolUserCommissionAmount (int): 达人CPS佣金=带货金额*达人CPS佣金率，单位分
                    - settleStatus (str): 待结算（WAIT_SETTLE）、已结算（SETTLED）（待结算订单只有在下单48小时后可查，因为下单48小时内可能离线归因未完成，导致CPS计算不准确）
                    - orderTime (int): 下单时间，单位ms
                    - finishTime (int): 完成时间，单位ms
                    - canSettleTime (int): 可结算时间，单位ms
                    - settleTime (int): 已结算时间，单位ms

        Note:
            - 待结算订单只有在下单48小时后可查，因为下单48小时内可能离线归因未完成，导致CPS计算不准确
            - 所有金额单位均为分
            - 佣金率单位为万分比

        Example:
            ```python
            response = finance_client.query_cps_settle(
                access_token=access_token,
                order_id="ORDER123456789"
            )

            if response.success:
                for detail in response.data.cpsUserSettleDetails:
                    print(f"Order: {detail.packageId}")
                    print(f"Influencer: {detail.kolUserName}")
                    print(f"Commission: {detail.kolUserCommissionAmount / 100:.2f} yuan")
                    print(f"Status: {detail.settleStatus}")
            ```
        """
        request = QueryCpsSettleRequest(package_id=order_id)
        request.method = "bill.queryCpsSettle"
        return self._execute(request, response_model=QueryCpsSettleResponse)

    def download_statement(
        self,
        month: str,
    ) -> BaseResponse[DownloadStatementResponse]:
        """查询月度结算单下载地址 (API: bill.downloadStatement)。

        获取指定月份结算单的下载地址，包含该月份的详细财务数据。

        Args:
            month (str): 结算月份，yyyy-MM格式 (required).

        Returns:
            BaseResponse[DownloadStatementResponse]: Response containing:
                - downloadUrl (str): 下载地址，2小时有效期

        Note:
            - 下载地址有效期为2小时
            - 月度结算单通常在月份结束后提供
            - 下载的文件包含详细的财务明细数据

        Example:
            ```python
            response = finance_client.download_statement(
                access_token=access_token,
                month="2024-03"  # March 2024 statement
            )

            if response.success:
                download_url = response.data.downloadUrl
                print(f"Statement download URL: {download_url}")
                # Download the file within 2 hours of URL generation
                import requests
                statement_response = requests.get(download_url)
                with open("statement_2024_03.xlsx", "wb") as f:
                    f.write(statement_response.content)
            ```
        """
        request = DownloadStatementRequest(month=month)
        request.method = "bill.downloadStatement"
        return self._execute(request, response_model=DownloadStatementResponse)

    def query_seller_account_records(
        self,
        start_time: int,
        end_time: int,
        page_num: int,
        page_size: int,
        business_no: Optional[str] = None,
        debit_type: Optional[str] = None,
        trade_types: Optional[List[str]] = None,
        fund_type: Optional[int] = None,
    ) -> BaseResponse[QuerySellerAccountRecordsResponse]:
        """分页查询账户动账流水 (API: finance.querySellerAccountRecords)。

        分页查询账户的动账记录，包含账户收支情况和余额变化的详细信息。

        Args:
            start_time (int): 开始时间（unix时间戳，例如按日查询则传入指定日期00:00:00的时间戳） (required).
            end_time (int): 结束时间（unix时间戳，例如按日查询则传入指定日期23:59:59的时间戳） (required).
            page_num (int): 当前分页 (required).
            page_size (int): 分页大小 (required).
            business_no (str, optional): 业务单号.
            debit_type (str, optional): 资金流向：IN（收入）、OUT（支出）.
            trade_types (List[str], optional): 交易类型：RECHARGE(充值)STATEMENT_IN(结算入账)STATEMENT_REFUND(退款)PAY_SUCCESS(提现)BOUNCE(提现退回)SELLER_FINE(扣款)REFUND(扣款退回)LOGISTIC_OUT(物流费用结算)MANUAL_ADJUST_STATEMENT(人工调账结算)TRANSFER_IN(转入)TRANSFER_OUT(转出)CUSTOMER_SERVICE_FEE(客服费用)MESSAGE_FEE(短信推送费)INVOICE_SEND(发票寄送费)COMMISION_RETURN(佣金返利)OTHER_IN(其他收入)OTHER_OUT(其他支出).
            fund_type (int, optional): 账户类型：0(店铺余额)1(微信)2(支付宝).

        Returns:
            BaseResponse[QuerySellerAccountRecordsResponse]: Response containing:
                - pageNum (int): 当前分页
                - pageSize (int): 分页大小
                - total (int): 总数量
                - totalPage (int): 总页数
                - records (List[AccountRecord]): 数据集 with:
                    - accountId (int): 账户唯一id
                    - sellerId (str): 店铺id
                    - tradeNo (str): 动账流水号 (required)
                    - incomeAmount (str): 收入（元）
                    - outcomeAmount (str): 支出（元）
                    - balanceAmount (str): 账户余额（元）
                    - businessNo (str): 业务单号
                    - remark (str): 备注
                    - type (str): 交易类型
                    - typeDesc (str): 交易类型中文描述
                    - createdTime (int): 创建时间
                    - businessType (str): 动账业务子类型
                    - balanceBefore (str): 交易前金额（元）
                    - fundType (str): 账户类型：NOT_ER_QING(店铺余额)ER_QING_WECHAT(微信)ER_QING_ALIPAY(支付宝)
                    - disableBusinessNoLink (bool): 是否屏蔽业务跳转

        Note:
            - 所有金额单位均为元
            - 适用于账户对账和财务报表
            - 建议使用合适的时间范围避免大数据集

        Example:
            ```python
            import time

            # Query last 24 hours of account activity
            end_time = int(time.time() * 1000)  # Current time in ms
            start_time = end_time - (24 * 60 * 60 * 1000)  # 24 hours ago

            response = finance_client.query_seller_account_records(
                access_token=access_token,
                start_time=start_time,
                end_time=end_time,
                page_num=1,
                page_size=50,
                debit_type="IN",  # Only income transactions
                fund_type=0  # Store balance account
            )

            if response.success:
                print(f"Total records: {response.data.total}")
                for record in response.data.records:
                    print(f"Transaction: {record.tradeNo}")
                    print(f"Type: {record.typeDesc}")
                    print(f"Income: {record.incomeAmount} yuan")
                    print(f"Balance: {record.balanceAmount} yuan")
            ```
        """
        request = QuerySellerAccountRecordsRequest(
            start_time=start_time,
            end_time=end_time,
            page_num=page_num,
            page_size=page_size,
            business_no=business_no,
            debit_type=debit_type,
            trade_types=trade_types,
            fund_type=fund_type,
        )
        request.method = "finance.querySellerAccountRecords"
        return self._execute(request, response_model=QuerySellerAccountRecordsResponse)

    def page_query_transaction(
        self,
        start_time: int,
        end_time: int,
        page_num: int,
        page_size: int,
        settle_biz_type: Optional[int] = None,
        erqing_type: Optional[int] = None,
        common_settle_status: Optional[int] = None,
        should_load_goods_info: Optional[bool] = None,
    ) -> BaseResponse[PageQueryTransactionResponse]:
        """分页查询订单货款结算明细 (API: finance.pageQueryTransaction)。

        分页查询订单货款的结算详情，包含支付金额、佣金、税费等各项财务组成的详细分解。

        Args:
            start_time (int): 开始时间（unix时间戳，包含；如果结算状态为「已结算」则时间指「结算时间」，如果结算状态为「未结算」则时间指「订单完成时间」） (required).
            end_time (int): 结束时间（unix时间戳，不包含，每次最多查询一天数据，即startTime和endTime之间的差值不能超过24*60*60*1000；如果结算状态为「已结算」则时间指「结算时间」，如果结算状态为「未结算」则时间指「订单完成时间」） (required).
            page_num (int): 页码 (required).
            page_size (int): 分页大小 (required).
            settle_biz_type (int, optional): 交易类型：0(结算入账) 1(退款).
            erqing_type (int, optional): 结算账户：0(店铺余额) 2(微信) 1(支付宝).
            common_settle_status (int, optional): 结算状态：0(未结算) 1(已结算).
            should_load_goods_info (bool, optional): 是否查询商品信息.

        Returns:
            BaseResponse[PageQueryTransactionResponse]: Response containing:
                - total (int): 总数
                - totalPage (int): 总页数
                - pageNum (int): 页码
                - pageSize (int): 分页大小
                - transactions (List[TransactionDetail]): 数据集 with:
                    - transactionId (int): 结算唯一id
                    - packageId (str): 订单号
                    - statementType (int): 结算类型：2(履约单单笔结算) 1(预约单打包结算) 0(订单结算)
                    - transactionBizType (int): 账本业务类型：3(售后退款) 2(客服退款) 1(退货退款) 0(销售)
                    - settleBizType (int): 交易类型：0(结算入账) 1(退款)
                    - deliveryId (str): 履约单号
                    - transactionBizNo (str): 账本业务单号
                    - returnId (str): 售后单号
                    - orderTime (float): 下单时间
                    - canSettleTime (float): 可结算时间
                    - settledTime (float): 结算时间
                    - predictableSettleTime (str): 预计结算时间
                    - erqingType (int): 结算账户：0(店铺余额) 2(微信) 1(支付宝)
                    - transactionSettleStatus (int): 账本结算状态：2(可结算) 1(初始态) 0(不需要结算) 4(已结算) 5(结算异常) 6(正逆冲抵无需结算) 3(结算中)
                    - commonSettleStatus (int): 结算状态：0(未结算) 1(已结算)
                    - amount (str): 动账金额
                    - goodsAmount (str): 结算金额
                    - payAmount (str): 商品实付/实退金额
                    - appPromotion (str): 平台优惠金额
                    - freightAmount (str): 运费实付/实退金额
                    - noFreightReason (str): 运费不收取/退还的原因
                    - taxAmount (str): 税金
                    - noTaxReason (str): 税金不收取/退还的原因
                    - freightTaxAmount (str): 运费税
                    - noFreightTaxReason (str): 运费税不收取/退还的原因
                    - commissionAmount (str): 总佣金
                    - payChannelAmount (str): 总支付渠道费
                    - noPayChannelReason (str): 总支付渠道费不收取/退还的原因
                    - cpsAmount (str): CPS佣金
                    - installmentAmount (str): 花呗分期手续费
                    - noInstallmentReason (str): 花呗分期手续费不收取/退还的原因
                    - extraAmount (str): 附加费
                    - noExtraReason (str): 附加费不收取/退还的原因
                    - calculateRemark (str): 计费备注
                    - goodsDetails (List[GoodsDetail], optional): 商品信息 if shouldLoadGoodsInfo=true
                    - freightAppPromotion (str): 平台运费补贴

        Note:
            - 每次最多查询一天数据
            - 所有金额单位均为元
            - 结算时间根据订单类型和支付方式有所不同
            - 设置shouldLoadGoodsInfo=true可获取详细商品信息，但可能影响性能

        Example:
            ```python
            import time

            # Query settlements from last 24 hours
            end_time = int(time.time() * 1000)
            start_time = end_time - (24 * 60 * 60 * 1000)

            response = finance_client.page_query_transaction(
                access_token=access_token,
                start_time=start_time,
                end_time=end_time,
                page_num=1,
                page_size=20,
                common_settle_status=1,  # Only settled transactions
                should_load_goods_info=True
            )

            if response.success:
                print(f"Total transactions: {response.data.total}")
                for transaction in response.data.transactions:
                    print(f"Order: {transaction.packageId}")
                    print(f"Settlement Amount: {transaction.goodsAmount} yuan")
                    print(f"Commission: {transaction.commissionAmount} yuan")
                    print(f"Status: {'Settled' if transaction.commonSettleStatus == 1 else 'Pending'}")
            ```
        """
        request = PageQueryTransactionRequest(
            settle_biz_type=settle_biz_type,
            start_time=start_time,
            end_time=end_time,
            erqing_type=erqing_type,
            common_settle_status=common_settle_status,
            page_num=page_num,
            page_size=page_size,
            should_load_goods_info=should_load_goods_info,
        )
        request.method = "finance.pageQueryTransaction"
        return self._execute(request, response_model=PageQueryTransactionResponse)

    def page_query_expense(
        self,
        start_time: int,
        end_time: int,
        page_num: int,
        page_size: int,
        base_biz_type: Optional[int] = None,
        settle_status: Optional[int] = None,
    ) -> BaseResponse[PageQueryExpenseResponse]:
        """分页查询其他服务款结算明细 (API: finance.pageQueryExpense)。

        分页查询各种服务费用和附加费用的结算详情，包含平台服务、物流费用和其他费用。

        Args:
            start_time (int): 开始时间（unix时间戳，包含） (required).
            end_time (int): 结束时间（unix时间戳，不包含，每次最多查询一天数据，即startTime和endTime之间的差值不能超过24*60*60*1000） (required).
            page_num (int): 页码 (required).
            page_size (int): 分页大小 (required).
            base_biz_type (int, optional): 交易类型：0(薯券) 1(在线寄件快递费) 2(极速退款赔付) 3(发货延误赔付) 4(运费宝) 5(分期免息平台补贴) 6(仲裁结算) 7(小额打款)8(运费报销赔付).
            settle_status (int, optional): 结算状态：0(未结算) 1(已结算).

        Returns:
            BaseResponse[PageQueryExpenseResponse]: Response containing:
                - total (int): 总数
                - totalPage (int): 总页数
                - pageNum (int): 页码
                - pageSize (int): 分页大小
                - expenses (List[ExpenseDetail]): 数据集 with:
                    - expenseId (float): 费用唯一id
                    - baseBizType (str): 交易类型：0(薯券) 1(在线寄件快递费) 2(极速退款赔付) 3(发货延误赔付) 4(运费宝) 5(分期免息平台补贴) 6(仲裁结算) 7(小额打款)
                    - packageId (str): 订单号
                    - bizNo (str): 业务单号
                    - settledTime (float): 动账时间，unix时间戳（毫秒）
                    - erqingType (int): 结算账户：0(店铺余额) 1(支付宝) 2(微信)
                    - settleBizType (int): 交易类型：0(结算入账) 1(退款)
                    - transactionSettleStatus (int): 账本结算状态：2(可结算) 1(初始态) 0(不需要结算) 4(已结算) 5(结算异常) 6(正逆冲抵无需结算) 3(结算中)
                    - commonSettleStatus (int): 结算状态：0(未结算) 1(已结算)
                    - amount (str): 动账金额

        Note:
            - 每次最多查询一天数据
            - 所有金额单位均为元
            - 涵盖常规订单结算之外的各种服务费用和平台费用
            - 不同费用类型可能有不同的结算时间和条件

        Example:
            ```python
            import time

            # Query shipping-related expenses from last 24 hours
            end_time = int(time.time() * 1000)
            start_time = end_time - (24 * 60 * 60 * 1000)

            response = finance_client.page_query_expense(
                access_token=access_token,
                start_time=start_time,
                end_time=end_time,
                page_num=1,
                page_size=20,
                base_biz_type=1,  # Online shipping express fees
                settle_status=1  # Only settled expenses
            )

            if response.success:
                print(f"Total expenses: {response.data.total}")
                for expense in response.data.expenses:
                    print(f"Expense ID: {expense.expenseId}")
                    print(f"Type: {expense.baseBizType}")
                    print(f"Amount: {expense.amount} yuan")
                    print(f"Order: {expense.packageId}")
                    print(f"Settlement Status: {'Settled' if expense.commonSettleStatus == 1 else 'Pending'}")
            ```
        """
        request = PageQueryExpenseRequest(
            start_time=start_time,
            end_time=end_time,
            page_num=page_num,
            page_size=page_size,
            base_biz_type=base_biz_type,
            settle_status=settle_status,
        )
        request.method = "finance.pageQueryExpense"
        return self._execute(request, response_model=PageQueryExpenseResponse)
