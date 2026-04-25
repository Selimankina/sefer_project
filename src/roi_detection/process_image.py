import traceback
import numpy as np

from config import DATA_DIR
from src.roi_detection.detector import detect_rois
from src.common.schemas import ROI


def process_roi(image: np.ndarray) -> ROI | None:
    """
    Выбирает лучшую ROI из списка найденных.

    Шаги:
    - запускает детектор ROI;
    - если ничего не найдено — возвращает None;
    - выбирает ROI с максимальной уверенностью.

    Args:
        image (np.ndarray): Входное изображение.

    Returns:
        ROI | None: Лучшая найденная область интереса или None,
        если ROI не найдены или произошла ошибка.
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