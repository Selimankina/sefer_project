import numpy as np


def fit_baseline(digits):
    """
    Строит линию по центрам цифр.

    Пытается провести прямую (y = kx + b), которая лучше всего
    проходит через центры всех цифр.

    Args:
        digits (list[Digit]): Список найденных цифр.

    Returns:
        tuple[float, float]:
            k — наклон линии,
            b — смещение по оси Y.

    Notes:
        Если цифр меньше двух, возвращается горизонтальная линия
        на уровне первой цифры (или 0.0, если список пуст).
    """
    if len(digits) < 2:
        return 0.0, digits[0].center_y if digits else 0.0

    xs = np.array([d.center_x for d in digits])
    ys = np.array([d.center_y for d in digits])

    k, b = np.polyfit(xs, ys, 1)

    return k, b


def distance_to_line(d, k, b):
    """
    Считает расстояние от цифры до линии.

    Args:
        d (Digit): Цифра (используется её центр).
        k (float): Наклон линии.
        b (float): Смещение линии.

    Returns:
        float: Расстояние от центра цифры до линии.
    """
    x = d.center_x
    y = d.center_y

    return abs(k * x - y + b) / (k**2 + 1) ** 0.5