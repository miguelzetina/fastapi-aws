from __future__ import annotations

import strawberry

from enum import Enum
from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json


@strawberry.enum
@dataclass_json(letter_case=LetterCase.CAMEL)
class DatabaseCollectionTypes(Enum):
    BOOKS = 'books'
    REVIEWS = 'reviews'


@strawberry.type
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GetRecord:
    success: bool
    record_id: str = None
    error_message: str = None


@strawberry.type
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CreateRecord:
    success: bool
    record_id: str = None
    error_message: str = None


@strawberry.type
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpdateRecord:
    success: bool
    record_id: str = None
    error_message: str = None


@strawberry.type
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DeleteRecord:
    success: bool
    record_id: str = None
    error_message: str = None

