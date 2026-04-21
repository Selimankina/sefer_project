from config.settings import MIN_DIGIT_HEIGHT

from src.number_assembly.geometry import (filter_by_height,
                                          filter_by_line,
                                          filter_overlapping
                                          )


def assemble_number(digits):
    """
    Собирает номер из списка детекций.

    Последовательно:
    - фильтрует по высоте;
    - фильтрует по линии;
    - сортирует слева направо;
    - проверяет формат;
    - вычисляет confidence.

    Args:
        digits (list[Digit]): Список детекций.

    Returns:
        tuple[str | None, float, dict]:
            number (str | None): Собранный номер или None при ошибке.
            confidence (float): Средняя уверенность.
            meta (dict): Дополнительная информация или ошибка.
    """

    if not digits:
        return None, 0.0, {"error": "no_digits"}

    # --- height ---
    digits = filter_by_height(digits)
    if not digits:
        return None, 0.0, {"error": "no_digits_after_height"}

    # --- overlap ---
    digits = filter_overlapping(digits)
    if not digits:
        return None, 0.0, {"error": "no_digits_after_overlap"}

    # --- line ---
    digits = filter_by_line(digits)
    if not digits:
        return None, 0.0, {"error": "no_digits_after_line"}

    # --- sort ---
    digits = sorted(digits, key=lambda d: d.center_x)
    labels = [d.label for d in digits]

    if not (1 <= len(labels) <= 4):
        return None, 0.0, {"error": "invalid_format"}

    number = "".join(labels)

    # --- номер не может состоять только из нулей ---
    if set(number) == {"0"}:
        return None, 0.0, {"error": "invalid_format"}

    confidence = sum(d.confidence for d in digits) / len(digits)

    return number, confidence, {
        "num_digits": len(digits),
    }