from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum


# --- Статус детекции ROI ---
class DetectionStatus(Enum):
    OK = "ok"
    MULTIPLE_PLATES = "multiple_plates"
    NO_PLATE = "no_plate"
    ERROR = "error"


# --- Одна табличка ---
@dataclass
class ROI:
    bbox: list[int]
    confidence: float
    keypoints: list[list[float]] | None


# --- Результат детекции ROI ---
@dataclass
class DetectionResult:
    image_path: Path
    status: DetectionStatus

    rois: list[ROI] = field(default_factory=list)
    best_roi: ROI | None = None

    error_message: str | None = None