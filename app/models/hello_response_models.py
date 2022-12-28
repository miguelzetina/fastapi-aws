from __future__ import annotations

import strawberry

from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class HelloResponse:
    message: str = None
    timestamp: str = None

