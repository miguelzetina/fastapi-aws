from __future__ import annotations

from datetime import datetime

from typing import Optional

import strawberry

from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json


@strawberry.type
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Review:
    _id: strawberry.ID
    book_id: str
    review_id: str
    rating: float
    review_comments: str
    created_on: datetime = None
    last_udpated_on: Optional[datetime] = None

    @property
    def id(self) -> strawberry.ID:
        return self._id
