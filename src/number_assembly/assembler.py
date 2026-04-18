from config.settings import (
    MIN_DIGIT_HEIGHT,
    LINE_DISTANCE_RATIO,
    VALID_LETTERS,
)

from src.number_assembly.geometry import fit_baseline, distance_to_line

def filter_by_height(digits):
    return [d for d in digits if d.height >= MIN_DIGIT_HEIGHT]


def filter_by_line(digits):
    if not digits:
        return digits

    k, b = fit_baseline(digits)

    distances = [distance_to_line(d, k, b) for d in digits]

    avg_height = sum(d.height for d in digits) / len(digits)
    threshold = avg_height * LINE_DISTANCE_RATIO

    return [
        d for d, dist in zip(digits, distances)
        if dist <= threshold
    ]


def assemble_number(digits):
    if not digits:
        return None, 0.0, {"error": "no_digits"}

    # --- height ---
    digits = filter_by_height(digits)
    if not digits:
        return None, 0.0, {"error": "no_digits_after_height"}

    # --- line ---
    digits = filter_by_line(digits)
    if not digits:
        return None, 0.0, {"error": "no_digits_after_line"}

    # --- sort ---
    digits = sorted(digits, key=lambda d: d.center_x)
    labels = [d.label for d in digits]

    digits_only = [l for l in labels if l.isdigit()]
    letters = [l for l in labels if l.isalpha()]

    if not (1 <= len(digits_only) <= 4):
        return None, 0.0, {"error": "invalid_format"}

    if len(letters) > 1:
        return None, 0.0, {"error": "invalid_format"}

    if letters:
        if letters[0] not in VALID_LETTERS:
            return None, 0.0, {"error": "invalid_format"}

        if not labels[-1].isalpha():
            return None, 0.0, {"error": "invalid_format"}

    number = "".join(labels)
    confidence = sum(d.confidence for d in digits) / len(digits)

    return number, confidence, {
        "num_digits": len(digits),
        "has_letter": bool(letters),
    }