from __future__ import annotations

from typing import Optional

import strawberry
from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from src.models.authors.author_models import Author


@strawberry.type
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Book:
    _id: strawberry.ID
    title: str
    author: Author
    price: float
    subtitle: Optional[str] = None
    description: Optional[str] = None
    isbn: Optional[str] = None
    book_format: Optional[str] = None
    rating: Optional[float] = None
    async_update_required: Optional[bool] = False
    created_on: Optional[str] = None
    last_updated_on: Optional[str] = None

    @property
    def id(self) -> strawberry.ID:
        return self._id
