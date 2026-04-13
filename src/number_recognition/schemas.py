from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from src.digits_detection.schemas import Digit


class NumberStatus(Enum):
    OK = "ok"
    LOW_CONFIDENCE = "low_confidence"
    NO_NUMBER = "no_number"
    INVALID_FORMAT = "invalid_format"
    ERROR = "error"


@dataclass
class NumberResult:
    image_path: Path
    status: NumberStatus

    raw_number: str | None
    formatted_number: str | None 

    confidence: float | None

    digits: list[Digit] = field(default_factory=list)

    error_message: str | None = None