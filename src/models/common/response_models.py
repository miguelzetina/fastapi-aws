from __future__ import annotations

from typing import Generic, Optional, TypeVar

import strawberry

from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json


T = TypeVar('T')


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class BaseResponse:
    error_message: Optional[str]
    success: bool


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class GetResponse(Generic[T], BaseResponse):
    result: Optional[T]
    record_id: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class CreateResponse(Generic[T], BaseResponse):
    result: Optional[T]
    record_id: Optional[str] = None

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class UpdateResponse(Generic[T], BaseResponse):
    result: Optional[T]
    record_id: Optional[str] = None

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class DeleteResponse(Generic[T], BaseResponse):
    result: Optional[T]
    record_id: Optional[str] = None
