from __future__ import annotations

from typing import Generic, Optional, TypeVar

import strawberry

from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json


T = TypeVar('T')


@strawberry.type
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class BaseResponse:
    error_message: Optional[str]
    success: bool


@strawberry.type
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GetResponse(Generic[T], BaseResponse):
    result: Optional[T]


@strawberry.type
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CreateResponse(Generic[T], BaseResponse):
    result: Optional[T]


@strawberry.type
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpdateResponse(Generic[T], BaseResponse):
    result: Optional[T]


@strawberry.type
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DeleteResponse(Generic[T], BaseResponse):
    result: Optional[T]

