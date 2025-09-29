"""Data processing and privacy protection client for Xiaohongshu e-commerce API."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from .base import SyncSubClient
from ..models import (
    BatchDecryptRequest,
    BatchDecryptResponse,
    BatchDesensitiseRequest,
    BatchDesensitiseResponse,
    BatchIndexRequest,
    BatchIndexResponse,
    DecryptItem,
    IndexItem,
)


if TYPE_CHECKING:  # pragma: no cover
    from ..models import BaseResponse


class DataClient(SyncSubClient):
    """数据处理和隐私保护API的同步客户端。

    数据模块为小红书电商平台提供重要的数据安全和隐私保护服务。
    包括敏感数据的加密/解密、隐私保护的数据脱敏，以及在保持隐私合规的同时
    为可搜索数据生成索引。
    """

    def batch_decrypt(
        self, base_infos: List[DecryptItem], action_type: str, app_user_id: str
    ) -> "BaseResponse[BatchDecryptResponse]":
        """批量解密 - 数据解密 (API: data.batchDecrypt).

        在单个请求中解密多个加密数据项。此API用于为授权操作（如订单履行和客户服务）
        显示敏感信息，如客户联系详情。

        Args:
            base_infos (List[DecryptItem]): 加密数据列表，上限100条 (required):
                - data_tag (str): 标签，订单场景为packageId（具体订单号），售后场景为returnId（具体售后单号）
                - encrypted_data (str): 密文数据
            action_type (str): 操作类型1 - 单个查看订单明文，2 - 批量解密打单，3 - 批量解密后面向三方的数据下发，4 - 其他场景,解密接口必填 (required)
            app_user_id (str): 旧逻辑字段无实际意义，由服务商自定义，非空即可 (required)

        Returns:
            BaseResponse[BatchDecryptResponse]: Response containing:
                - data_info_list (List[DecryptedInfo]): List of decryption results

        Examples:
            >>> # Decrypt customer contact information for order fulfillment
            >>> from xiaohongshu_ecommerce.models.data import DecryptItem
            >>>
            >>> # Create decrypt items
            >>> decrypt_items = [
            ...     DecryptItem(
            ...         data_tag="customer_phone_001",
            ...         encrypted_data="ENC_123456789ABCDEF"
            ...     ),
            ...     DecryptItem(
            ...         data_tag="customer_address_001",
            ...         encrypted_data="ENC_987654321FEDCBA"
            ...     )
            ... ]
            >>>
            >>> # Decrypt data
            >>> response = client.data.batch_decrypt(
            ...     access_token=access_token,
            ...     base_infos=decrypt_items,
            ...     action_type="ORDER_FULFILLMENT",
            ...     app_user_id="user_12345"
            ... )
            >>> for item in response.data.data_info_list:
            ...     if item.error_code == 0:
            ...         print(f"Decrypted {item.data_tag}: {item.decrypted_data}")
            ...     else:
            ...         print(f"Failed to decrypt {item.data_tag}: {item.error_msg}")

            >>> # Decrypt for customer service operations
            >>> service_items = [
            ...     DecryptItem(
            ...         data_tag="complaint_phone",
            ...         encrypted_data="ENC_COMPLAINT_123"
            ...     )
            ... ]
            >>> response = client.data.batch_decrypt(
            ...     access_token=access_token,
            ...     base_infos=service_items,
            ...     action_type="CUSTOMER_SERVICE",
            ...     app_user_id="service_agent_001"
            ... )

        Note:
            解密操作被记录和审计以保证合规目的。
            在客户联系期间可能提供虚拟号码以保护隐私。
            只有授权的操作类型和用户才能解密敏感数据。
            解密的数据应安全处理，不应以明文存储。
        """
        request = BatchDecryptRequest(
            base_infos=base_infos,
            action_type=action_type,
            app_user_id=app_user_id,
        )
        return self._execute(request, response_model=BatchDecryptResponse)

    def batch_desensitise(
        self, base_infos: List[DecryptItem]
    ) -> "BaseResponse[BatchDesensitiseResponse]":
        """批量脱敏 - 数据脱敏 (API: data.batchDesensitise).

        将加密的敏感数据转换为适合在用户界面中显示的脱敏格式，同时保护隐私。
        这允许显示部分信息（如遮罩的电话号码）而无需完全解密。

        Args:
            base_infos (List[DecryptItem]): 加密数据列表，上限100条 (required):
                - data_tag (str): 标签，订单场景为packageId（具体订单号），售后场景为returnId（具体售后单号）
                - encrypted_data (str): 密文数据

        Returns:
            BaseResponse[BatchDesensitiseResponse]: Response containing:
                - desensitise_info_list (List[DesensitiseInfo]): List of desensitization results

        Examples:
            >>> # Desensitize customer data for UI display
            >>> from xiaohongshu_ecommerce.models.data import DecryptItem
            >>>
            >>> # Create items to desensitize
            >>> desensitize_items = [
            ...     DecryptItem(
            ...         data_tag="customer_phone_display",
            ...         encrypted_data="ENC_13800138000"
            ...     ),
            ...     DecryptItem(
            ...         data_tag="customer_email_display",
            ...         encrypted_data="ENC_user@example.com"
            ...     ),
            ...     DecryptItem(
            ...         data_tag="customer_address_display",
            ...         encrypted_data="ENC_北京市朝阳区xxx街道123号"
            ...     )
            ... ]
            >>>
            >>> # Desensitize data
            >>> response = client.data.batch_desensitise(
            ...     access_token=access_token,
            ...     base_infos=desensitize_items
            ... )
            >>> for item in response.data.desensitise_info_list:
            ...     if item.error_code == 0:
            ...         print(f"Display {item.data_tag}: {item.desensitised_data}")
            ...         # Expected output examples:
            ...         # "Display customer_phone_display: 138****8000"
            ...         # "Display customer_email_display: u***@example.com"
            ...         # "Display customer_address_display: 北京市朝阳区***"
            ...     else:
            ...         print(f"Failed to desensitize {item.data_tag}: {item.error_msg}")

            >>> # Desensitize single item
            >>> single_item = [
            ...     DecryptItem(
            ...         data_tag="id_card_display",
            ...         encrypted_data="ENC_110101199001011234"
            ...     )
            ... ]
            >>> response = client.data.batch_desensitise(
            ...     access_token=access_token,
            ...     base_infos=single_item
            ... )

        Note:
            脱敏数据可安全在用户界面和日志中显示。
            脱敏程度取决于数据类型和隐私要求。
            常见模式：电话号码（138****8000）、邮箱（u***@domain.com）。
            此操作不需要action_type或user_id，与解密不同。
        """
        request = BatchDesensitiseRequest(base_infos=base_infos)
        return self._execute(request, response_model=BatchDesensitiseResponse)

    def batch_index(
        self, index_infos: List[IndexItem]
    ) -> "BaseResponse[BatchIndexResponse]":
        """批量获取索引串 - 索引串查询 (API: data.batchIndex).

        从明文数据生成可搜索索引，同时保持隐私保护。这允许数据可搜索
        而无需存储或暴露原始明文。常用于订单搜索和客户查找。

        Args:
            index_infos (List[IndexItem]): 索引串查询列表 (required):
                - plain_text (str): 关键词
                - type (int): 类型1：地址，2：姓名，3：电话，4：身份证号，5：身份证照片链接

        Returns:
            BaseResponse[BatchIndexResponse]: Response containing:
                - index_info_list (List[IndexInfo]): List of indexing results

        Examples:
            >>> # Generate search indexes for customer data
            >>> from xiaohongshu_ecommerce.models.data import IndexItem
            >>>
            >>> # Create index items
            >>> index_items = [
            ...     IndexItem(
            ...         plain_text="13800138000",
            ...         type=1  # Phone number
            ...     ),
            ...     IndexItem(
            ...         plain_text="customer@example.com",
            ...         type=2  # Email address
            ...     ),
            ...     IndexItem(
            ...         plain_text="张三",
            ...         type=4  # Name
            ...     ),
            ...     IndexItem(
            ...         plain_text="北京市朝阳区建国门外大街1号",
            ...         type=5  # Address
            ...     )
            ... ]
            >>>
            >>> # Generate indexes
            >>> response = client.data.batch_index(
            ...     access_token=access_token,
            ...     index_infos=index_items
            ... )
            >>> for item in response.data.index_info_list:
            ...     print(f"Index for '{item.plain_text}': {item.search_index}")
            ...     # Store search_index for later search operations

            >>> # Generate index for single identity card
            >>> id_card_item = [
            ...     IndexItem(
            ...         plain_text="110101199001011234",
            ...         type=3  # Identity card
            ...     )
            ... ]
            >>> response = client.data.batch_index(
            ...     access_token=access_token,
            ...     index_infos=id_card_item
            ... )

            >>> # Example usage in search scenario
            >>> # 1. Generate index when storing data
            >>> phone_index_items = [IndexItem(plain_text="13912345678", type=1)]
            >>> index_response = client.data.batch_index(
            ...     access_token=access_token,
            ...     index_infos=phone_index_items
            ... )
            >>> search_index = index_response.data.index_info_list[0].search_index
            >>>
            >>> # 2. Store search_index in database for later searches
            >>> # database.store_customer_search_index(customer_id, search_index)
            >>>
            >>> # 3. During search, generate index for search term
            >>> search_term_items = [IndexItem(plain_text="13912345678", type=1)]
            >>> search_response = client.data.batch_index(
            ...     access_token=access_token,
            ...     index_infos=search_term_items
            ... )
            >>> search_key = search_response.data.index_info_list[0].search_index
            >>>
            >>> # 4. Match search_key against stored indexes
            >>> # results = database.find_by_search_index(search_key)

        Note:
            搜索索引是单向转换 - 无法恢复原始数据。
            相同明文始终生成相同的搜索索引。
            不同数据类型使用不同的索引算法以获得最佳搜索效果。
            安全存储生成的索引以供搜索操作。
            索引生成是确定性的，不可逆搜索。
        """
        request = BatchIndexRequest(index_infos=index_infos)
        return self._execute(request, response_model=BatchIndexResponse)
