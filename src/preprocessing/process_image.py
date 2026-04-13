import cv2
import numpy as np

from src.roi_detection.schemas import DetectionStatus

from .validators import validate_keypoints, validate_geometry
from .transforms import perspective_transform, normalize_orientation
from .crop import resize_to_height, crop_roi
from .schemas import PreprocessResult, PreprocessStatus


KPT_CONF_THRESHOLD = 0.5


def process_image(detection) -> PreprocessResult:
    image_path = detection.image_path
    image = cv2.imread(str(image_path))

    if image is None:
        return PreprocessResult(image_path, None, PreprocessStatus.ERROR, "image_read_error", detection)

    if detection.status not in (
        DetectionStatus.OK,
        DetectionStatus.MULTIPLE_PLATES
    ):
        return PreprocessResult(image_path, None, PreprocessStatus.ERROR, detection.status.value, detection)

    roi_obj = detection.best_roi

    if roi_obj is None:
        return PreprocessResult(
            image_path,
            None,
            PreprocessStatus.ERROR,
            "no_best_roi",
            detection
        )

    keypoints = roi_obj.keypoints
    roi = None
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

    # --- fallback ---
    if fallback:
        bbox = roi_obj.bbox

        if bbox is None:
            return PreprocessResult(
                image_path,
                None,
                PreprocessStatus.ERROR,
                reason,
                detection
            )

        x1, y1, x2, y2 = bbox
        h, w = image.shape[:2]
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)

        if x2 <= x1 or y2 <= y1:
            return PreprocessResult(
                image_path,
                None,
                PreprocessStatus.ERROR,
                "invalid_bbox",
                detection
            )

        roi = image[y1:y2, x1:x2]

    # --- финал ---
    roi = normalize_orientation(roi)
    roi = resize_to_height(roi)
    roi = crop_roi(roi)

    status = PreprocessStatus.FALLBACK if fallback else PreprocessStatus.OK

    return PreprocessResult(image_path, roi, status, reason, detection)