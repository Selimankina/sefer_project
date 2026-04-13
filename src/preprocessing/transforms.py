import cv2
import numpy as np


def perspective_transform(image: np.ndarray, rect: np.ndarray) -> np.ndarray | None:
    tl, tr, br, bl = rect

    width = int(max(
        np.linalg.norm(br - bl),
        np.linalg.norm(tr - tl)
    ))

    height = int(max(
        np.linalg.norm(tr - br),
        np.linalg.norm(tl - bl)
    ))

    if width == 0 or height == 0:
        return None

    dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")

    m = cv2.getPerspectiveTransform(rect, dst)

    return cv2.warpPerspective(image, m, (width, height))


def normalize_orientation(image: np.ndarray) -> np.ndarray:
    h, w = image.shape[:2]
    return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE) if h > w else image