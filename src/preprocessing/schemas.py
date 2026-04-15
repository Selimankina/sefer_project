from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import numpy as np


class PreprocessStatus(Enum):
    OK = "ok"
    FALLBACK = "fallback"
    ERROR = "error"


@dataclass
class PreprocessResult:
    image_path: Path
    status: PreprocessStatus
    roi: np.ndarray | None
    reason: str | None
    detection: object