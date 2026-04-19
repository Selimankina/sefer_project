import numpy as np

from src.preprocessing.validators import validate_keypoints, validate_geometry
from src.preprocessing.transforms import perspective_transform, normalize_orientation
from src.preprocessing.crop import resize_to_height, crop_roi

from config.settings import KPT_CONF_THRESHOLD


def process_preprocessing(image: np.ndarray, roi_obj):
    """
        Выполняет предобработку ROI изображения.

        Шаги обработки:
        - проверка keypoints;
        - проверка геометрии;
        - перспективное преобразование (warp);
        - при ошибке используется fallback через bbox;
        - нормализация ориентации;
        - ресайз и кроп.

        Args:
            image (np.ndarray): Исходное изображение.
            roi_obj: Объект ROI с keypoints и bbox.

        Returns:
            tuple[np.ndarray | None, dict]:
                roi (np.ndarray | None): Обработанная область интереса.
                meta (dict): Информация о процессе (fallback, причина ошибки).
        """
    keypoints = roi_obj.keypoints

    fallback = False
    reason = None

    # --- keypoints ---
    if not validate_keypoints(keypoints, KPT_CONF_THRESHOLD):
        fallback = True
        reason = "invalid_keypoints"

    # --- geometry ---
    if not fallback:
        rect = np.array([[kp[0], kp[1]] for kp in keypoints], dtype="float32")

        if not validate_geometry(rect):
            fallback = True
            reason = "invalid_geometry"

    # --- warp ---
    if not fallback:
        roi = perspective_transform(image, rect)

        if roi is None:
            fallback = True
            reason = "warp_failed"
    else:
        roi = None

    # --- fallback ---
    if fallback:
        bbox = roi_obj.bbox

        if bbox is None:
            return None, {"error": "no_bbox", "fallback": True}

        x1, y1, x2, y2 = bbox
        h, w = image.shape[:2]

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)

        if x2 <= x1 or y2 <= y1:
            return None, {"error": "invalid_bbox", "fallback": True}

        roi = image[y1:y2, x1:x2]

    # --- финал ---
    roi = normalize_orientation(roi)
    roi = resize_to_height(roi)
    roi = crop_roi(roi)

    return roi, {
        "fallback": fallback,
        "reason": reason,
    }