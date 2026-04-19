import numpy as np
from config.settings import ROI_MIN_EDGE_LENGTH


def validate_keypoints(keypoints, conf_threshold: float) -> bool:
    """
        Проверяет корректность keypoints.

        Условие:
        - должно быть минимум 4 точки;
        - все точки должны иметь confidence выше порога.

        Args:
            keypoints (list): Список keypoints (x, y, confidence).
            conf_threshold (float): Минимальный порог уверенности.

        Returns:
            bool: True, если keypoints валидны, иначе False.
        """
    if not keypoints or len(keypoints) < 4:
        return False

    return sum(kp[2] >= conf_threshold for kp in keypoints) == 4


def validate_geometry(rect: np.ndarray) -> bool:
    """
        Проверяет корректность геометрии четырёхугольника.

        Условия:
        - форма должна быть (4, 2);
        - стороны не должны быть слишком короткими;
        - точки должны образовывать выпуклый четырёхугольник.

        Args:
            rect (np.ndarray): 4 точки (tl, tr, br, bl).

        Returns:
            bool: True, если геометрия корректна.
        """
    if rect.shape != (4, 2):
        return False

    tl, tr, br, bl = rect

    edges = [
        tr - tl,
        br - tr,
        bl - br,
        tl - bl
    ]

    if min(np.linalg.norm(e) for e in edges) < ROI_MIN_EDGE_LENGTH:
        return False

    def cross(a, b):
        return a[0] * b[1] - a[1] * b[0]

    crosses = [
        cross(edges[i], edges[(i + 1) % 4])
        for i in range(4)
    ]

    return all(c > 0 for c in crosses) or all(c < 0 for c in crosses)