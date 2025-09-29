"""Invoice management client for Xiaohongshu e-commerce API."""

from typing import Optional

from ..models.base import BaseResponse
from ..models.invoice import (
    ConfirmInvoiceRequest,
    GetInvoiceListRequest,
    GetInvoiceListResponse,
    ReverseInvoiceRequest,
)
from .base import SyncSubClient


class InvoiceClient(SyncSubClient):
    """发票管理API的同步客户端。

    发票系统处理小红书电商交易的电子发票生成、确认和管理。
    此客户端提供发票列表查询、确认发票上传和处理发票冲红的功能。
    """

    def get_invoice_list(
        self,
        invoice_status: Optional[int] = None,
        ref_no: Optional[str] = None,
        start_date_long: Optional[int] = None,
        end_date_long: Optional[int] = None,
        page_num: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_enum: Optional[int] = None,
        title_type: Optional[int] = None,
    ) -> BaseResponse[GetInvoiceListResponse]:
        """开票列表查询 (API: invoice.getInvoiceList).

        查询分页的发票列表，支持按状态、来源单号、日期范围和发票类型进行筛选。
        此API是发票管理和跟踪的必需功能。

        Args:
            invoice_status (Optional[int]): 开票状态，1:待开票；6：已开票；10：待作废
            ref_no (Optional[str]): 来源单号
            start_date_long (Optional[int]): 申请时间（开始时间）ms
            end_date_long (Optional[int]): 申请时间（结束时间）ms
            page_num (Optional[int]): 分页号
            page_size (Optional[int]): 分页大小,分页大小建议在100以内
            sort_enum (Optional[int]): 升序or降序，1:升序；2：降序
            title_type (Optional[int]): 发票抬头类型，1：个人；2：企业

        Returns:
            BaseResponse[GetInvoiceListResponse]: Response containing:
                - pageSize (int): 分页大小
                - pageIndex (int): 页码
                - total (int): Total number of invoices
                - totalPage (int): Total number of pages
                - invoiceRecords (List[InvoiceRecord]): List of invoice records

        Examples:
            >>> # Get all invoices with pagination
            >>> response = client.invoice.get_invoice_list(
            ...     access_token=access_token,
            ...     page_num=1,
            ...     page_size=50
            ... )

            >>> # Filter by invoice status
            >>> response = client.invoice.get_invoice_list(
            ...     access_token=access_token,
            ...     invoice_status=3,  # Completed invoices
            ...     page_num=1,
            ...     page_size=20
            ... )

            >>> # Filter by date range
            >>> import time
            >>> start_time = int((time.time() - 30 * 24 * 3600) * 1000)  # 30 days ago
            >>> end_time = int(time.time() * 1000)  # Now
            >>> response = client.invoice.get_invoice_list(
            ...     access_token=access_token,
            ...     start_date_long=start_time,
            ...     end_date_long=end_time,
            ...     sort_enum=2,  # Sort by creation time descending
            ...     page_num=1,
            ...     page_size=100
            ... )

            >>> # Filter by reference number and title type
            >>> response = client.invoice.get_invoice_list(
            ...     access_token=access_token,
            ...     ref_no="ORDER123456789",
            ...     title_type=2,  # Company invoices
            ...     page_num=1,
            ...     page_size=10
            ... )

        Note:
            对于大型数据集使用分页以提高性能。
            日期筛选使用Unix时间戳（毫秒）以进行精确控制。
            可用时发票文件可能包括图像和PDF格式。
        """
        request = GetInvoiceListRequest()
        request.invoice_status = invoice_status
        request.ref_no = ref_no
        request.start_date_long = start_date_long
        request.end_date_long = end_date_long
        request.page_num = page_num
        request.page_size = page_size
        request.sort_enum = sort_enum
        request.title_type = title_type
        request.method = "invoice.getInvoiceList"
        return self._execute(request, response_model=GetInvoiceListResponse)

    def confirm_invoice(
        self,
        xhs_invoice_no: str,
        ref_no: str,
        invoice_type: int,
        file: bytes,
        invoice_no: str,
        operator_id: str,
        operator_name: str,
    ) -> BaseResponse[str]:
        """开票结果回传（正向蓝票开具） (API: invoice.confirmInvoice).

        通过提供发票文件和详情来确认发票的上传和处理。此操作将发票标记为已完成，
        使客户可以下载。

        Args:
            xhs_invoice_no (str): 财务开票编码 (required)
            ref_no (str): 来源单号 (required)
            invoice_type (int): 发票类型，0:发票类型未知;1:增值税专用发票；2:增值税纸质普通发票；3:增值税电子普通发票；4:形式发票；5:电子专票；6:全电票电子普票；7:全电票纸质专票；8:全电票纸质普票 (required)
            file (bytes): 发票pdf文件字节数组，使用读取照片或视频后的byte[]数组， 请求转json时byte[]数组通过base64编码转成String (required)
            invoice_no (str): 发票号码，20位数字 (required)
            operator_id (str): 操作人 ID (required)
            operator_name (str): 操作人名称 (required)

        Returns:
            BaseResponse[str]: Response containing:
                - Operation status and confirmation message
                - Error information if confirmation fails

        Examples:
            >>> # Confirm invoice upload
            >>> with open("invoice_12345.pdf", "rb") as f:
            ...     invoice_content = f.read()
            >>>
            >>> response = client.invoice.confirm_invoice(
            ...     access_token=access_token,
            ...     xhs_invoice_no="XHS_INV_20240531001",
            ...     ref_no="ORDER123456789",
            ...     invoice_type=1,  # Regular invoice
            ...     file=invoice_content,
            ...     invoice_no="INV202405310001",
            ...     operator_id="OP001",
            ...     operator_name="张三"
            ... )

            >>> # Confirm VAT invoice
            >>> with open("vat_invoice.pdf", "rb") as f:
            ...     vat_content = f.read()
            >>>
            >>> response = client.invoice.confirm_invoice(
            ...     access_token=access_token,
            ...     xhs_invoice_no="XHS_INV_20240531002",
            ...     ref_no="ORDER987654321",
            ...     invoice_type=2,  # VAT invoice
            ...     file=vat_content,
            ...     invoice_no="VAT202405310001",
            ...     operator_id="OP002",
            ...     operator_name="李四"
            ... )

        Note:
            发票文件应为PDF格式以获得最佳兼容性。
            发票号码应与正式发票文件匹配。
            操作员信息用于审计跟踪和合规。
            此操作一旦成功确认即不可逆转。
        """
        request = ConfirmInvoiceRequest()
        request.xhs_invoice_no = xhs_invoice_no
        request.ref_no = ref_no
        request.invoice_type = invoice_type
        request.file = file
        request.invoice_no = invoice_no
        request.operator_id = operator_id
        request.operator_name = operator_name
        request.method = "invoice.confirmInvoice"
        return self._execute(request, response_model=str)

    def reverse_invoice(
        self,
        xhs_invoice_no: str,
        operator_id: str,
        operator_name: str,
    ) -> BaseResponse[str]:
        """发票冲红（逆向冲红） (API: invoice.reverseInvoice).

        执行发票冲红（红冲），这是中国会计实务中创建负项来取消或纠正之前开具的发票。
        这通常用于订单取消或发票纠正。

        Args:
            xhs_invoice_no (str): 系统开票号 (required)
            operator_id (str): 操作人 ID (required)
            operator_name (str): 操作人名称 (required)

        Returns:
            BaseResponse[str]: Response containing:
                - Reversal operation status and confirmation
                - Error information if reversal fails

        Examples:
            >>> # Reverse an invoice due to order cancellation
            >>> response = client.invoice.reverse_invoice(
            ...     access_token=access_token,
            ...     xhs_invoice_no="XHS_INV_20240531001",
            ...     operator_id="OP001",
            ...     operator_name="张三"
            ... )

            >>> # Reverse invoice for correction
            >>> response = client.invoice.reverse_invoice(
            ...     access_token=access_token,
            ...     xhs_invoice_no="XHS_INV_20240531002",
            ...     operator_id="OP003",
            ...     operator_name="王五"
            ... )

        Warning:
            发票冲红是影响会计记录的严重财务操作。
            在执行之前确保冲红是必要的并获得授权。
            已冲红的发票无法通过此API撤销冲红。

        Note:
            红冲（冲红）是中国会计实务中发票纠正的标准做法。
            操作员信息被记录用于审计和合规目的。
            冲红后，如订单仍然有效，可能需要开具新发票。
            请查阅当地税务法规中关于发票冲红程序的规定。
        """
        request = ReverseInvoiceRequest()
        request.xhs_invoice_no = xhs_invoice_no
        request.operator_id = operator_id
        request.operator_name = operator_name
        request.method = "invoice.reverseInvoice"
        return self._execute(request, response_model=str)
