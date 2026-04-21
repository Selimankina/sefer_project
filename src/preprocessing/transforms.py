import cv2
import numpy as np


def perspective_transform(image: np.ndarray, rect: np.ndarray) -> np.ndarray | None:
    """
        Преобразует изображение в прямоугольник по заданным углам.

        Выполняет перспективное преобразование (warp perspective),
        чтобы выровнять наклонённую область ROI.

        Args:
            image (np.ndarray): Входное изображение.
            rect (np.ndarray): 4 точки (tl, tr, br, bl), задающие область.

        Returns:
            np.ndarray | None: Выровненное изображение или None,
            если вычислить размеры невозможно.
        """
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
    """
        Нормализует ориентацию изображения.

        Если изображение горизонтальное (шире, чем выше),
        поворачивает его на 90° по часовой стрелке.

        Args:
            image (np.ndarray): Входное изображение.

        Returns:
            np.ndarray: Изображение в нормализованной ориентации.
        """
    h, w = image.shape[:2]
    return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE) if h > w else image