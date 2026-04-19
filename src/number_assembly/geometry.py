import numpy as np


def fit_baseline(digits):
    """
    Находит линию y = kx + b через центры цифр
    """
    if len(digits) < 2:
        return 0.0, digits[0].center_y if digits else 0.0

    xs = np.array([d.center_x for d in digits])
    ys = np.array([d.center_y for d in digits])

    k, b = np.polyfit(xs, ys, 1)

    return k, b


def distance_to_line(d, k, b):
    """
    Перпендикулярное расстояние от точки до линии
    """
    x = d.center_x
    y = d.center_y

    return abs(k * x - y + b) / (k**2 + 1) ** 0.5