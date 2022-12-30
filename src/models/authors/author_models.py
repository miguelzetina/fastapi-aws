from __future__ import annotations

from typing import Optional

import strawberry

from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json


@strawberry.input
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AuthorInput:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None


@strawberry.type
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None

