from dataclasses import dataclass
from typing import List, Optional
import numpy as np


@dataclass
class ROI:
    """
    Region of Interest (табличка).
    """
    bbox: List[int]  # [x1, y1, x2, y2]
    confidence: float
    keypoints: Optional[List[List[float]]] = None



@dataclass
class Digit:
    """
    Одна распознанная цифра.
    """
    bbox: np.ndarray  # shape (4, 2)
    label: str        # "0"-"9"
    confidence: float

    @property
    def center_x(self) -> float:
        return float(self.bbox[:, 0].mean())

    @property
    def center_y(self) -> float:
        return float(self.bbox[:, 1].mean())

    @property
    def width(self) -> float:
        return float(
            np.linalg.norm(self.bbox[1] - self.bbox[0])
        )

    @property
    def height(self) -> float:
        return float(
            np.linalg.norm(self.bbox[3] - self.bbox[0])
        )