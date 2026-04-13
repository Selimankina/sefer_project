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


def filter_by_line(digits, distance_ratio=0.5):
    if not digits:
        return digits

    # --- 1. фит линии ---
    k, b = fit_baseline(digits)

    # --- 2. считаем расстояния ---
    distances = [distance_to_line(d, k, b) for d in digits]

    # --- 3. адаптивный threshold ---
    heights = [d.height for d in digits]
    avg_height = sum(heights) / len(heights)

    threshold = avg_height * distance_ratio

    # --- 4. фильтрация ---
    filtered = [
        d for d, dist in zip(digits, distances)
        if dist <= threshold
    ]

    return filtered

def filter_by_height(digits, min_height=90):
    return [d for d in digits if d.height >= min_height]

def assemble_number(digits):
    if not digits:
        return None, 0.0, "no_digits"

    # 2. фильтр по высоте
    digits = filter_by_height(digits, min_height=90)

    if not digits:
        return None, 0.0, "no_digits_after_height_filter"

    # 3. фильтр по линии
    digits = filter_by_line(digits)

    if not digits:
        return None, 0.0, "no_digits_after_line_filter"

    # 4. сортировка
    digits = sorted(digits, key=lambda d: d.center_x)

    labels = [d.label for d in digits]

    # 5. проверка формата
    digits_only = [l for l in labels if l.isdigit()]
    letters = [l for l in labels if l.isalpha()]

    if not (1 <= len(digits_only) <= 4):
        return None, 0.0, "invalid_format"

    if len(letters) > 1:
        return None, 0.0, "invalid_format"

    if letters:
        if letters[0] not in list("abcde"):
            return None, 0.0, "invalid_format"

        if not labels[-1].isalpha():
            return None, 0.0, "invalid_format"

    # 6. сбор строки
    number = "".join(labels)

    # 7. confidence
    confidence = sum(d.confidence for d in digits) / len(digits)

    return number, confidence, None