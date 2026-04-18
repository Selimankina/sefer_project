import cv2
import numpy as np

from config.settings import TARGET_HEIGHT
from config.settings import (
    CROP_TOP_RATIO,
    CROP_BOTTOM_RATIO,
    CROP_LEFT_RATIO,
    CROP_RIGHT_RATIO,
)


def resize_to_height(image: np.ndarray, target_height: int = TARGET_HEIGHT) -> np.ndarray:
    h = image.shape[0]

    if h == 0:
        return image

    scale = target_height / h

    return cv2.resize(
        image,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC
    )


def crop_roi(image: np.ndarray) -> np.ndarray:
    h, w = image.shape[:2]

    top = int(CROP_TOP_RATIO * h)
    bottom = int(CROP_BOTTOM_RATIO * h)
    left = int(CROP_LEFT_RATIO * w)
    right = int(CROP_RIGHT_RATIO * w)

    if bottom > top and right > left:
        return image[top:bottom, left:right]

    return image