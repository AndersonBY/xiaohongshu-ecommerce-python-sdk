"""Material library management client for Xiaohongshu e-commerce API."""

from typing import List, Optional

from ..models.base import BaseResponse
from ..models.material import (
    DeleteMaterialInfoRequest,
    MaterialDetail,
    MaterialType,
    QueryMaterialInfoRequest,
    QueryMaterialInfoResponse,
    UpdateMaterialInfoRequest,
    UploadMaterialInfoRequest,
)
from .base import SyncSubClient


class MaterialClient(SyncSubClient):
    """素材中心API的同步客户端。

    素材中心提供小红书电商平台数字资产（图片和视频）的集中管理。
    此客户端处理平台素材库中素材的上传、更新、查询和删除操作。
    """

    def upload_material(
        self,
        name: Optional[str] = None,
        type: Optional[MaterialType] = None,
        material_content: Optional[bytes] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> BaseResponse[MaterialDetail]:
        """上传素材 (API: material.uploadMaterial).

        上传图片或视频素材到小红书素材库中心。上传成功后，素材可以在多个商品和营销活动中被引用。

        Args:
            name (Optional[str]): 素材名
            type (Optional[MaterialType]): 素材类型，MaterialType.IMAGE或MaterialType.VIDEO:
                - MaterialType.IMAGE: 图片素材
                - MaterialType.VIDEO: 视频素材
            material_content (Optional[bytes]): 素材文件字节数组，使用读取照片或视频后的byte[]数组，请求转json时byte[]数组通过base64编码转成String
            description (Optional[str]): 素材描述
            tags (Optional[List[str]]): 素材标签列表

        Returns:
            BaseResponse[MaterialDetail]: 响应包含上传的素材详情:
                - materialId (str): 素材id
                - name (str): 素材名
                - type (str): 素材类型 (IMAGE or VIDEO)
                - url (str): 素材小红书内链url
                - width (int): 图片宽度 (图片类型)
                - height (int): 图片高度 (图片类型)
                - duration (float): 视频时长,double (视频类型)
                - status (int): 状态,1:上传成功，2：上传中，3：上传失败
                - createTime (int): 创建时间 ms
                - updateTime (int): 更新时间 ms

        Examples:
            >>> # 上传图片素材
            >>> import base64
            >>> with open("product_image.jpg", "rb") as f:
            ...     content = base64.b64encode(f.read())
            >>> response = client.material.upload_material(
            ...     access_token=access_token,
            ...     name="商品主图",
            ...     type=MaterialType.IMAGE,
            ...     material_content=content
            ... )

            >>> # 上传视频素材
            >>> with open("product_video.mp4", "rb") as f:
            ...     content = base64.b64encode(f.read())
            >>> response = client.material.upload_material(
            ...     access_token=access_token,
            ...     name="商品演示视频",
            ...     type=MaterialType.VIDEO,
            ...     material_content=content,
            ...     description="商品演示视频",
            ...     tags=["商品", "演示"]
            ... )

        Note:
            文件必须在上传前转换为base64编码字符串。
            大文件可能需要时间处理 - 检查响应中的状态字段。
            返回的URL可用于在商品列表中引用此素材。
        """
        request = UploadMaterialInfoRequest(
            name=name,
            type=type,
            material_content=material_content,
            description=description,
            tags=tags or [],
        )
        request.method = "material.uploadMaterial"
        return self._execute(request, response_model=MaterialDetail)

    def update_material(
        self,
        material_id: Optional[str] = None,
        name: Optional[str] = None,
        type: Optional[MaterialType] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> BaseResponse[MaterialDetail]:
        """修改素材 (API: material.updateMaterial).

        更新素材库中现有素材的元数据信息。此操作仅修改素材信息，不更改实际文件内容。

        Args:
            material_id (Optional[str]): 素材id
            name (Optional[str]): 素材名
            type (Optional[MaterialType]): 素材类型
            description (Optional[str]): 更新的素材描述
            tags (Optional[List[str]]): 更新的素材标签列表

        Returns:
            BaseResponse[MaterialDetail]: 响应包含更新的素材详情:
                - materialId (str): 素材id (不变)
                - name (str): 素材名 (已更新)
                - type (str): 素材类型 (IMAGE or VIDEO)
                - url (str): 素材小红书内链url (不变)
                - width (int): 图片宽度 (图片类型)
                - height (int): 图片高度 (图片类型)
                - duration (float): 视频时长,double (视频类型)
                - status (int): 状态,1:上传成功，2：上传中，3：上传失败
                - createTime (int): 创建时间 ms (原始)
                - updateTime (int): 更新时间 ms (已更新)

        Examples:
            >>> # 更新素材名称
            >>> response = client.material.update_material(
            ...     access_token=access_token,
            ...     material_id="mat_123456789",
            ...     name="更新的商品图片"
            ... )

            >>> # 从之前的上传获取素材ID
            >>> upload_response = client.material.upload_material(
            ...     access_token=access_token,
            ...     name="商品图片",
            ...     type=MaterialType.IMAGE,
            ...     material_content=content
            ... )
            >>> material_id = upload_response.data.material_id
            >>>
            >>> # 更新上传的素材
            >>> response = client.material.update_material(
            ...     access_token=access_token,
            ...     material_id=material_id,
            ...     name="重命名的素材",
            ...     description="更新的描述",
            ...     tags=["更新", "新标签"]
            ... )

        Note:
            此操作仅更新元数据。要更改实际文件内容，
            需要上传新素材并相应更新引用。
            素材URL和类型无法通过此操作更改。
        """
        request = UpdateMaterialInfoRequest(
            material_id=material_id,
            name=name,
            type=type,
            description=description,
            tags=tags or [],
        )
        request.method = "material.updateMaterial"
        return self._execute(request, response_model=MaterialDetail)

    def delete_material(
        self,
        material_id: Optional[str] = None,
    ) -> BaseResponse[str]:
        """删除素材 (API: material.deleteMaterial).

        从素材库中永久删除素材。此操作无法撤销，将影响当前使用此素材的所有商品或营销活动。

        Args:
            material_id (Optional[str]): 素材id

        Returns:
            BaseResponse[str]: 响应包含:
                - 删除确认消息
                - 操作状态信息

        Examples:
            >>> # 通过ID删除素材
            >>> response = client.material.delete_material(
            ...     access_token=access_token,
            ...     material_id="mat_123456789"
            ... )

            >>> # 上传后删除素材
            >>> upload_response = client.material.upload_material(
            ...     access_token=access_token,
            ...     name="商品图片",
            ...     type=MaterialType.IMAGE,
            ...     material_content=content
            ... )
            >>> material_id = upload_response.data.material_id
            >>>
            >>> # 稍后删除素材
            >>> response = client.material.delete_material(
            ...     access_token=access_token,
            ...     material_id=material_id
            ... )

        Warning:
            此操作永久删除素材且无法撤销。
            删除前请确保素材未在活跃的商品或活动中使用。

        Note:
            删除在活跃商品中引用的素材可能导致显示问题。
            删除前请考虑更新商品引用。
        """
        request = DeleteMaterialInfoRequest(material_id=material_id)
        request.method = "material.deleteMaterial"
        return self._execute(request, response_model=str)

    def query_material(
        self,
        material_id: Optional[str] = None,
        name: Optional[str] = None,
        type: Optional[MaterialType] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ) -> BaseResponse[QueryMaterialInfoResponse]:
        """素材列表 (API: material.queryMaterial).

        从素材库查询素材列表，支持按类型、状态、创建时间和名称等多种条件进行筛选。

        Args:
            material_id (Optional[str]): 素材id
            name (Optional[str]): 素材名 (支持部分匹配)
            type (Optional[MaterialType]): 素材类型:
                - MaterialType.IMAGE: 仅筛选图片素材
                - MaterialType.VIDEO: 仅筛选视频素材
            page_no (Optional[int]): 分页查询，页码 (默认: 1)
            page_size (Optional[int]): 分页查询，页面大小 (默认: 20)
            start_time (Optional[int]): 创建开始时间 ms
            end_time (Optional[int]): 创建结束时间 ms

        Returns:
            BaseResponse[QueryMaterialInfoResponse]: 响应包含:
                - materialDetailList (List[MaterialDetail]): 匹配的素材列表:
                    - 每个MaterialDetail包含完整的素材信息
                    - 包括materialId、name、type、url、尺寸、状态、时间戳
                - 分页信息通过pageNo和pageSize参数处理

        Examples:
            >>> # 查询所有素材并分页
            >>> response = client.material.query_material(
            ...     access_token=access_token,
            ...     page_no=1,
            ...     page_size=20
            ... )

            >>> # 按类型查询素材
            >>> response = client.material.query_material(
            ...     access_token=access_token,
            ...     type=MaterialType.IMAGE,
            ...     page_no=1,
            ...     page_size=50
            ... )

            >>> # 按名称筛选查询素材
            >>> response = client.material.query_material(
            ...     access_token=access_token,
            ...     name="商品",  # 部分匹配
            ...     page_no=1,
            ...     page_size=30
            ... )

            >>> # 按日期范围查询素材
            >>> import time
            >>> week_ago = int((time.time() - 7 * 24 * 3600) * 1000)
            >>> now = int(time.time() * 1000)
            >>> response = client.material.query_material(
            ...     access_token=access_token,
            ...     start_time=week_ago,
            ...     end_time=now,
            ...     page_no=1,
            ...     page_size=100
            ... )

            >>> # 按ID查询特定素材
            >>> response = client.material.query_material(
            ...     access_token=access_token,
            ...     material_id="mat_123456789"
            ... )

        Note:
            对于大型结果集使用分页以避免性能问题。
            名称筛选支持部分匹配以便灵活搜索。
            时间筛选使用毫秒级Unix时间戳以实现精确控制。
        """
        request = QueryMaterialInfoRequest(
            material_id=material_id,
            name=name,
            type=type,
            page_no=page_no,
            page_size=page_size,
            start_time=start_time,
            end_time=end_time,
        )
        request.method = "material.queryMaterial"
        return self._execute(request, response_model=QueryMaterialInfoResponse)
