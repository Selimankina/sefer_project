import cv2
import numpy as np


def resize_to_height(image: np.ndarray, target_height: int = 640) -> np.ndarray:
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

    top = int(0.2 * h)
    bottom = int(0.8 * h)
    left = int(0.1 * w)
    right = int(0.75 * w)

    if bottom > top and right > left:
        return image[top:bottom, left:right]

    return image