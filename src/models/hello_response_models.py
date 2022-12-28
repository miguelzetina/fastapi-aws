from __future__ import annotations

import strawberry

from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json


@strawberry.type
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class HelloResponse:
    message: str = None
    timestamp: str = None

