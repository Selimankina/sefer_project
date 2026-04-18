import traceback
import numpy as np

from src.roi_detection.detector import detect_rois
from src.common.schemas import ROI


def process_roi(image: np.ndarray) -> ROI | None:
    """
    Возвращает лучшую ROI или None.
    """

    try:
        rois = detect_rois(image)

        if not rois:
            return None

        best_roi = max(rois, key=lambda r: r.confidence)

        return best_roi

    except Exception:
        print(traceback.format_exc())
        return None