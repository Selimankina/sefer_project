from config.settings import MIN_DIGIT_HEIGHT

from src.number_assembly.geometry import fit_baseline, distance_to_line, filter_overlapping

def filter_by_height(digits):
    """
        Фильтрует цифры по минимальной высоте.

        Args:
            digits (list[Digit]): Список детекций.

        Returns:
            list[Digit]: Отфильтрованный список, содержащий только цифры
            с высотой >= MIN_DIGIT_HEIGHT.
        """

    return [d for d in digits if d.height >= MIN_DIGIT_HEIGHT]


def filter_by_line(digits):
    """
        Фильтрует цифры по отклонению от базовой линии.

        Строит линию по центрам цифр и удаляет
        те, которые находятся слишком далеко от неё.

        Args:
            digits (list[Digit]): Список детекций.

        Returns:
            list[Digit]: Отфильтрованный список.
        """
    if not digits:
        return digits

    avg_height = sum(d.height for d in digits) / len(digits)

    filtered_for_line = [
        d for d in digits
        if d.height >= avg_height * 0.7
    ]

    if len(filtered_for_line) < 2:
        filtered_for_line = digits

    k, b = fit_baseline(filtered_for_line)

    digits_with_dist = [
        (d, distance_to_line(d, k, b))
        for d in digits
    ]

    digits_with_dist.sort(key=lambda x: x[1])

    # --- сначала убираем мелкий мусор ---
    filtered = [
        (d, dist)
        for d, dist in digits_with_dist
        if d.height >= avg_height * 0.8
    ]

    # fallback
    if len(filtered) < 2:
        filtered = digits_with_dist

    TOP_K = 4
    return [d for d, _ in filtered[:TOP_K]]



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