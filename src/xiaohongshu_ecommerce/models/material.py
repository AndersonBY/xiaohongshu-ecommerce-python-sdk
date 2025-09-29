"""Material library models for Xiaohongshu e-commerce API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .base import BaseRequest


class MaterialType(Enum):
    """Material type enumeration."""

    IMAGE = 0
    VIDEO = 1


@dataclass
class MaterialDetail:
    """Material detail information."""

    material_id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[MaterialType] = None
    url: Optional[str] = None
    file_size: Optional[int] = None
    upload_time: Optional[int] = None
    update_time: Optional[int] = None
    status: Optional[int] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)


# Request models
@dataclass
class UploadMaterialInfoRequest(BaseRequest):
    """Upload material info request."""

    name: Optional[str] = None
    type: Optional[MaterialType] = None
    material_content: Optional[bytes] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> Dict[str, Any]:
        payload = {}
        if self.name is not None:
            payload["name"] = self.name
        if self.type is not None:
            payload["type"] = (
                self.type.value if isinstance(self.type, MaterialType) else self.type
            )
        if self.material_content is not None:
            payload["materialContent"] = self.material_content
        if self.description is not None:
            payload["description"] = self.description
        if self.tags:
            payload["tags"] = self.tags
        return payload


@dataclass
class UpdateMaterialInfoRequest(BaseRequest):
    """Update material info request."""

    material_id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[MaterialType] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> Dict[str, Any]:
        payload = {}
        if self.material_id is not None:
            payload["materialId"] = self.material_id
        if self.name is not None:
            payload["name"] = self.name
        if self.type is not None:
            payload["type"] = (
                self.type.value if isinstance(self.type, MaterialType) else self.type
            )
        if self.description is not None:
            payload["description"] = self.description
        if self.tags:
            payload["tags"] = self.tags
        return payload


@dataclass
class DeleteMaterialInfoRequest(BaseRequest):
    """Delete material info request."""

    material_id: Optional[str] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> Dict[str, Any]:
        payload = {}
        if self.material_id is not None:
            payload["materialId"] = self.material_id
        return payload


@dataclass
class QueryMaterialInfoRequest(BaseRequest):
    """Query material info request."""

    material_id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[MaterialType] = None
    page_no: Optional[int] = None
    page_size: Optional[int] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None

    def __post_init__(self):
        super().__init__(method="")

    def extra_payload(self) -> Dict[str, Any]:
        payload = {}
        if self.material_id is not None:
            payload["materialId"] = self.material_id
        if self.name is not None:
            payload["name"] = self.name
        if self.type is not None:
            payload["type"] = (
                self.type.value if isinstance(self.type, MaterialType) else self.type
            )
        if self.page_no is not None:
            payload["pageNo"] = self.page_no
        if self.page_size is not None:
            payload["pageSize"] = self.page_size
        if self.start_time is not None:
            payload["createTimeStart"] = self.start_time
        if self.end_time is not None:
            payload["createTimeEnd"] = self.end_time
        return payload


# Response models
@dataclass
class QueryMaterialInfoResponse:
    """Query material info response."""

    total: int = 0
    page_no: int = 0
    page_size: int = 0
    max_page_no: int = 0
    material_list: List[MaterialDetail] = field(default_factory=list)
