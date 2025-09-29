"""Data module models."""

from __future__ import annotations

from collections.abc import Mapping as MappingABC, Sequence as SequenceABC
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Sequence, Type, TypeVar, Protocol

from .base import BaseRequest


@dataclass
class DecryptItem:
    data_tag: str
    encrypted_data: str

    def to_payload(self) -> Dict[str, str]:
        return {
            "dataTag": self.data_tag,
            "encryptedData": self.encrypted_data,
        }


@dataclass
class IndexItem:
    plain_text: str
    type: int

    def to_payload(self) -> Dict[str, object]:
        return {"plainText": self.plain_text, "type": self.type}


class BatchDecryptRequest(BaseRequest):
    def __init__(
        self, base_infos: Sequence[DecryptItem], action_type: str, app_user_id: str
    ) -> None:
        super().__init__(method="data.batchDecrypt")
        self.base_infos = list(base_infos)
        self.action_type = action_type
        self.app_user_id = app_user_id

    def extra_payload(self) -> Dict[str, object]:
        return {
            "baseInfos": [item.to_payload() for item in self.base_infos],
            "actionType": self.action_type,
            "appUserId": self.app_user_id,
        }


class BatchDesensitiseRequest(BaseRequest):
    def __init__(self, base_infos: Sequence[DecryptItem]) -> None:
        super().__init__(method="data.batchDesensitise")
        self.base_infos = list(base_infos)

    def extra_payload(self) -> Dict[str, object]:
        return {"baseInfos": [item.to_payload() for item in self.base_infos]}


class BatchIndexRequest(BaseRequest):
    def __init__(self, index_infos: Sequence[IndexItem]) -> None:
        super().__init__(method="data.batchIndex")
        self.index_infos = list(index_infos)

    def extra_payload(self) -> Dict[str, object]:
        return {"indexBaseInfoList": [item.to_payload() for item in self.index_infos]}


@dataclass
class DecryptedInfo:
    data_tag: str
    encrypted_data: str
    decrypted_data: str
    error_code: int
    error_msg: str
    virtual_number: str | None = None
    virtual_number_flag: bool = False
    virtual_phone_number: str | None = None
    virtual_extend_number: str | None = None
    expire_at: int | None = None

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "DecryptedInfo":
        return cls(
            data_tag=str(data.get("dataTag", "")),
            encrypted_data=str(data.get("encryptedData", "")),
            decrypted_data=str(data.get("decryptedData", "")),
            error_code=_int(data.get("errorCode")),
            error_msg=str(data.get("errorMsg", "")),
            virtual_number=_opt_str(data.get("virtualNumber")),
            virtual_number_flag=bool(data.get("virtualNumberFlag", False)),
            virtual_phone_number=_opt_str(data.get("virtualPhoneNumber")),
            virtual_extend_number=_opt_str(data.get("virtualExtendNumber")),
            expire_at=_opt_int(data.get("expireAt")),
        )


@dataclass
class DesensitiseInfo:
    data_tag: str
    encrypted_data: str
    desensitised_data: str
    error_code: int
    error_msg: str

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "DesensitiseInfo":
        return cls(
            data_tag=str(data.get("dataTag", "")),
            encrypted_data=str(data.get("encryptedData", "")),
            desensitised_data=str(data.get("desensitisedData", "")),
            error_code=_int(data.get("errorCode")),
            error_msg=str(data.get("errorMsg", "")),
        )


@dataclass
class IndexInfo:
    plain_text: str
    search_index: str

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "IndexInfo":
        return cls(
            plain_text=str(data.get("plainText", "")),
            search_index=str(data.get("searchIndex", "")),
        )


@dataclass
class BatchDecryptResponse:
    data_info_list: List[DecryptedInfo]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "BatchDecryptResponse":
        items = _coerce_many(data.get("dataInfoList"), DecryptedInfo)
        return cls(data_info_list=items)


@dataclass
class BatchDesensitiseResponse:
    desensitise_info_list: List[DesensitiseInfo]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "BatchDesensitiseResponse":
        items = _coerce_many(data.get("desensitiseInfoList"), DesensitiseInfo)
        return cls(desensitise_info_list=items)


@dataclass
class BatchIndexResponse:
    index_info_list: List[IndexInfo]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "BatchIndexResponse":
        items = _coerce_many(data.get("indexInfoList"), IndexInfo)
        return cls(index_info_list=items)


def _opt_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)


def _opt_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _int(value: Any, default: int = 0) -> int:
    result = _opt_int(value)
    return result if result is not None else default


_ModelT = TypeVar("_ModelT", bound="_SupportsFromDict")


class _SupportsFromDict(Protocol):
    @classmethod
    def from_dict(cls: Type[_ModelT], data: Mapping[str, object]) -> _ModelT: ...


def _coerce(raw: object, model: Type[_ModelT]) -> _ModelT:
    if isinstance(raw, MappingABC):
        return model.from_dict(raw)
    raise TypeError("Expected mapping for model conversion")


def _coerce_many(raw: object, model: Type[_ModelT]) -> List[_ModelT]:
    return [_coerce(item, model) for item in _mapping_sequence(raw)]


def _mapping_sequence(raw: object) -> List[Mapping[str, object]]:
    if raw is None:
        return []
    if isinstance(raw, MappingABC):
        return [raw]
    if isinstance(raw, SequenceABC) and not isinstance(raw, (str, bytes, bytearray)):
        items: List[Mapping[str, object]] = []
        for item in raw:
            if isinstance(item, MappingABC):
                items.append(item)
        return items
    return []


__all__ = [
    "DecryptItem",
    "IndexItem",
    "BatchDecryptRequest",
    "BatchDesensitiseRequest",
    "BatchIndexRequest",
    "DecryptedInfo",
    "DesensitiseInfo",
    "IndexInfo",
    "BatchDecryptResponse",
    "BatchDesensitiseResponse",
    "BatchIndexResponse",
]
