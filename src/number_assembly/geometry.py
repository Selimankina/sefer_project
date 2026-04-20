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

    digits = sorted(digits, key=lambda d: d.center_x)

    xs = np.array([d.center_x for d in digits])
    ys = np.array([d.center_y for d in digits])

    # 1. убрать крайние выбросы по X

    if len(digits) >= 5:
        xs = xs[1:-1]
        ys = ys[1:-1]

    # 2. базовая линия через polyfit
    k, b = np.polyfit(xs, ys, 1)

    # 3. стабилизация по медиане Y
    b = np.median(ys - k * xs)

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

def is_center_inside(d1, d2, scale=0.6):
    """
    Проверяет, является ли d1 дубликатом d2 по близости центров.

    Использует ту же систему координат, что fit_baseline:
    center_x / center_y.
    """

    dx = d1.center_x - d2.center_x
    dy = d1.center_y - d2.center_y

    distance = (dx ** 2 + dy ** 2) ** 0.5

    # масштабируем допустимое расстояние через размеры цифры
    threshold = d2.height * scale

    return distance <= threshold


def filter_overlapping(digits):
    """
    Удаляет пересекающиеся (дублирующие) боксы.

    Если центр одного бокса попадает в другой —
    оставляем только тот, у которого выше confidence.

    Args:
        digits (list[Digit])

    Returns:
        list[Digit]
    """
    if not digits:
        return digits

    # сортируем по уверенности (сильные — первыми)
    digits = sorted(digits, key=lambda d: d.confidence, reverse=True)

    result = []

    for d in digits:
        is_duplicate = False

        for kept in result:
            if is_center_inside(d, kept) or is_center_inside(kept, d):
                is_duplicate = True
                break

        if not is_duplicate:
            result.append(d)

    return result