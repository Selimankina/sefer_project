from dataclasses import dataclass, field
import numpy as np
from pathlib import Path
from enum import Enum


class DigitDetectionStatus(Enum):
    OK = "ok"
    NO_DIGITS = "no_digits"
    ERROR = "error"


@dataclass
class Digit:
    bbox: np.ndarray  # (4, 2)
    label: str
    confidence: float

    @property
    def x(self) -> float:
        return float(self.bbox[:, 0].min())

    @property
    def y(self) -> float:
        return float(self.bbox[:, 1].min())

    @property
    def width(self) -> float:
        return float(self.bbox[:, 0].max() - self.bbox[:, 0].min())

    @property
    def height(self) -> float:
        return float(self.bbox[:, 1].max() - self.bbox[:, 1].min())

    @property
    def center_x(self) -> float:
        return float(self.bbox[:, 0].mean())

    @property
    def center_y(self) -> float:
        return float(self.bbox[:, 1].mean())

@dataclass
class DigitDetectionResult:
    image_path: Path
    status: DigitDetectionStatus

    roi: np.ndarray | None

    digits: list[Digit] = field(default_factory=list)

    error_message: str | None = None